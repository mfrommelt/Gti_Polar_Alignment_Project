# OpenAstroTracker AutoPA Analysis

## What OpenAstroTracker AutoPA Does

The OpenAstroTracker (OAT) AutoPA system is an **automated polar alignment addon** that:

1. **Motorizes ALT and AZ adjustments** (just like your system!)
2. **Integrates with plate solving software** (SharpCap, NINA, Ekos)
3. **Reads correction values from log files**
4. **Automatically adjusts the mount** until aligned

---

## Key Architecture - How It Works

### The Workflow:

```
1. User starts plate solving software (SharpCap/NINA/Ekos)
2. Software takes images and calculates polar alignment error
3. Software writes error to log file (ALT error, AZ error in arcseconds)
4. AutoPA Python script reads the log file
5. AutoPA sends commands to mount via ASCOM/INDI
6. Mount adjusts ALT and AZ
7. Software re-solves to check alignment
8. Repeat until error < target threshold
```

### The Genius: **Log File Parsing**

Instead of implementing plate solving themselves, they:
- Let professional software (SharpCap/NINA) do the plate solving
- Parse the software's log files for error values
- React to those errors by moving the mount

---

## The autopa_v2.py Script - Key Features

### 1. **Multi-Software Support**

Supports log file formats from:
- **NINA** (Three Point Polar Alignment plugin)
- **SharpCap 3.2 and 4.0** (Polar Alignment Routine)
- **Ekos** (KStars polar alignment module)

### 2. **Log File Parsing**

```python
softwareTypes = {
    "NINA": {
        "expression": r"(\d{2}:\d{2}:\d{2}.\d{3})\s-\s({.*})",
        "logpath": f"{Path.home()}\Documents\N.I.N.A\PolarAlignment\*.log"
    },
    "Sharpcap4.0": {
        "expression": r"(?:Info)\W*(\d{2}:\d{2}:\d{2}.\d{6}).*(?:AltAzCor=)(?:Alt=)(.*)[,](?:Az=)(.*)...",
        "logpath": f"{os.getenv('LOCALAPPDATA')}\SharpCap\logs\*.log"
    },
    "Ekos": {
        "expression": r"(\d{2}:\d{2}:\d{2}.\d{3}).*(?:PAA Refresh).*(?:Corrected az:).*...",
        "logpath": "path_to_ekos_log"
    }
}
```

**What they extract:**
- Timestamp of log entry
- ALT correction needed (in arcseconds or arcminutes)
- AZ correction needed (in arcseconds or arcminutes)

### 3. **Mount Control via ASCOM/INDI**

```python
# Connects to mount via:
# - ASCOM (Windows) - OATControl, NINA, SharpCap
# - INDI (Linux) - Ekos/KStars

# Sends move commands to ALT/AZ motors
mount.move_altitude(alt_correction_steps)
mount.move_azimuth(az_correction_steps)
```

### 4. **Iterative Refinement**

```python
while polar_alignment_error > target_threshold:
    1. Wait for new log entry (plate solve result)
    2. Parse ALT/AZ error values
    3. Convert arcseconds to motor steps
    4. Send movement commands
    5. Wait for movement to complete
    6. Wait for software to re-solve
    7. Check if error is now acceptable
```

### 5. **Error Handling**

- Detects if log file is stale (no new entries)
- Handles connection errors to mount
- Prevents movement if error is too large (safety)
- Stops if software stops generating log entries

---

## How This Applies to Your System

### What You Can Adopt Directly:

#### 1. **Same Hardware Architecture** ✅
Your system already has:
- ALT motor (altitude adjustment)
- AZ motors (azimuth adjustment - differential)
- Arduino controller
- Serial/USB communication

**This is IDENTICAL to OAT's AutoPA hardware!**

#### 2. **Add Plate Solving Integration** 🎯

**Option A: Parse SharpCap Logs**

Create a Python script that:
```python
import re
import time
from polar_align_control import Controller

# Connect to your Arduino
controller = Controller('/dev/ttyUSB0')

# Monitor SharpCap log file
log_file = os.path.join(os.getenv('LOCALAPPDATA'), 'SharpCap', 'logs', 'log.txt')

# Parse for polar alignment errors
pattern = r'AltAzCor=Alt=(.*),Az=(.*)'

while True:
    # Read new log entries
    with open(log_file, 'r') as f:
        for line in f:
            match = re.search(pattern, line)
            if match:
                alt_error = float(match.group(1))  # arcseconds
                az_error = float(match.group(2))   # arcseconds
                
                # Convert to steps (using your calibration)
                alt_steps = int(alt_error * calibration.altStepsPerArcsec)
                az_steps = int(az_error * calibration.azStepsPerArcsec)
                
                # Move mount
                controller.send_command(f'A{alt_steps}')
                controller.send_command(f'Z{az_steps}')
                
                # Wait for next solve
                time.sleep(30)
```

**Option B: Parse NINA Logs**

```python
# NINA logs to:
# C:\Users\<username>\Documents\N.I.N.A\PolarAlignment\*.log

# Format:
# 12:34:56.789 - {"Alt": 120.5, "Az": -45.2, "Total": 128.7}

import json

pattern = r'(\d{2}:\d{2}:\d{2}.\d{3})\s-\s({.*})'
match = re.search(pattern, log_line)
if match:
    data = json.loads(match.group(2))
    alt_error = data['Alt']  # arcseconds
    az_error = data['Az']    # arcseconds
```

#### 3. **Add ASCOM Server Support** 🚀

**Make your Arduino controllable via ASCOM:**

```python
# Create ASCOM Alpaca server
# This lets SharpCap/NINA/etc control your mount directly

from alpaca.telescope import Telescope

class PolarAlignMount(Telescope):
    def MoveAxis(self, axis, rate):
        if axis == 0:  # ALT
            self.arduino.send_command(f'A{int(rate * 1000)}')
        elif axis == 1:  # AZ
            self.arduino.send_command(f'Z{int(rate * 1000)}')
```

---

## Comparison: OAT AutoPA vs Your System

| Feature | OpenAstroTracker AutoPA | Your System (Current) | Your System (Enhanced) |
|---------|------------------------|----------------------|----------------------|
| **Hardware** | 2 motors (ALT + AZ) | 3 motors (ALT + AZ diff) | Same |
| **Mount Type** | Full equatorial | Compact alt-az adjust | Same |
| **Control** | Arduino firmware | Arduino firmware | Same |
| **Communication** | ASCOM/INDI | Serial/USB | ASCOM + Serial |
| **Plate Solving** | External (SharpCap/NINA) | None (manual) | External (SharpCap/NINA) |
| **Automation** | Full auto via logs | Manual via Python | Full auto via logs |
| **Calibration** | Manual | Wizard-assisted | Wizard-assisted |
| **Software** | Python (log parser) | Python (CLI) | Python (log parser) |

---

## Recommended Enhancements for Your System

### Phase 1: Log File Integration (Easy - 2-4 hours)

**Create:** `plate_solving_autopa.py`

```python
#!/usr/bin/env python3
"""
Automatic Polar Alignment using SharpCap/NINA
Monitors log files and adjusts mount automatically
"""

import os
import re
import time
from pathlib import Path
from polar_align_control import Controller

class AutoPA:
    def __init__(self, software='sharpcap'):
        self.controller = Controller()
        self.software = software
        self.calibration = self.load_calibration()
        
    def monitor_sharpcap_logs(self):
        log_path = Path(os.getenv('LOCALAPPDATA')) / 'SharpCap' / 'logs'
        pattern = r'AltAzCor=Alt=([-\d.]+),Az=([-\d.]+)'
        
        # Monitor latest log file
        latest_log = max(log_path.glob('*.log'), key=os.path.getmtime)
        
        print(f"Monitoring: {latest_log}")
        print("Start SharpCap Polar Alignment routine...")
        
        last_position = 0
        
        while True:
            with open(latest_log, 'r') as f:
                f.seek(last_position)
                new_lines = f.readlines()
                last_position = f.tell()
                
                for line in new_lines:
                    match = re.search(pattern, line)
                    if match:
                        alt_error = float(match.group(1))  # arcseconds
                        az_error = float(match.group(2))
                        
                        print(f"\nPolar Alignment Error:")
                        print(f"  ALT: {alt_error:.1f} arcseconds")
                        print(f"  AZ:  {az_error:.1f} arcseconds")
                        
                        if abs(alt_error) < 30 and abs(az_error) < 30:
                            print("\n✓ Polar alignment achieved!")
                            return
                        
                        # Convert to steps
                        alt_steps = int(alt_error * self.calibration['alt'])
                        az_steps = int(az_error * self.calibration['az'])
                        
                        print(f"Correcting:")
                        print(f"  ALT: {alt_steps} steps")
                        print(f"  AZ:  {az_steps} steps")
                        
                        # Move mount
                        self.controller.move_altitude(alt_steps)
                        self.controller.move_azimuth(az_steps)
                        
                        print("Waiting for next solve...")
            
            time.sleep(1)  # Check for new log entries every second

if __name__ == '__main__':
    autopa = AutoPA()
    autopa.monitor_sharpcap_logs()
```

**How to use:**
```bash
# 1. Start your Arduino mount system
python polar_align_control.py

# 2. In another terminal, start AutoPA monitor
python plate_solving_autopa.py

# 3. Open SharpCap
# 4. Start Polar Alignment routine
# 5. Watch your mount automatically adjust!
```

### Phase 2: ASCOM Integration (Medium - 1-2 days)

**Benefits:**
- SharpCap/NINA can control your mount directly
- No log file parsing needed
- More elegant integration
- Standard astronomy interface

**Create:** `ascom_server.py`

```python
# Python ASCOM Alpaca server
# Exposes your Arduino as ASCOM telescope device

from alpaca.telescope import Telescope
from polar_align_control import Controller

class StarAdventurerAutoPA(Telescope):
    def __init__(self):
        super().__init__()
        self.controller = Controller()
        
    def MoveAxis(self, axis, rate):
        """Called by SharpCap during polar alignment"""
        if axis == 0:  # Primary (ALT)
            steps = int(rate * 100)  # Convert rate to steps
            self.controller.send_command(f'A{steps}')
        elif axis == 1:  # Secondary (AZ)
            steps = int(rate * 100)
            self.controller.send_command(f'Z{steps}')

# Start ASCOM server
server = StarAdventurerAutoPA()
server.start(host='127.0.0.1', port=11111)
```

**Then in SharpCap:**
1. Select "ASCOM Alpaca Telescope"
2. Enter: `http://127.0.0.1:11111`
3. Start Polar Alignment
4. SharpCap directly controls your mount!

### Phase 3: NINA Integration (Medium - 1-2 days)

**NINA Three Point Polar Alignment (TPPA):**
- More accurate than SharpCap (uses 3 images)
- Doesn't require view of Polaris
- Free and open source

**Implementation:**
Same as SharpCap, but parse NINA logs:
```
C:\Users\<username>\Documents\N.I.N.A\PolarAlignment\<date>.log
```

---

## Suggested Roadmap

### Immediate (This Weekend):

1. ✅ **Test OAT AutoPA concept manually:**
   ```bash
   # Run SharpCap polar alignment
   # Note the ALT/AZ errors shown
   # Manually send commands to your Arduino
   # Verify this works end-to-end
   ```

2. ✅ **Create basic log parser:**
   ```bash
   python plate_solving_autopa.py --software sharpcap
   ```

### Near Term (Next Week):

3. **Add error checking:**
   - Safety limits (don't move too far)
   - Stale log detection
   - Connection error handling

4. **Test with real stars:**
   - Actual polar alignment session
   - Measure accuracy improvement
   - Tune calibration if needed

### Long Term (Next Month):

5. **ASCOM server implementation**
6. **NINA TPPA integration**
7. **Ekos support (Linux users)**
8. **Web interface** (optional - overkill but cool!)

---

## Key Insights from OAT AutoPA

### What They Did Right:

1. **Leveraged existing software**
   - Didn't reinvent plate solving
   - Used professional tools (SharpCap/NINA)
   - Just bridged the gap

2. **Simple architecture**
   - Log files are easy to parse
   - Regular expressions handle variations
   - Timestamp tracking prevents duplicates

3. **Multi-software support**
   - Not locked to one platform
   - Users choose their preferred tool
   - Increased adoption

4. **Safety features**
   - Movement limits
   - Connection monitoring
   - Error thresholds

### What We Can Improve:

1. **Better calibration system** ✅ (You already have this!)
2. **More robust serial communication**
3. **Real-time feedback in UI**
4. **Automated backlash handling** ✅ (You have this!)
5. **ASCOM direct control** (not just logs)

---

## Example Session

### Fully Automated Polar Alignment:

```bash
# Terminal 1: Start your mount control
$ python polar_align_control.py
Star Adventurer GTi Polar Alignment Controller
Ready.

# Terminal 2: Start AutoPA
$ python plate_solving_autopa.py
AutoPA Starting...
Monitoring SharpCap logs...
Waiting for polar alignment routine to start...
```

**Then in SharpCap:**
```
1. Open Polar Alignment
2. Click "Start"
3. SharpCap takes image, solves
4. Displays: "ALT: +120", AZ: -45"
```

**AutoPA Terminal shows:**
```
Polar Alignment Error Detected:
  ALT: +120.5 arcseconds
  AZ:  -45.2 arcseconds

Calculating corrections...
  ALT: +10785 steps (120.5 * 89.5)
  AZ:  -1130 steps (-45.2 * 25.0)

Sending commands...
  A10785 ✓
  Z-1130 ✓

Waiting for mount to complete...
Done.

Waiting for SharpCap to re-solve...
```

**SharpCap re-solves:**
```
New error: "ALT: +15", AZ: -8"
```

**AutoPA:**
```
Polar Alignment Error Detected:
  ALT: +15.2 arcseconds
  AZ:  -8.1 arcseconds

Correcting...
Done.

Waiting for re-solve...

New error: ALT: +2", AZ: +1"

✓ Polar alignment achieved!
  Final error: 2.2 arcseconds total
  
AutoPA complete. You may now start imaging.
```

**Total time: 3-5 minutes from start to perfect alignment!**

---

## Implementation Priority

### Must Have (Core Functionality):
1. ✅ Calibration system (you have this!)
2. ✅ Motor control (you have this!)
3. **Log file parser** ← Build this next
4. **Error-to-steps conversion** ← Easy with calibration
5. **Safety limits** ← Prevent crashes

### Should Have (Better UX):
6. Multi-software support (SharpCap + NINA)
7. Visual feedback (terminal UI)
8. Configuration file (save settings)
9. Movement status display

### Nice to Have (Professional):
10. ASCOM server (direct control)
11. Web interface
12. Logging and analytics
13. Auto-calibration from plate solving

---

## Code Structure

### Recommended File Organization:

```
polar_align_controller/
├── arduino/
│   └── polar_align_controller_v3_calibration.ino  ← You have this
├── python/
│   ├── polar_align_control.py                     ← You have this
│   ├── calibration_wizard.py                      ← You have this
│   ├── plate_solving_autopa.py                    ← NEW: Log parser
│   ├── ascom_server.py                            ← NEW: ASCOM interface
│   └── config.py                                  ← NEW: Configuration
├── docs/
│   ├── CALIBRATION_GUIDE.md                       ← You have this
│   ├── AUTOPA_INTEGRATION.md                      ← NEW: This guide
│   └── ASCOM_SETUP.md                             ← NEW: ASCOM docs
└── README.md
```

---

## Next Steps

### Option 1: Quick Test (Today - 1 hour)

```bash
# 1. Download OAT AutoPA script to study:
wget https://raw.githubusercontent.com/OpenAstroTech/OpenAstroTracker-Addons/master/AutoPA/Software/source/autopa_v2.py

# 2. Extract just the log parsing regex
# 3. Create minimal test script
# 4. Run SharpCap polar alignment (trial version)
# 5. Watch log file populate
# 6. Parse and print errors
```

### Option 2: Full Implementation (This Weekend)

```bash
# 1. Create plate_solving_autopa.py
# 2. Add SharpCap log parsing
# 3. Integrate with your controller
# 4. Test with real mount
# 5. Measure accuracy
```

### Option 3: Professional Solution (Next 2 Weeks)

```bash
# 1. Study ASCOM Alpaca protocol
# 2. Implement ASCOM server
# 3. Add NINA support
# 4. Create web UI
# 5. Open source release
```

---

## Summary

**What OpenAstroTracker taught us:**

✅ **Your hardware is perfect** - same architecture as OAT  
✅ **Don't reinvent plate solving** - use existing software  
✅ **Log file parsing works** - simple and effective  
✅ **Calibration is key** - you already have this!  
✅ **Iterative refinement** - solve → adjust → repeat  

**What you should build next:**

1. **`plate_solving_autopa.py`** - Monitor SharpCap logs
2. Test with real mount and stars
3. Add NINA support
4. Consider ASCOM server

**Estimated time to working AutoPA:**
- Basic (log parsing): **4-6 hours**
- Full featured: **2-3 days**
- Professional (ASCOM): **1-2 weeks**

**Your system is 90% there!** Just need the software bridge to plate solving. 🎯

# Calibration System - Feature Summary

## What Was Added

Your polar alignment automation system now includes a **complete calibration system** for measuring and compensating:

1. **Steps per Arcsecond** (ALT and AZ)
2. **Backlash** (dead zones in direction reversals)
3. **Automatic Compensation** (firmware applies corrections)

---

## New Files Created

### 1. Enhanced Arduino Firmware
**File:** `arduino/polar_align_controller_v3_calibration.ino`

**Features:**
- Calibration data structure with EEPROM storage
- Commands for setting/loading/saving calibration
- Automatic backlash compensation in movements
- Position tracking with direction awareness
- Checksum validation for data integrity

**New Commands:**
```
CAL:ALT:<arcsec>:<steps>    - Set ALT calibration
CAL:AZ:<arcsec>:<steps>     - Set AZ calibration
CAL:ALTBL:<steps>           - Set ALT backlash
CAL:AZBL:<steps>            - Set AZ backlash
CAL:SAVE                    - Save to EEPROM
CAL:LOAD                    - Load from EEPROM
CAL:SHOW                    - Display calibration
CAL:RESET                   - Reset to defaults
```

### 2. Python Calibration Wizard
**File:** `python/calibration_wizard.py`

**Features:**
- Interactive step-by-step calibration
- Three calibration methods (star drift, reticle, manual)
- Guided backlash measurement
- Auto-detection of Arduino
- EEPROM save/load
- Beautiful terminal UI

**Usage:**
```bash
python calibration_wizard.py        # Auto-detect port
python calibration_wizard.py COM3   # Specify port
```

### 3. Comprehensive Guide
**File:** `CALIBRATION_GUIDE.md`

**Contents:**
- Theory and concepts (why calibration matters)
- Three calibration methods explained
- Step-by-step procedures for each method
- Backlash measurement guide
- Best practices and troubleshooting
- Expected values reference
- Command reference
- Testing procedures

---

## How It Works

### Step 1: Measure Steps Per Arcsecond

**Concept:**  
Determine how many motor steps = 1 arcsecond of mount movement

**Methods Available:**

**A. Star Drift Timing (Most Accurate - ±1-2%)**
```
1. Point at star near celestial equator
2. Turn off tracking
3. Move mount with motors
4. Time how long for star to drift back
5. Earth rotates 15 arcsec/second
6. Calculate: steps ÷ (time × 15) = steps/arcsec
```

**B. Polar Scope Reticle (Good - ±5-10%)**
```
1. Note starting position on polar scope reticle
2. Move mount with motors
3. Measure angular change on reticle
4. Calculate: steps ÷ arcseconds = steps/arcsec
```

**C. Manual Calculation (Acceptable - ±20-30%)**
```
1. Calculate from gear ratios
2. Or measure with protractor
3. Convert to steps/arcsec
```

### Step 2: Measure Backlash

**Concept:**  
Measure dead zone when reversing direction

**Procedure:**
```
1. Move forward 2000 steps
2. Reverse direction slowly
3. Count steps until actual movement starts
4. That count = backlash in steps
```

**Typical Values:**
- ALT: 10-50 steps
- AZ: 5-30 steps

### Step 3: Save to EEPROM

**Permanent Storage:**
```
CAL:SAVE command writes data to Arduino EEPROM
- Survives power cycles
- Loads automatically on startup
- No need to recalibrate each session!
```

### Step 4: Automatic Compensation

**Firmware Handles It:**
```cpp
When moving:
1. Check if direction changed
2. If yes, add backlash steps first (don't count position)
3. Then do normal movement
4. Result: Accurate positioning!
```

---

## Example Calibration Session

### Using the Wizard

```bash
$ python calibration_wizard.py

╔════════════════════════════════════════════════════════════════╗
║    Star Adventurer GTi Calibration Wizard                     ║
╚════════════════════════════════════════════════════════════════╝

✓ Connected to Arduino on /dev/ttyUSB0

--- ALT Calibration ---
Method: Star Drift Timing

1. Point at star, center in eyepiece
2. Moving 1000 steps...
3. Time drift back to center: 11.2 seconds
4. Calculated: 168 arcseconds moved
5. Result: 5.95 steps/arcsecond

Save? yes
✓ ALT calibration set

--- AZ Calibration ---
Method: Polar Scope Reticle

1. Note position on reticle
2. Moving 500 steps...
3. Measure movement: 20 arcseconds
4. Result: 25 steps/arcsecond

Save? yes
✓ AZ calibration set

--- ALT Backlash ---
1. Moving forward...
2. Reversing slowly...
3. Count steps: 23 steps

Save? yes
✓ ALT backlash set

--- AZ Backlash ---
Result: 15 steps
✓ AZ backlash set

--- Final Calibration ---
ALT: 5.95 steps/arcsec, 23 steps backlash
AZ:  25 steps/arcsec, 15 steps backlash

Save to EEPROM? yes
✓ Calibration saved permanently!

Calibration Complete! 🎯
```

### Manual Commands

```bash
# View current calibration
> CAL:SHOW

=== CALIBRATION DATA ===
Calibrated: YES

Steps per arcsecond:
  ALT: 89.50 steps/arcsec
  AZ:  25.00 steps/arcsec

Backlash:
  ALT: 23 steps
  AZ:  15 steps

# Set ALT: 60 arcseconds in 5400 steps
> CAL:ALT:60:5400
OK:ALT_CAL_SET
INFO:ALT calibration: 90.00 steps/arcsec

# Set backlash
> CAL:ALTBL:23
OK:ALT_BACKLASH_SET

# Save
> CAL:SAVE
OK:CAL_SAVED
```

---

## Benefits

### Before Calibration:
```
❌ Guessing how far mount moves
❌ Unknown backlash causes inaccuracy
❌ Can't convert arcseconds to steps
❌ Positioning errors accumulate
❌ Poor polar alignment results
```

### After Calibration:
```
✅ Know exact steps per arcsecond
✅ Automatic backlash compensation
✅ Can command in arcseconds
✅ Repeatable positioning
✅ Sub-arcminute polar alignment!
```

### Real-World Impact

**Scenario:** Plate solving shows error of 120 arcseconds

**Without Calibration:**
```
"Um... try moving 3000 steps?"
Result: Moved 95 arcseconds (still off by 25)
Try again: "Maybe 500 more steps?"
Result: Overshot by 15 arcseconds
Frustrating!
```

**With Calibration:**
```
Error: 120 arcseconds
Calculation: 120 × 25 steps/arcsec = 3000 steps
Command: Z3000
Result: Moved exactly 120 arcseconds
Perfect on first try! ✓
```

---

## Typical Calibration Values

### ALT (Altitude with Worm Gear)

**Expected Range:** 50-150 steps/arcsecond

**With your system:**
- Belt ratio: 4:1 (20T:80T)
- Worm gear: ~90:1 (estimated)
- Total: 360:1 reduction
- **Predicted: ~90 steps/arcsecond**

**Backlash:** 10-50 steps (typical: 25)

### AZ (Azimuth Differential Screws)

**Expected Range:** 15-35 steps/arcsecond

**With your system:**
- Belt ratio: 3:1 (20T:60T)
- Screw pitch: varies
- **Predicted: ~25 steps/arcsecond**

**Backlash:** 5-30 steps (typical: 15)

---

## When to Calibrate

### Must Calibrate:
- ✅ Initial system setup
- ✅ After mechanical changes (belts, gears, etc.)
- ✅ If positioning becomes inaccurate
- ✅ After replacing motors

### Don't Need to Recalibrate:
- ❌ Every session (stored in EEPROM!)
- ❌ New observing location
- ❌ Different telescope
- ❌ Normal operation

**Once calibrated, good for months or years!**

---

## Accuracy Comparison

| Method | Accuracy | Time | Requirements |
|--------|----------|------|--------------|
| Star Drift | ±1-2% | 15-30 min | Clear sky, telescope |
| Reticle | ±5-10% | 10 min | Polar scope access |
| Manual | ±20-30% | 5 min | Calculator |

**Recommendation:** Use star drift for best results!

---

## Integration with Existing System

### Firmware Compatibility

**v2 → v3 Upgrade:**
- All existing commands still work
- Position tracking unchanged
- Adds calibration features
- Backward compatible

**To Upgrade:**
```bash
1. Upload polar_align_controller_v3_calibration.ino
2. Run calibration wizard
3. Continue using normally
```

### Python Software Compatibility

**Existing software works as-is:**
- `polar_align_control.py` - no changes needed
- `test_system.py` - still works
- New: `calibration_wizard.py` - optional tool

**Future Enhancement:**
You could add arcsecond commands to Python:
```python
def move_alt_arcsec(self, arcsec):
    steps = int(arcsec * self.cal_alt_steps_per_arcsec)
    self.move_altitude(steps)
```

---

## Files Reference

### Core System (Unchanged):
```
arduino/polar_align_controller_v2_differential.ino  ← v2 firmware
python/polar_align_control.py                       ← Control software
python/test_system.py                               ← Diagnostics
README.md                                           ← Main docs
```

### Calibration System (New):
```
arduino/polar_align_controller_v3_calibration.ino  ← v3 firmware with cal
python/calibration_wizard.py                       ← Cal wizard
CALIBRATION_GUIDE.md                               ← Complete guide
CALIBRATION_FEATURES.md                            ← This summary
```

### Documentation:
```
FINAL_SYSTEM_DESIGN.md                             ← System overview
SHOPPING_LIST_UPDATED.md                           ← What to buy
COMPACT_MOTOR_SOLUTIONS.md                         ← Motor selection
+ All other existing docs                          ← Still valid
```

---

## Quick Start with Calibration

### 1. Upload Firmware
```bash
# In Arduino IDE:
1. Open polar_align_controller_v3_calibration.ino
2. Select Tools → Board → Arduino Nano
3. Select correct COM port
4. Click Upload

# Or with arduino-cli:
arduino-cli upload -p COM3 \
  --fqbn arduino:avr:nano \
  polar_align_controller_v3_calibration.ino
```

### 2. Run Wizard
```bash
cd python
python calibration_wizard.py
```

### 3. Follow Instructions
```
- Choose calibration method
- Perform measurements
- Save to EEPROM
- Done!
```

### 4. Use System
```bash
python polar_align_control.py
# System now uses calibrated values automatically
# Backlash compensation happens transparently
```

---

## Testing Your Calibration

### Accuracy Test
```python
# Move a known distance
controller.move_altitude(9000)  # If 90 steps/arcsec, this is 100 arcsec

# Measure actual movement
# Should be 100 arcseconds ±1-2 arcseconds
```

### Repeatability Test
```python
# Go to position
controller.move_altitude(5000)

# Return to zero
controller.move_altitude(-5000)

# Check position
pos = controller.get_position()
# Should be 0,0 or very close (within 2-3 steps)
```

### Backlash Test
```python
# Forward
controller.move_altitude(1000)

# Reverse
controller.move_altitude(-1000)

# Should return to exact start
# If not, backlash compensation needs adjustment
```

---

## Troubleshooting

### Problem: Calibration values seem wrong

**Check:**
- Gear ratios correct?
- Belt not skipping teeth?
- Measured correctly?
- Try different calibration method

### Problem: Backlash varies

**Causes:**
- Belt tension inconsistent → Tighten
- Worn gears → Inspect/replace
- Loose couplers → Tighten set screws

### Problem: Can't save to EEPROM

**Solutions:**
- Reset first: `CAL:RESET`
- Check Arduino model (Nano has EEPROM)
- Try different USB cable/port

---

## Advanced: Future Enhancements

### Potential Additions:

**1. Arcsecond Commands:**
```python
controller.move_alt_arcsec(120)  # Move 120 arcseconds
# Firmware calculates: 120 * steps_per_arcsec
```

**2. Plate Solving Integration:**
```python
def auto_calibrate():
    image1 = take_image()
    move_mount(1000)
    image2 = take_image()
    angle = plate_solve_difference(image1, image2)
    calibration = 1000 / angle
    save_calibration(calibration)
```

**3. Web Interface:**
```
http://localhost:8000/calibrate
# Web-based calibration wizard
# No Python installation needed
```

**4. Machine Learning:**
```python
# Learn system behavior over time
# Adapt to temperature, wear, etc.
# Self-improving calibration
```

---

## Summary

### What You Have Now:

✅ **Complete calibration system**  
✅ **Three calibration methods**  
✅ **Automatic backlash compensation**  
✅ **EEPROM storage (permanent)**  
✅ **Interactive wizard**  
✅ **Comprehensive documentation**  
✅ **Professional-grade precision**  

### What This Enables:

✅ Sub-arcminute polar alignment  
✅ Repeatable positioning  
✅ Long-exposure astrophotography  
✅ Plate solving integration  
✅ Automated polar alignment  
✅ Professional results  

---

## Ready to Calibrate! 🎯

**Your system now has the tools for precision polar alignment!**

**Next Steps:**
1. Upload v3 firmware
2. Run calibration wizard
3. Save calibration to EEPROM
4. Test accuracy
5. Start imaging!

**Clear skies and precise tracking!** 🌟✨

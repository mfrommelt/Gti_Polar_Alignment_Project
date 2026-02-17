# Quick Start Guide - Star Adventurer GTi Polar Alignment Controller

Get your automated polar alignment system running in 30 minutes!

## What You Need

### Required (Minimum for Testing)
- [ ] Arduino Nano (or Uno)
- [ ] 2x TMC2208 stepper driver boards
- [ ] 2x NEMA 17 stepper motors
- [ ] 12V 2A power supply (with barrel jack or wires)
- [ ] USB cable (for Arduino)
- [ ] ~20 jumper wires (male-to-female)
- [ ] Computer with Python installed

### Optional (For Final Build)
- [ ] GT2 timing belt (2 meters)
- [ ] GT2 pulleys (4x 20-tooth)
- [ ] Motor mounting brackets
- [ ] Breadboard (for clean wiring)

## Step-by-Step Setup (30 Minutes)

### Part 1: Electronics Assembly (15 min)

#### 1. Install Heatsinks on Drivers (2 min)
```
✓ Peel backing from heatsink
✓ Press firmly onto TMC2208 chip
✓ Repeat for both drivers
```

#### 2. Wire the System (10 min)

**Power Connections:**
```
12V Power Supply (+) → Arduino VIN
12V Power Supply (+) → TMC2208 #1 VM
12V Power Supply (+) → TMC2208 #2 VM

All GND pins connected together:
- 12V Power Supply (-)
- Arduino GND
- TMC2208 #1 GND
- TMC2208 #2 GND
```

**Arduino to TMC2208 #1 (ALT):**
```
Arduino D2 → TMC2208 #1 STEP
Arduino D3 → TMC2208 #1 DIR
Arduino D4 → TMC2208 #1 EN
```

**Arduino to TMC2208 #2 (AZ):**
```
Arduino D5 → TMC2208 #2 STEP
Arduino D6 → TMC2208 #2 DIR
Arduino D7 → TMC2208 #2 EN
```

**Motors to Drivers:**
```
Motor #1 → TMC2208 #1 (A1, A2, B1, B2)
Motor #2 → TMC2208 #2 (A1, A2, B1, B2)

Note: Use multimeter to identify motor coils:
- Measure resistance between wire pairs
- Wires of same coil show ~1-10 ohms
- Wires of different coils show infinite resistance
```

#### 3. Set Current Limit (3 min)

**CRITICAL: Do this BEFORE first power-on!**

For 0.4A motors (typical NEMA 17):
```
1. Connect 12V power (Arduino NOT connected yet)
2. Measure voltage between Vref pin and GND
3. Adjust potentiometer until Vref = 0.2V
   Formula: Vref = Motor_Current × 0.5
           Vref = 0.4A × 0.5 = 0.2V
4. Turn SLOWLY - very sensitive!
5. Repeat for both drivers
```

### Part 2: Software Setup (10 min)

#### 1. Install Arduino Firmware (5 min)

**Download Arduino IDE:**
- Windows: https://www.arduino.cc/en/software
- Mac: https://www.arduino.cc/en/software
- Linux: `sudo apt install arduino` or `brew install arduino-cli`

**Upload Firmware:**
```
1. Open Arduino IDE
2. File → Open → polar_align_controller.ino
3. Tools → Board → Arduino Nano
4. Tools → Processor → ATmega328P
5. Tools → Port → [Your COM/USB port]
6. Click Upload (→ button)
7. Wait for "Done uploading"
```

**Verify Upload:**
```
1. Tools → Serial Monitor
2. Set baud rate: 115200
3. Should see "READY" message
```

#### 2. Install Python Software (5 min)

**Install Python (if needed):**
- Windows: https://www.python.org/downloads/
  - ✓ Check "Add Python to PATH"
- Mac: `brew install python3`
- Linux: Usually pre-installed

**Install pyserial:**
```bash
# Windows
pip install pyserial

# Mac/Linux
pip3 install pyserial
```

**Test Python Software:**
```bash
# Navigate to project folder
cd polar_align_controller/python

# Run the software
python polar_align_control.py
# or
python3 polar_align_control.py
```

### Part 3: First Test (5 min)

#### 1. Power On Sequence
```
1. Connect 12V power supply
2. Connect Arduino USB to computer
3. Run Python control software
   → Should auto-connect and show menu
```

#### 2. Enable Motors
```
Command: +
Response: Motors enabled
```

#### 3. Test Movement
```
# Test ALT motor
Command: W
Response: Altitude moved 50 steps

# Test AZ motor  
Command: H
Response: Azimuth moved 50 steps

# Check position
Command: P
Response: Position - ALT: 50 steps, AZ: 50 steps
```

#### 4. Emergency Stop Test
```
Command: X
Response: Motors stopped
```

#### 5. Disable Motors
```
Command: -
Response: Motors disabled
```

## Troubleshooting Quick Fixes

### "No serial ports found"
```
Fix:
1. Check USB cable connection
2. Install Arduino drivers (if Windows)
3. Try different USB port
4. Check Device Manager (Windows) for COM port
```

### "Motors not moving"
```
Fix:
1. Enable motors: command +
2. Check all wire connections
3. Verify 12V power supply is on
4. Check Vref setting on drivers
```

### "Motors vibrate but don't move"
```
Fix:
1. Reduce speed: command V → enter 200
2. Check motor wire connections
3. Verify coil wiring (may need to swap A1/A2 or B1/B2)
```

### "Connection timeout"
```
Fix:
1. Close Serial Monitor in Arduino IDE
2. Unplug and replug USB
3. Wait 3 seconds after plugging in
4. Try running Python software again
```

## Next Steps

### Mechanical Integration

Once electronics are working:

1. **Design mounting brackets**
   - Motor bracket for ALT knob
   - Motor bracket for AZ screws
   - Can be 3D printed or fabricated from aluminum

2. **Install belt drive for ALT**
   - Mount motor next to altitude knob
   - Install pulleys on motor and knob shafts
   - Connect with GT2 timing belt
   - Adjust tension (snug, not tight)

3. **Install motors for AZ**
   - Option A: One motor per screw (dual motor)
   - Option B: Platform rotation (more complex)

4. **Calibrate**
   - Measure actual degrees per step
   - Update software presets if needed
   - Test full range of motion

### Software Enhancements

Ideas for customization:

1. **Adjust step sizes** in Python code:
   ```python
   self.FINE_STEP = 10      # Currently 10 steps
   self.SMALL_STEP = 50     # Currently 50 steps
   self.MEDIUM_STEP = 200   # Currently 200 steps
   self.LARGE_STEP = 800    # Currently 800 steps
   ```

2. **Change speed** (default 800 steps/sec):
   ```python
   self.current_speed = 800  # Adjust to your preference
   ```

3. **Add custom commands** in both Arduino and Python

## Safety Checklist

Before each use:

- [ ] All connections secure
- [ ] Power supply voltage correct (12V)
- [ ] Current limit set correctly
- [ ] Heatsinks attached to drivers
- [ ] No shorts or exposed wires
- [ ] Emergency stop tested
- [ ] Mount payload within limits (5kg)
- [ ] Counterweight installed

## Getting Help

If stuck:

1. **Check README.md** - comprehensive documentation
2. **Review wiring diagram** - verify all connections
3. **Test with multimeter** - check voltages
4. **Serial Monitor** - see Arduino debug output
5. **Python error messages** - read carefully

## Success Criteria

You're ready for polar alignment when:

- ✓ Both motors move smoothly in both directions
- ✓ Position tracking works correctly
- ✓ Speed changes take effect
- ✓ Emergency stop works immediately
- ✓ Motors hold position when enabled
- ✓ No overheating or unusual noises

## Congratulations!

You now have a working automated polar alignment controller! 

Next: Mount it to your Star Adventurer GTi and enjoy easier polar alignment. 🔭✨

---

**Total Setup Time**: ~30 minutes
**Difficulty**: Intermediate
**Cost**: ~$75-100

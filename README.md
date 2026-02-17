# Star Adventurer GTi - Automated Polar Alignment System

An automated polar alignment system for the Sky-Watcher Star Adventurer GTi telescope mount using stepper motors controlled via Arduino.

## Overview

This system automates the manual polar alignment adjustments on the Star Adventurer GTi by using stepper motors to control:
- **ALT (Altitude)**: Vertical adjustment via front knob
- **AZ (Azimuth)**: Horizontal adjustment via rear thumb screws

## Features

- **Precision Control**: 3200 steps per revolution with 1/16 microstepping
- **Dual Motor Control**: Independent ALT and AZ adjustments
- **USB/Serial Interface**: Control from computer or smartphone (via USB OTG)
- **Speed Adjustment**: Variable speed from 1-2000 steps/second
- **Position Tracking**: Real-time position monitoring
- **Easy Integration**: Can be controlled manually or via astronomy software

## Hardware Requirements

### Electronics Components

| Component | Quantity | Specification | Approx. Cost (USD) |
|-----------|----------|---------------|-------------------|
| Arduino Nano | 1 | ATmega328P, USB | $5-10 |
| TMC2208 Stepper Driver | 3 | V3.0, 256 microsteps | $5-8 each |
| **NEMA 11 Stepper Motor** | **3** | **28mm, 1.8°, 12V, 0.33-0.67A** | **$8-12 each** |
| 12V Power Supply | 1 | 3A minimum | $10-15 |
| USB Cable | 1 | USB-A to Mini/Micro | $3-5 |
| Jumper Wires | 30+ | Dupont connectors | $5 |
| Breadboard (optional) | 1 | For prototyping | $5 |
| Heatsinks | 3 | For TMC2208 drivers | $3 |

**Total Cost**: ~$85-110 USD

**Motor Note**: NEMA 11 (28mm × 28mm) recommended for compact Star Adventurer GTi.  
NEMA 17 (42mm × 42mm) too large and will interfere with telescope mounting.  
Alternative: NEMA 14 (35mm) or remote-mount NEMA 17 away from telescope.

### Mechanical Components (for final build)

| Component | Quantity | Notes |
|-----------|----------|-------|
| GT2 Timing Belt | 2m | 6mm width |
| GT2 Pulleys | 4 | 20 teeth, 5mm bore |
| Motor Brackets | 2 | 3D printed or aluminum |
| Mounting Screws | Various | M3, M4 sizes |
| Flexible Couplers | 2 | 5mm to shaft size |

### Tools Required

- Soldering iron and solder
- Wire strippers
- Small screwdrivers
- Multimeter (for troubleshooting)
- 3D printer (optional, for brackets)

## Wiring Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ARDUINO NANO                              │
│                                                              │
│  D2 (ALT_STEP)  ────────────┬─── STEP (TMC2208 #1)         │
│  D3 (ALT_DIR)   ────────────┼─── DIR  (TMC2208 #1)         │
│  D4 (ALT_EN)    ────────────┼─── EN   (TMC2208 #1)         │
│                             │                                │
│  D5 (AZ_STEP)   ────────────┼─── STEP (TMC2208 #2)         │
│  D6 (AZ_DIR)    ────────────┼─── DIR  (TMC2208 #2)         │
│  D7 (AZ_EN)     ────────────┼─── EN   (TMC2208 #2)         │
│                             │                                │
│  GND ───────────────────────┴─── GND (Both TMC2208)         │
│  VIN (12V) ──────────────────── VM  (Both TMC2208)         │
│                                                              │
│  USB ───────────────────────── Computer                     │
└─────────────────────────────────────────────────────────────┘

TMC2208 Stepper Driver Pinout:
┌──────────────┐
│  EN  DIR  STEP│  ← To Arduino
│  VM  GND  VDD │  ← Power (VM=12V motor power, VDD from Arduino 5V or leave NC)
│  B2  B1      │  ← To Motor Coil B
│  A1  A2      │  ← To Motor Coil A
└──────────────┘

NEMA 11/17 Motor Connections:
- Identify coils with multimeter (resistance test)
- Same connection pattern for both motor sizes
- Typical wire colors:
  * Coil A: Red/Blue (or Red/Yellow)
  * Coil B: Green/Black (or Green/White)
```

### Power Distribution

```
12V Power Supply
├── Arduino VIN (powers Arduino)
├── TMC2208 #1 VM (motor power)
└── TMC2208 #2 VM (motor power)

Ground (Common)
└── Connect all GND pins together
```

## Software Setup

### Prerequisites

1. **Arduino IDE** (version 1.8.x or newer)
   - Download from: https://www.arduino.cc/en/software

2. **Python 3.7+** (for control software)
   - Download from: https://www.python.org/downloads/

3. **Python Package: pyserial**
   ```bash
   pip install pyserial
   ```

### Arduino Firmware Installation

1. Open `arduino/polar_align_controller.ino` in Arduino IDE

2. Select your board:
   - Tools → Board → Arduino Nano
   - Tools → Processor → ATmega328P (or ATmega328P Old Bootloader)

3. Select your COM port:
   - Tools → Port → [Your Arduino Port]

4. Upload the sketch:
   - Click Upload button (→) or Ctrl+U

5. Verify upload:
   - Open Serial Monitor (Tools → Serial Monitor)
   - Set baud rate to 115200
   - You should see "READY" and help text

### Python Software Installation

1. Navigate to the python directory:
   ```bash
   cd polar_align_controller/python
   ```

2. Make the script executable (Linux/Mac):
   ```bash
   chmod +x polar_align_control.py
   ```

3. Run the control software:
   ```bash
   python polar_align_control.py
   ```
   or
   ```bash
   python3 polar_align_control.py
   ```

## TMC2208 Driver Configuration

### Microstepping Settings

The TMC2208 drivers need to be configured for 1/16 microstepping:

**Pin Configuration** (on bottom of driver board):
```
MS1  MS2  CFG1  CFG2  CFG3
[0]  [0]  [0]   [0]   [0]

0 = Not connected (leave floating)
1 = Connect to GND
```

For **1/16 microstepping** (recommended):
- Leave all MS pins disconnected (floating)
- This is the default configuration

### Current Limiting

**IMPORTANT**: Set current limit to prevent motor overheating!

1. **Calculate Vref**:
   ```
   Vref = Motor_Current × 0.5
   
   Example: For 0.4A motor
   Vref = 0.4 × 0.5 = 0.2V
   ```

2. **Adjust Vref**:
   - Connect power to driver
   - Measure voltage between Vref pin and GND
   - Carefully turn potentiometer until Vref matches calculated value
   - **Turn slowly** - small adjustments make big differences!

### Driver Installation

1. **Add heatsinks** to TMC2208 chips
2. **Orient correctly** - check pinout labels
3. **Connect power** (12V) BEFORE connecting motors
4. **Test with multimeter** before connecting Arduino

## Usage Guide

### Starting the System

1. **Power on** the 12V supply
2. **Connect** Arduino via USB to computer
3. **Run** the Python control software
4. **Enable motors** with '+' command
5. **Start adjusting** using keyboard commands

### Control Commands

#### Altitude Controls (Up/Down)
- `Q` - Fine UP (10 steps)
- `W` - Small UP (50 steps)
- `E` - Medium UP (200 steps)
- `R` - Large UP (800 steps)
- `A` - Fine DOWN (10 steps)
- `S` - Small DOWN (50 steps)
- `D` - Medium DOWN (200 steps)
- `F` - Large DOWN (800 steps)

#### Azimuth Controls (Left/Right)
- `T` - Fine CCW (10 steps)
- `Y` - Small CCW (50 steps)
- `U` - Medium CCW (200 steps)
- `I` - Large CCW (800 steps)
- `G` - Fine CW (10 steps)
- `H` - Small CW (50 steps)
- `J` - Medium CW (200 steps)
- `K` - Large CW (800 steps)

#### Utility Commands
- `P` - Display current position
- `0` - Reset position to 0,0
- `V` - Set motor speed
- `X` - Emergency stop
- `+` - Enable motors
- `-` - Disable motors
- `?` - Show status
- `M` - Show menu
- `QUIT` - Exit program

### Typical Polar Alignment Workflow

1. **Set up mount** manually (rough polar alignment)
2. **Enable motors** using control software
3. **Start polar alignment** in SynScan app
4. **View Polaris** in polar scope
5. **Adjust ALT/AZ** with this system to position Polaris
6. **Fine-tune** until Polaris is in correct position
7. **Disable motors** to lock position
8. **Begin observing/imaging**

## Mechanical Integration

### Prototype Setup (Belt Drive)

**For ALT (Altitude Knob):**

1. Attach motor to mount using bracket
2. Mount pulley on motor shaft (5mm)
3. Mount pulley on altitude knob shaft
4. Connect with GT2 timing belt
5. Adjust tension (should be snug but not too tight)

**Recommended Gear Ratio**: 3:1 or 5:1
- Motor pulley: 20 teeth
- Knob pulley: 60 teeth (3:1) or 100 teeth (5:1)

**For AZ (Azimuth Screws):**

**Option 1: Dual Motor (Simpler)**
- One motor per screw
- Direct coupling or belt drive
- Software coordinates opposing movements

**Option 2: Differential Platform (More elegant)**
- Single motor with worm gear
- Platform sits between mount and tripod
- Rotates entire mount for AZ

## Calibration

### Step Calibration

1. **Measure actual movement**:
   - Mark starting position
   - Send 3200 steps (1 full revolution with 1/16 microstepping)
   - Measure actual rotation

2. **Calculate steps per degree**:
   ```
   If using 3:1 gear ratio:
   3200 steps = 1/3 revolution of knob
   3200 steps = 120°
   Steps per degree = 3200 / 120 = 26.67 steps/degree
   ```

3. **Fine-tune** in software if needed

### Speed Calibration

Start with conservative speeds and increase gradually:
- **Initial testing**: 200 steps/sec
- **Normal operation**: 800 steps/sec
- **Fast slewing**: 1500-2000 steps/sec

## Troubleshooting

### Motors Not Moving

1. **Check connections**:
   - Verify wiring against diagram
   - Test continuity with multimeter
   - Check for loose connections

2. **Check power**:
   - Measure 12V at power supply
   - Measure voltage at Arduino VIN
   - Check TMC2208 VM pins

3. **Check drivers**:
   - Verify Vref setting
   - Check for overheating
   - Ensure heatsinks attached

4. **Check enable state**:
   - Motors should be enabled (`+` command)
   - EN pin should be LOW (enabled)

### Motors Stuttering or Skipping

1. **Reduce speed**: Use `V` command to lower speed
2. **Check current limit**: Vref may be too low
3. **Reduce load**: Check for mechanical binding
4. **Check belt tension**: Should not be too tight

### Serial Communication Errors

1. **Check port**: May have changed after reconnecting
2. **Check baud rate**: Must be 115200
3. **Check cable**: Try different USB cable
4. **Reset Arduino**: Unplug and replug USB

### Position Drift

1. **Check microstepping**: Ensure drivers configured correctly
2. **Check belt tension**: May be slipping
3. **Enable holding torque**: Motors should stay energized
4. **Check for backlash**: Mechanical play in couplings

## Safety Notes

⚠️ **IMPORTANT SAFETY INFORMATION**

1. **Never exceed payload capacity** (5kg / 11 lbs)
2. **Always use counterweight** before attaching telescope
3. **Disable motors** when manually adjusting
4. **Emergency stop**: Press `X` or unplug power
5. **Don't force movement**: If motors stall, reduce load
6. **Monitor temperature**: Drivers and motors should not be hot to touch
7. **Secure all connections**: Prevent shorts and disconnections
8. **Proper grounding**: Use grounded power supply

## Advanced Features (Future Development)

### Plate Solving Integration

Integrate with plate solving software for automated alignment:

1. **Capture image** with camera
2. **Plate solve** to get current pointing
3. **Calculate error** from celestial pole
4. **Send corrections** to this controller
5. **Re-image and iterate** until aligned

Compatible with:
- ASTAP
- Astrometry.net
- PlateSolver
- NINA (N.I.N.A.)
- SGP (Sequence Generator Pro)

### ASCOM/INDI Driver

Future development could include:
- ASCOM driver for Windows
- INDI driver for Linux
- Direct integration with:
  - PHD2 for autoguiding
  - SharpCap for polar alignment
  - APT (AstroPhotography Tool)

## File Structure

```
polar_align_controller/
│
├── arduino/
│   └── polar_align_controller.ino    # Arduino firmware
│
├── python/
│   └── polar_align_control.py        # Python control software
│
├── mechanical/
│   ├── README.md                      # Mechanical build guide
│   └── (STL files for 3D printed parts - to be added)
│
├── docs/
│   ├── wiring_diagram.pdf
│   ├── calibration_guide.md
│   └── integration_guide.md
│
└── README.md                          # This file
```

## Support and Contributions

This is an open-source project. Contributions welcome!

**Future Enhancements:**
- GUI control interface (tkinter or PyQt)
- Mobile app (Android/iOS)
- 3D printable mounting brackets
- ASCOM driver
- Automated plate-solve alignment
- Configuration file for different gear ratios

## License

This project is provided as-is for educational and personal use.

## Acknowledgments

- Sky-Watcher for the Star Adventurer GTi platform
- Arduino and Python communities
- TMC2208 driver documentation from Trinamic

## Version History

- **v1.0** (2024) - Initial release
  - Arduino firmware with dual motor control
  - Python CLI control interface
  - Basic positioning and speed control

---

**Built by astronomers, for astronomers** 🔭✨

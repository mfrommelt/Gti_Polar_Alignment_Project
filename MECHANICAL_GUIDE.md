# Mechanical Integration Guide

Detailed guide for mounting motors to your Star Adventurer GTi

## Overview

This guide covers three mounting approaches:
1. **Prototype Setup** - Quick test with hand-held motors
2. **Belt Drive System** - Production-ready ALT control
3. **Azimuth Control Options** - Two approaches for AZ

---

## Understanding the Star Adventurer GTi Adjustment Mechanisms

### Altitude (ALT) Adjustment
- **Location**: Front of mount
- **Control**: Single knob
- **Rotation**: ~270° total travel
- **Thread pitch**: Unknown (needs measurement)
- **Torque required**: Low (finger tight)

### Azimuth (AZ) Adjustment  
- **Location**: Rear of mount
- **Control**: Two opposing thumb screws
- **Function**: Push-pull differential adjustment
- **Rotation**: Screws rotate, mount rotates on base
- **Torque required**: Very low

---

## Phase 1: Prototype Setup (0 Mechanical Work)

### Purpose
Test electronics before committing to mechanical design.

### Method
**Hand-Held Test**

1. **Power on** and connect system
2. **Hold motor shaft** by hand near knob
3. **Run motors** and observe rotation
4. **Verify direction** and step count
5. **Feel torque** to ensure adequate power

**Quick Coupling Test**
- Use rubber tubing as temporary coupler
- Press motor shaft against knob shaft
- Run motor and observe movement
- Tests concept without permanent mounting

### Measurements to Take
```
ALT Knob:
- Shaft diameter: _____ mm
- Knob rotation for 1° altitude: _____ degrees
- Total rotation range: _____ degrees
- Knob clearance space: _____ mm

AZ Screws:
- Screw head type: _____
- Screw diameter: _____ mm  
- Thread pitch: _____ mm
- Rotation for 1° azimuth: _____ degrees
```

---

## Phase 2: Belt Drive System for ALT

### Recommended Approach
**3:1 Gear Reduction via Belt Drive**

#### Components Needed
- NEMA 17 motor
- Motor mounting bracket
- 20-tooth GT2 pulley (motor)
- 60-tooth GT2 pulley (knob) 
- GT2 timing belt, 6mm wide
- Shaft coupler (pulley to knob shaft)

#### Advantages
- Simple, reliable
- Easy to adjust tension
- No backlash
- Silent operation
- Easy to disconnect

### Mounting Options

#### Option 1: Side Mount Bracket

**Design**:
```
      [Motor]
         |
    [20T Pulley]
         |
    [GT2 Belt]───┐
                 │
                 │
            [60T Pulley]
                 |
            [ALT Knob]
```

**Bracket Requirements**:
- Mount to side of Star Adventurer GTi
- Positions motor parallel to ALT knob shaft
- Allows belt to run perpendicular to both shafts
- Adjustable belt tension

**Materials**:
- 3D printed PLA/PETG (simplest)
- Aluminum plate, 3mm thick (more rigid)
- Steel L-bracket (strongest)

**3D Printable Design** (STL file to be added):
```
Features:
- NEMA 17 mounting holes (31mm spacing)
- Attachment to mount via existing holes
- Belt tension adjustment slots
- ~100mm motor offset from knob
```

#### Option 2: Top Mount Bracket

**Design**: Motor mounts above altitude assembly
- More compact
- Better weight distribution
- Requires precise alignment

#### Option 3: Rear Mount

**Design**: Motor behind mount head
- Uses longer belt
- Easier access
- More flexible positioning

### Belt Drive Calculations

**Gear Ratio Selection**:
```
1:1 ratio (direct)
- Pros: Simple, fast movement
- Cons: Less precision, more steps needed

3:1 ratio (recommended)
- 20T motor : 60T knob
- Pros: Good precision, adequate speed
- Motor steps = 3 × knob rotation
- Example: 3200 motor steps = 1 full knob rotation

5:1 ratio (high precision)
- 20T motor : 100T knob  
- Pros: Maximum precision
- Cons: Slower, larger pulley required
```

**Belt Length Calculation**:
```
C = Center distance between shafts
P1 = Pitch diameter of motor pulley
P2 = Pitch diameter of knob pulley

Belt length (mm) = 2C + 1.57(P1 + P2) + ((P2-P1)²)/(4C)

Example with 100mm center distance:
P1 = 12.7mm (20T GT2)
P2 = 38.2mm (60T GT2)  
Belt ≈ 280mm

Always buy longer and cut to size!
```

### Installation Steps

1. **Attach pulley to motor shaft**
   - Slide on pulley
   - Tighten set screw against flat of shaft
   - Verify secure

2. **Attach pulley to ALT knob shaft**
   - May need to fabricate coupler
   - Options:
     * Direct mount (drill knob, tap threads)
     * Flexible coupler + extension shaft
     * Friction coupling

3. **Mount motor bracket**
   - Find suitable attachment point on mount
   - Use existing holes if possible
   - Add rubber padding to reduce vibration

4. **Install belt**
   - Loop around both pulleys
   - Adjust bracket position for tension
   - Belt should not slip but not too tight
   - Test: Twist 90° should be possible with moderate force

5. **Test movement**
   - Power on
   - Move motor slowly
   - Verify knob rotates correctly
   - Check for belt slipping
   - Listen for unusual noises

### Backlash Compensation

**Belt systems typically have minimal backlash, but:**

1. **Ensure proper tension**
   - Too loose = slipping
   - Too tight = binding

2. **Software compensation**
   - Always approach target from same direction
   - Add small "overrun and back up" to final position

3. **Use spring-loaded tensioner** (advanced)
   - Maintains constant tension
   - Compensates for temperature changes

---

## Phase 3: Azimuth Control Options

### Option A: Dual Motor Direct Drive

**Concept**: One motor per screw

#### Advantages
- Simple mechanical design
- Direct control
- No additional hardware needed
- Easy to implement

#### Challenges
- Requires precise synchronization
- Two motors = more power consumption
- Opposing forces must balance

#### Implementation

**Motor Mounting**:
```
[Motor 1]──[Coupler]──[AZ Screw 1]
                           
           [Mount Head]

[Motor 2]──[Coupler]──[AZ Screw 2]
```

**Software Control**:
```python
def move_azimuth_dual(steps):
    if steps > 0:  # Move right
        motor_1.forward(steps)   # Tighten screw 1
        motor_2.backward(steps)  # Loosen screw 2
    else:  # Move left
        motor_1.backward(abs(steps))
        motor_2.forward(abs(steps))
```

**Coupling Options**:
1. **Direct coupling**: Replace screw head with motor shaft
2. **Flexible coupler**: Connect motor shaft to screw
3. **Belt drive**: Small pulley on each screw

**Calibration Required**:
- Balance point (equal tension on both screws)
- Step calibration (degrees per step)
- Speed matching between motors

---

### Option B: Differential Platform (Advanced)

**Concept**: Single motor rotates entire mount on base

#### Advantages
- Single motor = simpler control
- More precise
- No synchronization issues
- Can be very elegant

#### Challenges
- More complex mechanical design
- Requires precision machining
- More expensive
- Needs to support full mount weight

#### Design

**Worm Gear Drive**:
```
                [Motor]
                   |
              [Worm Gear]
                   |
         [Worm Wheel (360°)]
                   |
            [Rotating Platform]
                   |
          [Stationary Tripod Base]
```

**Specifications**:
- Worm ratio: 90:1 or 120:1 (high precision)
- Platform bearing: Lazy Susan type, 6" diameter
- Platform material: Aluminum, 6mm thick

**Components**:
1. **Worm gear set** (90:1 ratio)
   - Worm: Connected to motor
   - Wheel: Mounted to platform
   
2. **Rotating platform**
   - Sits between mount and tripod
   - Aluminum or steel
   - ~150mm diameter
   
3. **Bearing system**
   - Lazy Susan bearing OR
   - Ball bearing race OR
   - Teflon pads

4. **Motor mount**
   - Positioned tangent to platform
   - Worm meshes with wheel

**Advantages of Worm Drive**:
- Self-locking (holds position without power)
- Very high precision
- Smooth motion
- Can handle high loads

**Platform Design Considerations**:
- Must support mount weight (2.6kg) + telescope (up to 5kg)
- Center of gravity should be over platform center
- Platform must clear tripod legs
- Access to mount controls

#### Commercial Alternative

**Look for**: 
- Motorized camera turntable/slider
- Lazy Susan bearing, 6-8" diameter
- May already have motor mount
- Adapt to hold Star Adventurer GTi

---

## Material Selection Guide

### 3D Printing

**PLA**:
- Pros: Easy to print, rigid, inexpensive
- Cons: Can warp in heat, brittle
- Use for: Indoor use, prototypes

**PETG**:
- Pros: Strong, flexible, heat resistant
- Cons: Harder to print, slight warping
- Use for: Field use, production parts

**ABS**:
- Pros: Very strong, heat resistant
- Cons: Difficult to print, warping, fumes
- Use for: Heavy-duty applications

**Print Settings**:
- Layer height: 0.2mm
- Infill: 50-100% for structural parts
- Walls: 3-4 perimeters
- Top/bottom: 5-6 layers

### Metal Fabrication

**Aluminum 6061**:
- Easy to machine
- Lightweight
- Good rigidity
- Thickness: 3-5mm for brackets

**Steel**:
- Very strong
- Heavier
- May require powder coating (rust prevention)
- Thickness: 2-3mm for brackets

### Hardware

**Screws**:
- M3: Small assemblies, plastic
- M4: Standard, most brackets
- M5: Heavy-duty, high load

**Washers**: Always use with plastic
**Loctite**: Thread locker for vibration resistance

---

## Assembly Best Practices

### Alignment

1. **Use alignment jigs** when possible
2. **Check perpendicularity** with square
3. **Test fit before drilling** permanent holes
4. **Mark everything** before assembly

### Vibration Reduction

1. **Use rubber washers** between motor and bracket
2. **Add dampening material** to bracket
3. **Ensure rigid mounting** (no flexing)
4. **Balance rotating parts** (pulleys)

### Cable Management

1. **Strain relief** at all connections
2. **Spiral wrap** for neat appearance
3. **Allow slack** for mount movement
4. **Secure to mount** with zip ties/velcro

---

## Testing & Calibration

### Initial Tests

**No Load Test**:
1. Motors installed but not coupled
2. Run through full speed range
3. Listen for unusual sounds
4. Check for vibration
5. Verify holding torque

**Light Load Test**:
1. Couple to mount (no telescope)
2. Test full range of motion
3. Verify no binding
4. Check belt tension
5. Measure actual degrees of movement

**Full Load Test**:
1. Add counterweight
2. Add telescope
3. Test at various positions
4. Check for slipping
5. Monitor motor temperature

### Calibration Procedure

**Step 1: Measure Gear Ratio**
```
1. Mark starting position on knob
2. Send 3200 motor steps (1 full rotation)
3. Measure actual knob rotation
4. Calculate: Steps per degree = 3200 / measured_degrees
```

**Step 2: Measure Total Range**
```
1. Move to minimum ALT position
2. Reset position counter
3. Move to maximum ALT position
4. Record total steps
5. Verify with physical measurement
```

**Step 3: Set Speed Limits**
```
1. Start at low speed (200 steps/sec)
2. Increase until motor starts skipping
3. Use 70% of maximum as safe speed
4. Set this in software
```

**Step 4: Backlash Measurement**
```
1. Move to position, note reading
2. Move 100 steps away
3. Return to original position
4. Measure difference (backlash)
5. Implement compensation if >10 steps
```

---

## Advanced Features

### Limit Switches (Optional)

Add mechanical limit switches to prevent over-rotation:

**Hardware**:
- 2x microswitch per axis
- Mounting brackets
- Wire to Arduino interrupt pins

**Software**:
- Emergency stop on switch trigger
- Soft limits in code
- Homing routine on startup

### Position Encoding (Optional)

Add absolute encoders for position feedback:

**Options**:
- Magnetic encoders (AS5600)
- Optical encoders
- Hall effect sensors

**Benefits**:
- Know exact position after power loss
- Closed-loop control
- Error detection

### Motorized Focus (Future)

Use same system to automate telescope focus:

**Required**:
- Small NEMA 14 or 11 motor
- Additional TMC2208 driver
- Focus coupling
- Software extension

---

## Troubleshooting Mechanical Issues

### Belt Slipping
- Increase tension
- Clean belt and pulleys
- Check pulley teeth not worn
- Verify set screws tight

### Excessive Noise
- Reduce speed
- Check for binding
- Verify proper belt tension
- Add vibration dampening

### Binding/Sticking
- Check alignment
- Lubricate if appropriate
- Verify no interference
- Check for debris

### Inconsistent Movement
- Check belt tension
- Verify coupling tight
- Look for loose screws
- Check for flex in brackets

---

## Safety Notes

⚠️ **CRITICAL SAFETY**

1. **Never exceed mount capacity** (5kg payload)
2. **Always use counterweight** before attaching telescope
3. **Disable motors** before manual adjustment
4. **Secure all connections** to prevent detachment
5. **Monitor first operations** closely
6. **Emergency stop tested** and working
7. **Clear workspace** of trip hazards

---

## Design Files Repository

Coming soon:
- 3D printable STL files
- CAD models (STEP format)
- Technical drawings
- Bill of materials
- Assembly instructions

---

## Community Contributions

Share your build!
- Photos of your setup
- Modifications and improvements
- Calibration data for your mount
- Alternative mounting solutions

---

**Good luck with your mechanical build!** 🔧🔭

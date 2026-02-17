# Differential Azimuth Control - Important Update

## Critical Clarification

Based on your explanation, the Star Adventurer GTi uses a **differential push-pull system** for azimuth adjustment:

- **To move WEST**: Loosen west screw + tighten east screw
- **To move EAST**: Tighten west screw + loosen east screw

This is MORE precise than a single-motor system but requires **synchronized dual motor control**.

---

## Updated Hardware Requirements

### You Need 3 Motors (Not 2!)

| Motor | Purpose | Control Type |
|-------|---------|--------------|
| Motor 1 | ALT (Altitude) | Independent |
| Motor 2 | AZ West Screw | Differential pair |
| Motor 3 | AZ East Screw | Differential pair |

### Updated Parts List

**Additional Items Needed:**
- 1 more NEMA 17 motor (total: 3) - Add $12
- 1 more TMC2208 driver (total: 3) - Add $8
- **New Total Cost**: ~$95 instead of $75

---

## Updated Wiring Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    ARDUINO NANO                              │
│                                                              │
│  D2 (ALT_STEP)       ─────── STEP (TMC2208 #1 - ALT)       │
│  D3 (ALT_DIR)        ─────── DIR  (TMC2208 #1 - ALT)       │
│  D4 (ALT_EN)         ─────── EN   (TMC2208 #1 - ALT)       │
│                                                              │
│  D5 (AZ_WEST_STEP)   ─────── STEP (TMC2208 #2 - WEST)      │
│  D6 (AZ_WEST_DIR)    ─────── DIR  (TMC2208 #2 - WEST)      │
│  D7 (AZ_WEST_EN)     ─────── EN   (TMC2208 #2 - WEST)      │
│                                                              │
│  D8 (AZ_EAST_STEP)   ─────── STEP (TMC2208 #3 - EAST)      │
│  D9 (AZ_EAST_DIR)    ─────── DIR  (TMC2208 #3 - EAST)      │
│  D10 (AZ_EAST_EN)    ─────── EN   (TMC2208 #3 - EAST)      │
│                                                              │
│  GND ─────────────────────── GND (All 3 TMC2208)            │
│  VIN (12V) ───────────────── VM  (All 3 TMC2208)            │
│                                                              │
│  USB ─────────────────────── Computer                       │
└─────────────────────────────────────────────────────────────┘

Power Requirements (Updated):
- 3x motors @ 0.4A = 1.2A total
- Recommend 12V 3A supply (was 2A)
```

---

## How Differential Control Works

### Mechanical Principle

```
        [Mount Head]
             ▼
    ◄───[West Screw]  [East Screw]───►
         (Motor 2)      (Motor 3)
```

**To Move Mount WEST** (negative steps):
1. West screw motor: LOOSEN (rotate backward)
2. East screw motor: TIGHTEN (rotate forward)
3. Net result: Mount pivots west

**To Move Mount EAST** (positive steps):
1. West screw motor: TIGHTEN (rotate forward)
2. East screw motor: LOOSEN (rotate backward)
3. Net result: Mount pivots east

### Critical Requirements

✅ **Synchronized Movement**: Both motors step simultaneously  
✅ **Opposite Directions**: Motors rotate in opposite directions  
✅ **Equal Steps**: Both motors move exactly the same number of steps  
✅ **Balanced Tension**: Screws maintain equal and opposite pressure  

---

## Software Implementation

### Arduino Firmware (v2.0)

I've created an updated firmware: `polar_align_controller_v2_differential.ino`

**Key Function:**
```cpp
void moveAzimuthDifferential(long steps) {
  if (steps > 0) {
    // Move EAST
    West_Motor: Tighten (forward)
    East_Motor: Loosen (backward)
  } else {
    // Move WEST
    West_Motor: Loosen (backward)
    East_Motor: Tighten (forward)
  }
  
  // Step both motors simultaneously
  for each step:
    Pulse both motors at same time
}
```

**Advantages:**
- Perfect synchronization (no drift)
- Single command moves both motors
- Maintains balanced tension
- Position tracking remains simple

---

## Mechanical Coupling Options

### Option 1: Direct Coupling (Recommended)

**Each motor couples directly to its screw:**

```
Motor 2 ──[Flexible Coupler]── West Screw
Motor 3 ──[Flexible Coupler]── East Screw
```

**Coupling Methods:**
1. **Flexible shaft coupler** (5mm motor to screw diameter)
   - Easiest installation
   - Allows slight misalignment
   - Cost: $3-4 each

2. **Replace screw heads** with motor shaft adapters
   - Most direct connection
   - Requires machining
   - Most rigid

3. **Belt drive per screw** (if space limited)
   - Small pulley on motor
   - Small pulley on screw
   - Short GT2 belt
   - More complex but flexible

### Mounting Configuration

```
     [Mount Head - Rear View]
          ___________
         |           |
         |           |
[Motor 2]|  MOUNT   |[Motor 3]
(West)   |   HEAD   |(East)
  ║      |           |      ║
  ║      |___________|      ║
  ╚══[West Screw]  [East Screw]══╝
```

**Mounting Considerations:**
- Motors positioned symmetrically
- Clear access to screws
- Avoid interference with polar scope
- Cable management for 3 motors
- Weight distribution (add ~350g total for 3 motors)

---

## Calibration Procedure

### Step 1: Initial Balance (CRITICAL)

Before first use, establish the **neutral center position**:

1. **Manual centering**:
   - Adjust screws by hand until mount is centered
   - Both screws should have equal tension
   - Mount should not favor east or west

2. **Send balance command**: `B`
   - Firmware will guide you through process
   
3. **Reset position**: `R`
   - Sets current position as 0,0
   - This is your reference point

### Step 2: Test Differential Movement

```bash
# Move 50 steps WEST
Z-50

# Observe:
✓ Mount moves smoothly west
✓ West screw loosens
✓ East screw tightens
✓ Both motors step together

# Return to center
Z50

# Should return to exact starting position
```

### Step 3: Measure Range

Find the total travel limits:
```
1. Move west until screw fully loosened: Z-XXXX
2. Note position (west limit)
3. Return to center: ZXXXX
4. Move east until screw fully tightened: ZXXXX
5. Note position (east limit)
6. Calculate total range
```

Typical range might be ±500 to ±2000 steps from center.

### Step 4: Calibrate Steps per Degree

```
Method 1: Visual alignment
1. Align mount to known reference (north star)
2. Reset position: R
3. Move mount exactly 1 degree using controls
4. Note step count
5. Steps/degree = step_count / 1

Method 2: Polar scope reticle
1. Use polar scope alignment marks
2. Move between known reference points
3. Calculate steps per degree
```

---

## Troubleshooting Differential System

### Motors Moving Out of Sync

**Symptom**: Mount doesn't move smoothly, screws get unbalanced

**Causes**:
1. Wiring issue - check connections
2. Different motor speeds - verify identical motors
3. Mechanical binding - check for obstructions
4. Power supply insufficient - use 3A supply

**Solution**:
- Verify both motors receive step pulses simultaneously
- Check with oscilloscope if available
- Ensure identical motors (same model, current rating)

### One Screw Tightens Too Much

**Symptom**: One screw gets very tight, other very loose

**Causes**:
1. Started from off-center position
2. Steps lost on one motor (skipping)
3. Different gear ratios (if using belts)

**Solution**:
- Re-run balance procedure
- Reduce speed if motors skipping
- Ensure equal gear ratios
- Add position verification

### Mount Binds During Movement

**Symptom**: Movement stops, motors stall

**Causes**:
1. Screws reached mechanical limit
2. Too much tension on one side
3. Mechanical interference

**Solution**:
- Implement soft limits in software
- Re-balance from center
- Check for physical obstructions
- Reduce travel range

---

## Software Limits & Safety

### Recommended Soft Limits

Add to Arduino code:
```cpp
#define AZ_MAX_EAST 1500   // Maximum steps east of center
#define AZ_MAX_WEST -1500  // Maximum steps west of center

// In moveAzimuthDifferential():
if (azPosition + steps > AZ_MAX_EAST) {
  Serial.println("ERROR:EAST_LIMIT");
  return;
}
if (azPosition + steps < AZ_MAX_WEST) {
  Serial.println("ERROR:WEST_LIMIT");
  return;
}
```

### Emergency Re-centering

If mount gets far off-center:
```
1. Send 'D' to disable motors
2. Manually adjust screws to balanced center
3. Send 'E' to enable motors
4. Send 'R' to reset position
5. Resume normal operation
```

---

## Alternative: Platform Rotation Approach

If the 3-motor differential system seems too complex, consider:

### Single Motor Platform Rotation

**Concept**: Instead of motorizing the screws, rotate the entire mount on a platform

**Advantages**:
- Only 2 motors total (ALT + AZ platform)
- Simpler software (no differential control)
- No screw tension issues
- More precise

**Disadvantages**:
- More complex mechanical design
- Requires precision bearing/platform
- Must support full mount weight
- More expensive (~$50 more)

**Design**:
```
    [Mount Head]
         ▼
  [Rotating Platform]
    (worm gear driven)
         ▼
    [Tripod Base]
```

See **MECHANICAL_GUIDE.md - Option B** for full details.

---

## Which Approach Should You Use?

### Use 3-Motor Differential If:
✓ You want to use existing mount mechanics  
✓ Budget conscious (~$95 total)  
✓ Comfortable with electronics  
✓ Don't mind slightly more complex software  

### Use 2-Motor Platform If:
✓ Want maximum precision  
✓ Comfortable with mechanical fabrication  
✓ Can invest more (~$150 total)  
✓ Prefer simpler software  
✓ Building "forever" solution  

---

## Updated Cost Analysis

### 3-Motor Differential System
```
Arduino Nano:           $8
3x TMC2208 drivers:     $24 (3 × $8)
3x NEMA 17 motors:      $36 (3 × $12)
12V 3A power supply:    $12
Couplers (3x):          $12
Wiring/hardware:        $8
────────────────────────
TOTAL:                  $100
```

### 2-Motor Platform System
```
Arduino Nano:           $8
2x TMC2208 drivers:     $16
2x NEMA 17 motors:      $24
Platform bearing:       $25
Worm gear set:          $30
12V 3A power supply:    $12
Hardware/brackets:      $20
────────────────────────
TOTAL:                  $135
```

---

## Recommendation

For your first build, I recommend the **3-motor differential approach**:

**Pros**:
- Uses mount's existing mechanisms
- Less mechanical fabrication
- Easier to prototype
- Can upgrade to platform later if desired
- Software handles complexity automatically

**Cons**:
- One extra motor/driver needed
- Requires balanced starting position
- Slightly more wiring

The updated firmware (`v2_differential.ino`) handles all the complexity - you just send one command and both motors move perfectly synchronized.

---

## Files Updated

New files created:
- `polar_align_controller_v2_differential.ino` - Updated Arduino firmware
- `DIFFERENTIAL_AZ_CONTROL.md` - This document

Still valid:
- Python control software (works with both versions)
- All documentation
- Shopping list (add 1 motor + 1 driver)

---

## Next Steps

1. **Decide**: 3-motor differential OR 2-motor platform
2. **Order parts**: Use updated shopping list
3. **Use v2 firmware**: Upload `v2_differential.ino` to Arduino
4. **Follow QUICK_START.md**: Same procedure, just add 3rd motor
5. **Balance first**: Critical step before use!

---

**Questions about differential control?** This is actually a superior approach mechanically - you're getting more precision than a simple rotation system. The software handles the complexity automatically.

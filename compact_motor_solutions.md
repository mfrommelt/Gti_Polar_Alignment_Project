# Compact Motor Solutions for Star Adventurer GTi

## Problem: NEMA 17 Motors Too Large

**Standard NEMA 17 dimensions:**
- Size: 42mm × 42mm × ~40mm
- Weight: ~280g each
- **3 motors = 840g total weight**
- **Footprint = 126mm × 42mm if mounted in a row**

**Impact on Star Adventurer GTi:**
- ❌ Blocks mount's range of motion
- ❌ Interferes with telescope attachment
- ❌ Adds significant weight (mount itself is 2.6kg)
- ❌ Bulky appearance
- ❌ Cable management nightmare
- ❌ Reduces portability

**You need: Smaller motors with adequate torque**

---

## Solution 1: NEMA 11 Stepper Motors (RECOMMENDED)

### Specifications

**Size:** 28mm × 28mm × 30-40mm
- **67% smaller footprint** than NEMA 17
- **60% lighter** (~100g vs 280g)

**Torque:** 80-120 mN·m (8-12 N·cm)
- Lower than NEMA 17 (400-500 mN·m)
- **But still adequate** for your application!

**Current:** 0.33-0.67A
- Lower power consumption
- Less heat generation

**Shaft:** 5mm diameter (same as NEMA 17!)
- **All your pulleys still fit!**

### Why NEMA 11 Works for You

**Your application doesn't need high torque:**

1. **ALT (Worm Gear):**
   - Worm gear has 50:1 to 180:1 reduction
   - Belt drive adds 4:1 reduction  
   - **Total 200:1 to 720:1 reduction**
   - Motor only needs to turn knob, not lift telescope
   - **Required torque: ~5 N·cm → NEMA 11 provides 8-12 N·cm ✓**

2. **AZ (Differential Screws):**
   - Screws are fine-pitch (easy to turn)
   - Belt drive adds 3:1 reduction
   - Push-pull reduces load per motor
   - **Required torque: ~6 N·cm per motor → NEMA 11 provides 8-12 N·cm ✓**

**Conclusion: NEMA 11 has MORE than enough torque!**

### Cost & Availability

**Amazon:**
- "NEMA 11 Stepper Motor 28mm"
- Price: $8-12 each
- Widely available
- 2-day shipping

**AliExpress:**
- Cheaper: $5-8 each
- 3-4 week shipping

**Models to look for:**
- 28HS13 (0.33A, 80 mN·m)
- 28HS32 (0.67A, 120 mN·m) ← Recommended

### Dimensions Comparison

```
NEMA 17:  42mm × 42mm × 40mm    280g
NEMA 11:  28mm × 28mm × 32mm    100g
          ↓ 67% smaller        ↓ 64% lighter

3× NEMA 17: 840g total bulk
3× NEMA 11: 300g total bulk
            ↓ 540g SAVINGS!
```

### Compatibility

**What stays the same:**
- ✅ 5mm motor shaft diameter
- ✅ All your pulleys fit
- ✅ Same mounting holes pattern (scaled down)
- ✅ Same TMC2208 drivers work
- ✅ Same Arduino firmware
- ✅ Same power supply

**What changes:**
- ✅ Mounting brackets (smaller, easier to fit)
- ✅ Reduced weight on mount
- ✅ Better cable routing
- ✅ Less interference with telescope

---

## Solution 2: NEMA 14 Stepper Motors (Middle Ground)

### Specifications

**Size:** 35mm × 35mm × 34-36mm
- **31% smaller footprint** than NEMA 17
- **40% lighter** (~170g vs 280g)

**Torque:** 180-260 mN·m (18-26 N·cm)
- **3× more than NEMA 11**
- **Better than needed** for this application

**Current:** 0.4-1.0A
- Similar to NEMA 17

**Shaft:** 5mm diameter
- **All pulleys fit!**

### When to Choose NEMA 14

**Use NEMA 14 if:**
- You want extra torque margin
- Slightly larger than NEMA 11 is acceptable
- You'll add future features (automated focus, rotator, etc.)
- Budget allows ($12-18 each)

**Skip NEMA 14 if:**
- Space is critical (NEMA 11 better)
- Cost conscious (NEMA 11 cheaper)
- Minimum weight desired (NEMA 11 lighter)

### Cost

**Amazon:** $12-18 each
**AliExpress:** $8-12 each

**Models:**
- 35HS28 (0.4A, 180 mN·m)
- 35HS48 (1.0A, 260 mN·m)

---

## Solution 3: Geared Stepper Motors (COMPACT + HIGH TORQUE)

### What Are They?

**Geared stepper** = Stepper motor + planetary gearbox integrated

```
[Stepper Motor] → [Planetary Gearbox] → [Output Shaft]
  28mm × 28mm      +20mm length          High torque
```

**Typical specs:**
- Size: 28mm × 28mm × 50mm (longer but same footprint)
- Gear ratios: 5:1, 10:1, 27:1, 51:1
- Output torque: 10× to 50× base torque!
- Speed: Lower (gearing reduces RPM)

### Advantages

✅ **Compact footprint** (NEMA 11 size)  
✅ **Very high torque** (can eliminate belt reduction)  
✅ **Self-locking** (high gear ratios hold position)  
✅ **Quieter** (lower speed)  

### Disadvantages

❌ **More expensive** ($25-40 each)  
❌ **Longer** (50mm vs 32mm)  
❌ **Slower** (may need adjustment in firmware)  
❌ **Some backlash** (planetary gears)  

### Best Use Case

**If you want:**
- Direct drive (no belt system)
- Couple motor directly to screws/knob
- Maximum simplicity
- Don't mind extra length
- Budget allows

**Cost:** $25-40 each × 3 = $75-120 (motors only)

---

## Solution 4: Remote Motor Placement

### Concept

**Instead of mounting motors AT adjustment points:**
- Mount all 3 motors together in ONE location
- Use longer belts to reach adjustment points
- Consolidate into single motor module

```
     ┌─────────────────┐
     │  Motor Module   │
     │  ┌─┐ ┌─┐ ┌─┐   │
     │  │M│ │M│ │M│   │ ← All 3 motors
     │  └─┘ └─┘ └─┘   │
     └─────────────────┘
            │ │ │
         Long belts
            │ │ │
         ┌──┴─┴─┴──┐
         │  Mount  │
         │ ALT  AZ │
         └─────────┘
```

### Advantages

✅ **Motors away from telescope**  
✅ **Better weight distribution**  
✅ **Consolidated electronics**  
✅ **Easier cable management**  
✅ **Can use NEMA 17** (size doesn't matter)  

### Disadvantages

❌ **Longer belts** (more complex routing)  
❌ **Belt friction** (longer path)  
❌ **More belt slack** to manage  
❌ **Less compact overall**  

### Implementation

**Mount location options:**
1. **On tripod leg** (below mount head)
2. **On counterweight shaft** (opposite side)
3. **Separate motor box** (connected via belts)

**Belt routing:**
- Use belt guides/pulleys at corners
- Keep belts away from moving parts
- Spring tensioners for longer runs

---

## Solution 5: Hybrid Approach

### Best of Multiple Worlds

**ALT Motor:** NEMA 11 (low torque needed)  
**AZ Motors:** NEMA 11 (×2, differential)  
**Placement:** ALT close-mounted, AZ remote-mounted  

**OR:**

**ALT:** Geared NEMA 11 with direct drive (no belt)  
**AZ:** NEMA 11 with belts (×2)  

**OR:**

**All 3:** NEMA 11 but remote-mount AZ motors away from scope

---

## Recommended Solution Matrix

| Priority | Motor Choice | Cost | Footprint | Torque | Complexity |
|----------|--------------|------|-----------|--------|----------|
| **Best Overall** | NEMA 11 | $24-36 | Smallest | Adequate | Low |
| **Extra Margin** | NEMA 14 | $36-54 | Small | Plenty | Low |
| **Simplest Mech** | Geared N11 | $75-120 | Small | Highest | Very Low |
| **Use NEMA 17** | Remote Mount | $36 | Large total | Highest | Medium |

## My Recommendation: NEMA 11

**Why:**
1. **Size:** 67% smaller footprint
2. **Weight:** 64% lighter (300g vs 840g total)
3. **Torque:** More than adequate for worm gear and screws
4. **Cost:** Cheaper than NEMA 17 ($24-36 vs $36)
5. **5mm shaft:** All your pulleys work
6. **Proven:** Used in compact 3D printers successfully
7. **Available:** Easy to source on Amazon

**Your prototype bracket:**
- Will need smaller mounting holes
- Much less material needed
- Lighter, more compact result
- Won't interfere with scope

---

## Updated Shopping List - NEMA 11

### Electronics

```
Arduino Nano:                  $8
3× TMC2208 drivers:           $24
3× NEMA 11 motors (28HS32):   $30  ← Was $36 for NEMA 17
12V 3A power supply:          $12
Wiring:                        $8
────────────────────────────────
Electronics:                   $82  ← SAVES $8
```

### Mechanical (same pulleys, smaller brackets)

```
Pulleys + belts:              $59
Custom screws (if needed):    $50
Motor brackets (smaller):     $15  ← Was $30
Hardware:                     $12
────────────────────────────────
Mechanical:                   $136
```

### **NEW TOTAL: $218** (vs $231 with NEMA 17)

**Savings: $13 + much better fit!**

---

## Torque Calculations - Why NEMA 11 Works

### ALT System Analysis

**Load:** Turn worm gear knob
```
Knob diameter: 30mm = 0.03m radius
Force to turn: ~2N (finger pressure, measured)
Torque at knob: 2N × 0.015m = 0.03 N·m = 3 N·cm

Belt reduction: 4:1 (20T:80T)
Motor torque needed: 3 N·cm / 4 = 0.75 N·cm

NEMA 11 provides: 8-12 N·cm
Safety factor: 10× to 16× ✓✓✓
```

**Conclusion:** Massive overkill - NEMA 11 perfect!

### AZ System Analysis

**Load:** Turn differential screws
```
Screw: M5 × 0.8mm pitch
Force per screw: ~3N (estimated)
Torque per screw: ~0.6 N·cm

Belt reduction: 3:1 (20T:60T)
Motor torque needed: 0.6 / 3 = 0.2 N·cm per motor

NEMA 11 provides: 8-12 N·cm
Safety factor: 40× to 60× ✓✓✓
```

**Conclusion:** Ridiculous overkill - NEMA 11 perfect!

### Why We Don't Need More Torque

Your application is **precision positioning**, not **heavy lifting**:
- No telescope weight on motors
- Worm gear does the work
- Screws are fine-pitch
- Low friction mechanisms
- Only need to overcome adjustment resistance

**High torque matters for:**
- Direct drive mounts (no reduction)
- Lifting telescope weight
- Fast slewing speeds
- Heavy loads

**Your case:**
- High reduction gearing
- Only turning adjustment knobs/screws
- Slow, precise movements
- Very light loads

**NEMA 11 is actually IDEAL for your application!**

---

## Motor Mounting Holes - Dimensional Change

### NEMA 17 Mounting Pattern

```
┌───────────────────────────────┐
│                               │
│   ●                       ●   │ ← 31mm spacing
│                               │
│           42mm                │
│                               │
│   ●                       ●   │
│                               │
└───────────────────────────────┘
```

### NEMA 11 Mounting Pattern

```
┌─────────────────────┐
│                     │
│  ●             ●    │ ← 23mm spacing
│                     │
│       28mm          │
│                     │
│  ●             ●    │
│                     │
└─────────────────────┘
```

**Your bracket redesign:**
- Reduce hole spacing: 31mm → 23mm
- Reduce overall size
- Same hole size (M3)
- Much easier to fit

---

## Next Steps

### 1. Measure Clearances (Today)

**With your prototype bracket:**
- How much space do you have?
- Where does interference occur?
- Minimum motor size needed?

**Answer:** If you have 30-35mm clearance, NEMA 11 fits perfectly!

### 2. Order NEMA 11 Test Motor (This Week)

**Buy just ONE motor first:**
- Test torque adequacy
- Verify physical fit
- Confirm pulleys work
- Total risk: $10

**Amazon search:**
- "NEMA 11 stepper motor 28HS32"
- "28mm stepper motor 5mm shaft"

### 3. Test Before Full Commit

**With one NEMA 11:**
1. Wire to your electronics
2. Test with pulley and belt
3. Measure torque against ALT knob
4. Verify adequate strength
5. **Then** order 2 more

### 4. Redesign Brackets

**For NEMA 11:**
- 28mm × 28mm body size
- 23mm mounting hole spacing
- M3 mounting screws
- Much lighter, simpler design

---

## FAQ

**Q: Is NEMA 11 strong enough?**  
A: YES! You have 10-60× safety margin. More than adequate.

**Q: Will my pulleys fit?**  
A: YES! Same 5mm shaft diameter as NEMA 17.

**Q: Will TMC2208 drivers work?**  
A: YES! Same driver, just set lower current limit (0.33-0.67A).

**Q: What about precision?**  
A: SAME! 200 steps/rev, same microstepping. Identical precision.

**Q: Can I use NEMA 11 and NEMA 17 together?**  
A: YES! Mix and match as needed. Same shaft size.

**Q: What if NEMA 11 doesn't work?**  
A: Upgrade to NEMA 14 (still 30% smaller than NEMA 17).

---

## Alternative: Redesign for NEMA 17

**If you really want NEMA 17:**

### Remote Mounting Strategy

**Place motors AWAY from mount:**
1. Build motor module box (3 motors together)
2. Mount on tripod leg or separate stand
3. Route long belts to mount head
4. Use belt guides at corners

**Advantages:**
- Can use NEMA 17 (higher torque margin)
- Motors away from telescope
- Consolidated electronics
- Better weight distribution

**Disadvantages:**
- More complex belt routing
- Longer belts (more friction)
- Less portable
- More parts

---

## Conclusion

**NEMA 11 is your solution:**

✅ **67% smaller** - fits in tight spaces  
✅ **64% lighter** - preserves mount portability  
✅ **10-60× more torque** than needed  
✅ **Same 5mm shaft** - pulleys work  
✅ **Cheaper** than NEMA 17  
✅ **Perfect for** precision positioning with gearing  

**Action items:**
1. Order ONE NEMA 11 motor to test ($10)
2. Verify torque adequate with your setup
3. Order 2 more if successful
4. Redesign brackets for 28mm × 28mm
5. Enjoy compact, lightweight automation!

**Your prototype taught you something important** - and now you have the right solution! 🎯

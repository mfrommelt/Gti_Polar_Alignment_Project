# Updated Shopping List - Differential AZ Control

## Important Update

Based on the clarification that AZ uses **opposing screws** (push-pull differential), you need **3 motors** instead of 2:

- 1 motor for ALT (altitude knob)
- 2 motors for AZ (west screw + east screw)

---

## Updated Essential Electronics (~$100)

### Same Components as Before

**Arduino Nano** - 1x - $8
**12V Power Supply** - Upgrade to 3A - $12 (was $10)
**USB Cable** - 1x - $4
**Jumper Wires** - 1 pack - $6
**Breadboard** (optional) - $5

### UPDATED Components

**TMC2208 V3.0 Stepper Drivers**
- **Quantity**: **3** (was 2)
- **Cost**: $24 total (3 × $8)
- **Where**: Amazon "BIGTREETECH TMC2208 V3.0 3-pack"
- **NOTE**: Often cheaper to buy 5-pack ($30) and have spares

**NEMA 11 Stepper Motors (0.33-0.67A)** ← UPDATED for compact size!
- **Quantity**: **3** (was 2)
- **Cost**: $30 total (3 × $10)
- **Where**: Amazon "NEMA 11 stepper motor 28HS32"
- **Why NEMA 11**: Star Adventurer GTi is compact - NEMA 17 (42mm) too bulky!
- **Size**: 28mm × 28mm (67% smaller than NEMA 17)
- **Note**: Same 5mm shaft, adequate torque with gear reductions

**Heatsinks**
- **Quantity**: 3 (for 3 drivers)
- **Usually included with drivers**

---

## Updated Total Cost

### Minimum Working System
```
Arduino Nano:           $8
3x TMC2208:             $24
3x NEMA 11:             $30  ← UPDATED (was $36)
12V 3A Power Supply:    $12
USB Cable:              $4
Jumper Wires:           $6
Heatsinks:              $2 (if not included)
───────────────────────────
SUBTOTAL:               $86  ← SAVES $6!
```

### Complete Mechanical System
```
Above electronics:      $86  ← UPDATED
3x Flexible Couplers:   $12 (3 × $4)
GT2 Belt (for ALT):     $10
GT2 Pulleys (for ALT):  $10
Hardware (screws):      $8
───────────────────────────
TOTAL:                  $126  ← SAVES $6!
```

**Benefits of NEMA 11**: Smaller (28mm vs 42mm), lighter, won't block telescope, same 5mm shaft!

---

## Smart Shopping Strategy

### Option 1: Buy Complete 3-Motor Kit

Look for combo kits on Amazon/AliExpress:
- "3D Printer Stepper Motor Kit" 
- Usually includes 5 motors + 5 drivers
- Cost: $60-80 total
- Gives you spares
- Often includes heatsinks and wiring

**Search Terms**:
- "5x NEMA 17 + 5x TMC2208 kit"
- "3D printer stepper driver set"
- "BIGTREETECH TMC2208 5-pack"

### Option 2: Buy Exactly What You Need

**3-Motor Specific Kit** (if available):
- Some sellers offer custom quantities
- Contact seller for quote
- May get slight discount

### Option 3: Individual Components

**Buy from same vendor to save shipping:**

Amazon cart example:
```
1. Arduino Nano CH340 USB              $8
2. NEMA 17 Motor 0.4A (qty 3)          $36
3. TMC2208 V3.0 Driver (qty 3)         $24
4. 12V 3A Power Adapter                $12
5. Dupont Jumper Wire Set              $6
6. 5mm Flexible Couplers (qty 3)       $12
7. GT2 Belt + Pulley Kit               $15
────────────────────────────────────────────
TOTAL:                                 $113
```

---

## Power Supply Upgrade

### Why 3A Instead of 2A?

**Power Calculation** (with NEMA 11):
```
3 motors @ 0.67A each = 2.0A continuous max
3 motors @ 0.33A each = 1.0A continuous min
Typical operation:      ~1.3A continuous
Arduino: ~0.1A
Total: ~1.4A continuous

Peak current (all motors): ~2.2A
Safety margin (30%): 2.2A × 1.3 = 2.9A

Recommended: 3A supply
```

**Note**: NEMA 11 uses less power than NEMA 17 - 3A still provides good margin.

### Power Supply Options

**12V 3A AC/DC Adapter**
- **Cost**: $10-15
- **Where**: Amazon "12V 3A Power Supply 2.1mm"
- **Specs**: 
  - Output: 12V DC, 3A
  - Connector: 2.1mm barrel jack
  - Input: 100-240V AC
  - Safety: UL/CE listed

**Alternative - USB PD Power Bank**
- **Type**: USB-C PD with 12V output
- **Cost**: $35-50
- **Benefit**: Portable field operation
- **Example**: "12V USB-C PD Trigger Cable"

---

## Updated Wiring Requirements

### Additional Wire Needed

**For 3rd Motor**:
- 6 more jumper wires (step, dir, enable, 2x motor coils, gnd)
- 1 more motor cable (usually included with motor)
- Total: Same wire pack works, just need to organize better

### Wire Organization Tips

Use different colors for different functions:
- **Red**: Power (12V, VIN)
- **Black**: Ground (GND)
- **Yellow**: STEP signals
- **Green**: DIR signals
- **Blue**: ENABLE signals
- **White**: Motor connections

---

## Mechanical Components Update

### Couplers for AZ Screws

**You Need**:
- 2x flexible couplers for AZ screws (west + east)
- 1x coupler OR pulley for ALT
- Total: 3 couplers minimum

**Sizing**:
- Motor side: 5mm (NEMA 11 standard shaft - same as NEMA 17!)
- Screw side: **MEASURE YOUR SCREWS!**
  - Common sizes: 3mm, 4mm, 5mm, 6mm
  - May need to drill/tap screw heads

**Cost**: $4 each × 3 = $12

### Mounting Brackets Update

**For 3 Motors**:
- Need mounting space for 3 motors instead of 2
- West motor + East motor need to be symmetric
- ALT motor mounts as before

**Options**:
1. **3D printed custom bracket** ($10-15 in filament) - **Easier with NEMA 11!**
2. **Aluminum L-brackets** ($12-18) - **Smaller for NEMA 11**
3. **Commercial NEMA 11 brackets** ($6 each × 3 = $18) - **Compact!**

**Note**: NEMA 11 brackets much smaller than NEMA 17 - easier to fit on mount!

---

## Bundle Deals to Look For

### Amazon/AliExpress Deals

**3D Printer Kits** typically have NEMA 17 (too large).  
For NEMA 11, buy individually:

**NEMA 11 + Driver Bundle** (if available):
- 3× NEMA 11 motors  
- 3× TMC2208 drivers
- Often sold for compact CNC or small 3D printers
- Cost: $50-70 total
- **Search**: "NEMA 11 stepper kit" or "28mm stepper CNC"

**Or Buy Separately** (more common):
- NEMA 11 motors individually: $10 each × 3 = $30
- TMC2208 5-pack: $30 (have 2 spares)
- Total: $60 for motors + drivers

---

## Cost Comparison: 3-Motor vs Platform

### 3-Motor Differential (Updated with NEMA 11)
```
Electronics:             $86  ← UPDATED
Mechanical:              $40
────────────────────────────
TOTAL:                   $126 ← SAVES $6!
```

**Bonus**: NEMA 11 is smaller, lighter, won't interfere with telescope!

### 2-Motor Platform
```
Electronics:             $70
Platform bearing:        $25
Worm gear:               $30
Brackets/hardware:       $25
────────────────────────────
TOTAL:                   $150
```

**Difference**: Only $18 more for platform approach

---

## Recommended Purchase Plan

### Phase 1: Electronics Testing ($86)

Buy first to test before mechanical:
1. Arduino Nano
2. 3× TMC2208 drivers
3. 3× NEMA 11 motors ← UPDATED (28mm × 28mm compact!)
4. 12V 3A power supply
5. Wiring/breadboard

**Test everything works before buying mechanical parts**

**Why NEMA 11**: Compact size crucial for Star Adventurer GTi - NEMA 17 too bulky!

### Phase 2: Mechanical Integration ($40)

After electronics proven:
1. Measure your exact screw dimensions
2. Order correct size couplers
3. Order ALT belt/pulley system
4. Design/order mounting brackets

---

## Where to Buy - Updated Recommendations

### Best Value: AliExpress

**Pros**:
- Cheapest pricing (often 50% off Amazon)
- Many bundle options
- 3D printer kits perfect for this

**Cons**:
- Slow shipping (2-6 weeks)
- Less reliable customer service
- Check seller ratings carefully

**Recommended Search**:
- "3D printer stepper kit 5 motor TMC2208"
- "CNC stepper motor kit 3 axis"
- Filter: 4+ stars, 100+ orders

### Fastest: Amazon Prime

**Pros**:
- 2-day shipping available
- Easy returns
- Reliable brands (BIGTREETECH)

**Cons**:
- Higher cost
- Fewer bundle options

**Recommended Products**:
1. BIGTREETECH TMC2208 V3.0 (5-pack) - $30-35
2. NEMA 11 28HS32 stepper motor - $10-12 each ← UPDATED for compact size!
3. ALITOVE 12V 3A Power Supply - $11

**Search terms**: 
- "NEMA 11 stepper motor 28HS32"
- "28mm stepper motor 0.67A 5mm shaft"

### Best Quality: StepperOnline

**Pros**:
- High-quality motors
- Good documentation
- Excellent customer service

**Cons**:
- Higher price
- Shipping costs

**Use for**: Final production build after prototyping

---

## Sample Amazon Shopping Cart

**Copy-paste these search terms**:

```
1. "Arduino Nano V3 ATmega328P CH340"
   Price: ~$8

2. "NEMA 11 Stepper Motor 28HS32 0.67A 5mm"
   Quantity: 3
   Price: ~$10 each = $30  ← UPDATED for compact mount!

3. "BIGTREETECH TMC2208 V3.0 Stepper Motor Driver"
   Quantity: 3 (or buy 5-pack for $30)
   Price: ~$24

4. "12V 3A Power Supply Adapter 2.1mm"
   Price: ~$12

5. "Dupont Jumper Wire Kit 120pcs"
   Price: ~$6

6. "5mm Flexible Shaft Coupling Coupler"
   Quantity: 3
   Price: ~$12

7. "GT2 Timing Belt Kit 6mm with Pulleys"
   Price: ~$15
```

**Cart Total**: ~$107 + tax/shipping  ← SAVES $6 with NEMA 11!

---

## Money-Saving Alternatives

### Option A: Reuse 3D Printer Parts

If you have an old 3D printer:
- Salvage 3 stepper motors (typically NEMA 17 - but check size!)
- **Warning**: NEMA 17 may be too bulky for Star Adventurer GTi
- **Better**: Look for NEMA 11 or compact NEMA 14
- Salvage TMC drivers or A4988 drivers
- Reuse power supply if 12V
- **Cost**: $20 for Arduino + wiring

### Option B: Arduino Nano Clone

- Official Arduino Nano: $25
- CH340 clone: $3-5
- **Savings**: $20
- **Note**: Functionality identical for this project

### Option C: A4988 Drivers Instead of TMC2208

- A4988: $3 each
- TMC2208: $8 each
- **Savings**: $15 (for 3 drivers)
- **Tradeoff**: A4988 is louder but works fine

**If using A4988**:
- Need to adjust current limit differently
- Noisier operation (not ideal for astronomy)
- Same functionality otherwise

---

## Final Shopping Checklist

Before ordering, verify:

- [ ] **3** stepper motors (not 2!)
- [ ] **NEMA 11** (28mm) recommended for compact mount ← UPDATED!
- [ ] Or NEMA 14/17 if remote-mounting motors
- [ ] **3** stepper drivers (not 2!)
- [ ] **12V 3A** power supply (not 2A)
- [ ] Arduino has USB cable included
- [ ] TMC2208 version 3.0 or later
- [ ] Motors are 5mm shaft diameter
- [ ] Measured AZ screw diameters for couplers
- [ ] Heatsinks included with drivers
- [ ] Jumper wires are male-to-female

---

## When You Can Skip the 3rd Motor

**Only use 2 motors if you choose the Platform Rotation approach**:
- 1 motor for ALT
- 1 motor for AZ platform rotation
- See DIFFERENTIAL_AZ_CONTROL.md for details

For the differential screw approach (easier mechanically), you **must have 3 motors**.

---

## Bulk Discount Opportunities

If you know other astronomers interested in automation:

**Group Buy Benefits**:
- 10-pack motors: ~$8 each (vs $12)
- 10-pack TMC2208: ~$6 each (vs $8)
- Split shipping costs
- Everyone saves 20-30%

**Suggested**: Post in local astronomy club!

---

## Updated Timeline

### With 3 Motors

| Source | Delivery Time |
|--------|---------------|
| Amazon Prime | 2 days - 1 week |
| Amazon Standard | 1-2 weeks |
| AliExpress | 2-6 weeks |

**Recommendation**: Order everything at once to avoid multiple shipping costs.

---

## What If I Already Ordered 2 Motors?

**No problem!** Two options:

1. **Order 1 more motor + driver**
   - Add to your kit
   - Total cost: +$20
   - Minimal delay

2. **Switch to Platform Rotation approach**
   - Use 2 motors you have
   - More mechanical work
   - See MECHANICAL_GUIDE.md Option B

---

## Ready to Order?

**Fastest path (NEMA 11 - Compact!)**: 
1. Search Amazon for "NEMA 11 stepper motor 28HS32"
2. Buy 3 motors individually ($30 total)
3. Add BIGTREETECH TMC2208 5-pack ($30)
4. Add Arduino Nano ($8)
5. Add 12V 3A power supply ($12)
6. Add wire kit ($6)
7. **Total**: ~$86, delivered in 2 days
8. **Bonus**: Won't interfere with telescope!

**Budget path**:
1. AliExpress "NEMA 11 stepper motor 28mm"
2. Buy 3 motors + TMC2208 drivers separately
3. Total: ~$45-55
4. Wait 3-4 weeks
5. Save $30-40

**Alternative (if space permits)**:
- NEMA 17 remote-mounted away from telescope
- Longer belts required
- See COMPACT_MOTOR_SOLUTIONS.md

Your choice! 🛒

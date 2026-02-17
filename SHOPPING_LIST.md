# Shopping List - Star Adventurer GTi Polar Alignment Controller

Complete parts list with specific product recommendations and approximate costs.

## Essential Electronics (~$75)

### Microcontroller

**Arduino Nano** (Recommended)
- **Specs**: ATmega328P, 5V, USB Mini/Micro
- **Quantity**: 1
- **Cost**: $5-10
- **Where to Buy**:
  - Amazon: "Arduino Nano V3.0"
  - AliExpress: "NANO V3.0 ATmega328P"
  - Local electronics store
- **Alternative**: Arduino Uno ($15-20) - works but larger

**Why Arduino Nano?**
- Compact size
- USB connectivity
- 5V logic compatible with TMC2208
- Well-documented, huge community support
- Easy to integrate into final enclosure

---

### Stepper Motor Drivers

**TMC2208 V3.0 Stepper Driver**
- **Specs**: 
  - Silent operation (StealthChop)
  - 256 microstep resolution
  - 2A peak current
  - 12-24V input
  - UART configuration (optional)
- **Quantity**: 2
- **Cost**: $5-8 each
- **Where to Buy**:
  - Amazon: "BIGTREETECH TMC2208 V3.0"
  - AliExpress: "TMC2208 V3.0 Stepper Driver"
  - BigTreeTech official store
- **Alternative**: 
  - A4988 ($3-5 each) - louder but cheaper
  - DRV8825 ($5-7 each) - higher current capability

**Why TMC2208?**
- Nearly silent operation (important for astronomy)
- Excellent microstepping accuracy
- Built-in protection (thermal, over-current)
- Widely available
- Well-documented

**Important**: Get V3.0 or newer for best reliability

---

### Stepper Motors

**NEMA 17 Stepper Motor (17HS4401)**
- **Specs**:
  - Step angle: 1.8° (200 steps/rev)
  - Voltage: 12V
  - Current: 0.4A - 1.7A (0.4A recommended for less heat)
  - Holding torque: 40-50 N·cm
  - Shaft: 5mm diameter
  - 4-wire bipolar
- **Quantity**: 2
- **Cost**: $10-15 each
- **Where to Buy**:
  - Amazon: "NEMA 17 Stepper Motor 12V 0.4A"
  - StepperOnline: Part #17HS4401
  - AliExpress: "42 Stepper Motor 17HS4401"
- **Recommended models**:
  - 17HS4401: 0.4A, less heat (best for astronomy)
  - 17HS8401: 1.7A, more torque (if high load)

**Motor Selection Guide**:
- **0.4A motors**: Cooler, quieter, sufficient for polar align
- **1.7A motors**: More torque, but more heat
- **Avoid pancake motors**: Less torque

---

### Power Supply

**12V 2A DC Power Adapter**
- **Specs**:
  - Output: 12V DC, 2A minimum (3A preferred)
  - Connector: 2.1mm barrel jack OR bare wires
  - Input: 100-240V AC (universal)
  - Safety: UL/CE certified
- **Quantity**: 1
- **Cost**: $8-12
- **Where to Buy**:
  - Amazon: "12V 3A Power Supply"
  - Local electronics store
  - Reuse old laptop/router power supply (check voltage!)

**Power Requirements**:
```
Arduino Nano:     ~100mA (0.5W)
2x NEMA 17 (0.4A): ~800mA total (9.6W)
TMC2208 drivers:   ~50mA each (0.6W)
Total:            ~1A continuous (12W)
Peak:             ~2A (24W)
```

**Recommendation**: Get 3A supply for headroom

**Alternative Power**:
- USB power bank (5V) + DC-DC boost converter (5V→12V)
- Portable battery pack (12V, for field use)
- Car cigarette lighter adapter (12V)

---

### Wiring & Connectors

**Jumper Wires - Dupont Connectors**
- **Specs**: 
  - Male-to-Female
  - 20cm length
  - 22 AWG
- **Quantity**: 20+ wires
- **Cost**: $5-8
- **Where to Buy**:
  - Amazon: "Dupont Jumper Wire Kit"
  - AliExpress: "120pcs Dupont Wire Set"

**USB Cable**
- **Type**: USB-A to Mini-USB or Micro-USB
- **Length**: 1-2 meters
- **Quantity**: 1
- **Cost**: $3-5
- **Note**: Match to your Arduino Nano connector type

**Optional - Barrel Jack Connector**
- For clean 12V power connection
- **Cost**: $2-3
- **Where**: Amazon "DC Barrel Jack Connector"

**Optional - Screw Terminals**
- For permanent motor connections
- **Cost**: $5
- **Where**: Amazon "Screw Terminal Block"

---

### Accessories

**Heatsinks for TMC2208**
- **Size**: 8.8 x 8.8 x 5mm aluminum
- **Quantity**: 2 (or 4 if you want extras)
- **Cost**: $2-3
- **Where to Buy**: Often included with TMC2208 drivers
- **Note**: CRITICAL - drivers will overheat without these!

**Breadboard (Optional for Prototyping)**
- **Size**: 400 or 830 point
- **Quantity**: 1
- **Cost**: $3-5
- **Where to Buy**: Amazon "Solderless Breadboard"
- **Note**: Makes prototyping cleaner, not needed for final build

**Multimeter (If you don't have one)**
- **Essential for**:
  - Setting current limit (Vref)
  - Checking voltages
  - Identifying motor coils
  - Troubleshooting
- **Cost**: $15-30
- **Recommendation**: Any basic digital multimeter works

---

## Mechanical Components (~$30)

### Belt Drive System

**GT2 Timing Belt**
- **Specs**: 
  - Type: GT2 (2mm pitch)
  - Width: 6mm
  - Length: 2 meters (buy extra for mistakes)
- **Quantity**: 2m minimum
- **Cost**: $8-12
- **Where to Buy**:
  - Amazon: "GT2 Timing Belt 6mm"
  - AliExpress: "GT2 Belt 2GT 6mm"
- **Note**: Get rubber belt, not fiberglass core (more forgiving)

**GT2 Pulleys**
- **Specs**:
  - Type: GT2, 2mm pitch
  - Teeth: 20T (tooth count)
  - Bore: 5mm (for motor shaft)
  - Width: 6mm
- **Quantity**: 4 (2 for motors, 2 for knob shafts)
- **Cost**: $8-12 for set of 4
- **Where to Buy**:
  - Amazon: "GT2 Pulley 20 Teeth 5mm Bore"
  - AliExpress: "GT2 20T Pulley Set"

**Pulley Options**:
- **20 teeth**: Standard, works for most applications
- **16 teeth**: Smaller, tighter bends
- **30+ teeth**: Larger, better for high-torque

---

### Couplers & Shafts

**Flexible Shaft Couplers**
- **Specs**:
  - Type: Aluminum flexible jaw coupling
  - Size: 5mm to 5mm (or 5mm to your knob shaft size)
  - Length: 25mm
- **Quantity**: 2-4
- **Cost**: $6-10
- **Where to Buy**:
  - Amazon: "5mm to 5mm Flexible Coupling"
  - AliExpress: "Flexible Shaft Coupler"

**Alternative**: Rigid couplers (cheaper but require perfect alignment)

---

### Mounting Hardware

**Motor Brackets** (Option 1: 3D Printed)
- **Material**: PLA or PETG
- **Cost**: $5-10 (material + printing service)
- **Where**: 
  - Print yourself if you have 3D printer
  - Local makerspace
  - Online printing service (Craftcloud, Shapeways)
- **Note**: STL files to be added to project

**Motor Brackets** (Option 2: Aluminum)
- **Type**: NEMA 17 mounting bracket
- **Cost**: $8-12 each
- **Where to Buy**:
  - Amazon: "NEMA 17 Stepper Motor Bracket"
  - McMaster-Carr: Part #6061 Aluminum bracket

**Screws & Hardware**
- **M3 screws**: 20-30 pieces, various lengths (6mm, 10mm, 20mm)
- **M4 screws**: 10 pieces (for motor mounting)
- **Cost**: $5-8
- **Where**: Amazon "M3 M4 Screw Assortment Kit"

---

## Optional Upgrades (~$50)

### Enclosure

**Project Box**
- **Size**: 150mm x 100mm x 50mm minimum
- **Material**: ABS plastic or aluminum
- **Cost**: $10-15
- **Where**: Amazon "Electronic Project Enclosure"
- **Purpose**: Protect electronics, professional appearance

**Alternative**: 3D print custom enclosure

---

### Improved Power

**Portable Power Bank - 12V Output**
- **Specs**: 
  - 12V DC output
  - 10,000+ mAh capacity
  - Multiple outputs
- **Cost**: $30-40
- **Where**: Amazon "12V Portable Battery Pack"
- **Benefit**: Field use without AC power

**DC-DC Converter** (if using USB power bank)
- **Input**: 5V USB
- **Output**: 12V, 2A
- **Cost**: $8-12
- **Where**: Amazon "USB to 12V DC Converter"

---

### Field Deployment

**Weatherproof Case**
- **Type**: IP65 rated plastic case
- **Size**: Fits all electronics
- **Cost**: $15-25
- **Purpose**: Protection from dew, moisture
- **Where**: Amazon "Waterproof Electronics Case"

**Cable Management**
- **Spiral wrap**: $5
- **Cable ties**: $3
- **Velcro straps**: $5

---

## Total Cost Breakdown

### Minimum Working System
```
Arduino Nano:            $8
2x TMC2208:              $16 (2 × $8)
2x NEMA 17:              $24 (2 × $12)
12V Power Supply:        $10
USB Cable:               $4
Jumper Wires:            $6
Heatsinks:               $2 (often included)
──────────────────────
SUBTOTAL:                $70
```

### Complete Mechanical System
```
Above electronics:       $70
GT2 Belt:                $10
GT2 Pulleys:             $10
Couplers:                $8
Hardware (screws):       $7
──────────────────────
TOTAL:                   $105
```

### Professional System
```
Above complete:          $105
Enclosure:               $12
Portable power:          $35
Weatherproofing:         $20
──────────────────────
TOTAL:                   $172
```

---

## Where to Buy - Recommended Vendors

### United States
- **Amazon**: Fast shipping, easy returns
- **Adafruit**: High quality, US-based support
- **StepperOnline**: Specialized motors
- **McMaster-Carr**: Industrial-grade hardware

### International
- **AliExpress**: Cheapest, slower shipping (2-4 weeks)
- **Banggood**: Good middle ground
- **Mouser**: Electronic components
- **DigiKey**: Electronic components, technical support

### Local
- **Micro Center**: In-store pickup (if near you)
- **Local electronics stores**: Immediate availability
- **Makerspace**: May have components to borrow

---

## Money-Saving Tips

1. **Buy kits**: "Arduino + Stepper Kit" often cheaper
2. **Shop sales**: Black Friday, Prime Day
3. **Buy bulk**: Share with astronomy club
4. **Reuse**: Old 3D printer parts (motors, drivers, belts)
5. **Print locally**: Cheaper than online printing services

---

## Sample Amazon Shopping Cart

**Complete System - Ready to Order**

1. Arduino Nano V3.0 (with cable) - $8
2. BIGTREETECH TMC2208 V3.0 (2-pack) - $16
3. NEMA 17 Stepper Motor 0.4A (2-pack) - $24
4. 12V 3A Power Supply - $11
5. Dupont Jumper Wire Kit - $7
6. GT2 Belt + Pulley Kit - $15
7. M3/M4 Screw Assortment - $8
8. 5mm Shaft Couplers (2pcs) - $7

**Total**: ~$96 + tax/shipping

**Search terms for Amazon**:
- "Arduino Nano ATmega328P CH340"
- "TMC2208 V3.0 stepper driver"
- "NEMA 17 stepper motor 0.4A 40Ncm"
- "12V 3A power adapter 2.1mm barrel"
- "GT2 timing belt pulley kit"

---

## Verification Checklist

Before ordering, verify:

- [ ] Arduino Nano has USB cable included
- [ ] TMC2208 version 3.0 or newer
- [ ] NEMA 17 motors are 5mm shaft diameter
- [ ] Power supply is 12V, minimum 2A
- [ ] GT2 belt width matches pulley width (6mm)
- [ ] Pulley bore matches motor shaft (5mm)
- [ ] Heatsinks included with TMC2208 (or order separately)

---

## Next Steps After Purchasing

1. **Read QUICK_START.md** for assembly instructions
2. **Test electronics** before mechanical integration
3. **Measure your mount** for custom bracket design
4. **Join community** to share your build!

---

**Estimated Delivery Time**: 
- Amazon Prime: 2 days - 1 week
- Standard shipping: 1-2 weeks
- International: 2-6 weeks

**Ready to build?** Order your parts and let's automate that polar alignment! 🔭✨

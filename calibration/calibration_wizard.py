#!/usr/bin/env python3
"""
Calibration Wizard for Star Adventurer GTi Polar Alignment System

This wizard guides you through calibrating:
1. Steps per arcsecond (ALT and AZ)
2. Backlash measurement (ALT and AZ)
3. Speed limits

The calibration is saved to the Arduino's EEPROM for permanent storage.

Usage:
    python calibration_wizard.py [port]
    
If port is not specified, will auto-detect Arduino.
"""

import serial
import serial.tools.list_ports
import time
import sys

class CalibrationWizard:
    def __init__(self, port=None):
        self.serial = None
        self.port = port
        self.connected = False
        
    def find_arduino(self):
        """Auto-detect Arduino port"""
        ports = list(serial.tools.list_ports.comports())
        for p in ports:
            if 'USB' in p.description or 'Arduino' in p.description or 'CH340' in p.description:
                return p.device
        return None
    
    def connect(self):
        """Connect to Arduino"""
        if not self.port:
            self.port = self.find_arduino()
            
        if not self.port:
            print("ERROR: Could not find Arduino. Please specify port.")
            return False
            
        try:
            self.serial = serial.Serial(self.port, 115200, timeout=2)
            time.sleep(2)  # Wait for Arduino reset
            
            # Clear any startup messages
            while self.serial.in_waiting:
                self.serial.readline()
                
            self.connected = True
            print(f"✓ Connected to Arduino on {self.port}")
            return True
        except Exception as e:
            print(f"ERROR: Could not connect to {self.port}: {e}")
            return False
    
    def send_command(self, cmd):
        """Send command and return response"""
        if not self.connected:
            return None
            
        self.serial.write(f"{cmd}\n".encode())
        time.sleep(0.1)
        
        response = []
        while self.serial.in_waiting:
            line = self.serial.readline().decode('utf-8').strip()
            response.append(line)
        
        return '\n'.join(response)
    
    def clear_screen(self):
        """Clear terminal screen"""
        print("\n" * 50)
    
    def print_header(self, title):
        """Print section header"""
        print("\n" + "="*70)
        print(f"  {title}")
        print("="*70 + "\n")
    
    def calibrate_steps_per_arcsec(self, axis):
        """Calibrate steps per arcsecond for ALT or AZ"""
        axis_name = "ALTITUDE (ALT)" if axis == "ALT" else "AZIMUTH (AZ)"
        
        self.print_header(f"Calibrating {axis_name} - Steps per Arcsecond")
        
        print(f"""
This calibration measures how many motor steps equal one arcsecond of 
{axis_name.lower()} movement.

METHOD 1 - Star Drift Timing (Most Accurate):
1. Point telescope at star near celestial equator
2. Turn off tracking
3. Note time for star to drift 1 arcminute (60 arcsec)
4. We'll calculate steps per arcsecond from motor movement

METHOD 2 - Polar Scope Reticle (Good):
1. Use polar scope reticle markings
2. Move mount and measure angular change
3. Calculate from known reticle spacing

METHOD 3 - Manual Measurement (Acceptable):
1. Measure physical movement of adjustment knob/screw
2. Calculate from known gear ratios

Which method do you want to use?
""")
        
        choice = input("Enter 1, 2, or 3 (or 'skip' to skip): ").strip()
        
        if choice.lower() == 'skip':
            return False
            
        if choice == '1':
            return self.calibrate_drift_method(axis)
        elif choice == '2':
            return self.calibrate_reticle_method(axis)
        elif choice == '3':
            return self.calibrate_manual_method(axis)
        else:
            print("Invalid choice. Skipping.")
            return False
    
    def calibrate_drift_method(self, axis):
        """Calibrate using star drift timing"""
        print(f"\n--- Star Drift Method for {axis} ---\n")
        
        print("SETUP:")
        print("1. Point telescope at star near celestial equator")
        print("2. Center star in eyepiece")
        print("3. Turn OFF mount tracking")
        print("4. Get stopwatch ready")
        
        input("\nPress ENTER when ready...")
        
        print("\nNow we'll move the mount slightly in one direction.")
        print("You'll time how long it takes for the star to drift back to center.")
        
        # Suggest movement amount
        test_steps = 1000
        print(f"\nWe'll move {test_steps} steps.")
        
        move_cmd = f"A{test_steps}" if axis == "ALT" else f"Z{test_steps}"
        
        input("Press ENTER to move mount...")
        
        # Enable motors and move
        self.send_command("E")
        response = self.send_command(move_cmd)
        print(f"Mount moved. Response: {response}")
        
        print("\nSTART TIMING NOW!")
        print("Watch the star drift back to center position.")
        print("Stop timing when star returns to original position.")
        
        input("\nPress ENTER when star has returned to center...")
        
        drift_time = float(input("Enter drift time in SECONDS: "))
        
        # Calculate
        # Earth rotates 15 arcseconds per second
        arcsec_moved = drift_time * 15.0
        steps_per_arcsec = test_steps / arcsec_moved
        
        print(f"\n=== CALCULATION ===")
        print(f"Drift time: {drift_time} seconds")
        print(f"Angular movement: {arcsec_moved:.2f} arcseconds")
        print(f"Steps used: {test_steps}")
        print(f"Result: {steps_per_arcsec:.2f} steps/arcsecond")
        
        confirm = input("\nSave this calibration? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            cal_cmd = f"CAL:{axis}:{arcsec_moved}:{test_steps}"
            response = self.send_command(cal_cmd)
            print(response)
            return True
        else:
            return False
    
    def calibrate_reticle_method(self, axis):
        """Calibrate using polar scope reticle"""
        print(f"\n--- Polar Scope Reticle Method for {axis} ---\n")
        
        print("SETUP:")
        print("1. Look through polar scope")
        print("2. Note starting position on reticle")
        print("3. We'll move the mount")
        print("4. Measure angular change on reticle")
        
        input("\nPress ENTER when ready...")
        
        test_steps = int(input("How many steps to move? (suggest 1000-2000): "))
        
        move_cmd = f"A{test_steps}" if axis == "ALT" else f"Z{test_steps}"
        
        # Move
        self.send_command("E")
        response = self.send_command(move_cmd)
        print(f"Mount moved. Response: {response}")
        
        print("\nMeasure the angular change on the polar scope reticle.")
        print("Each small division is typically 1-5 arcminutes.")
        print("Refer to your polar scope manual for exact spacing.")
        
        arcsec_moved = float(input("\nEnter angular movement in ARCSECONDS: "))
        
        if arcsec_moved > 0:
            steps_per_arcsec = test_steps / arcsec_moved
            
            print(f"\n=== CALCULATION ===")
            print(f"Steps moved: {test_steps}")
            print(f"Angular movement: {arcsec_moved} arcseconds")
            print(f"Result: {steps_per_arcsec:.2f} steps/arcsecond")
            
            confirm = input("\nSave this calibration? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                cal_cmd = f"CAL:{axis}:{arcsec_moved}:{test_steps}"
                response = self.send_command(cal_cmd)
                print(response)
                return True
        
        return False
    
    def calibrate_manual_method(self, axis):
        """Calibrate using manual calculation"""
        print(f"\n--- Manual Calculation Method for {axis} ---\n")
        
        print("This method uses known gear ratios and measurements.")
        print("\nYou'll need to know:")
        print("- Belt reduction ratio")
        print("- Gear reduction ratio (worm gear for ALT)")
        print("- Screw pitch (for AZ)")
        
        print("\nOR you can measure movement directly:")
        
        test_steps = int(input("How many steps to move? (suggest 10000): "))
        
        move_cmd = f"A{test_steps}" if axis == "ALT" else f"Z{test_steps}"
        
        print("\nMoving mount...")
        self.send_command("E")
        response = self.send_command(move_cmd)
        print(f"Response: {response}")
        
        print("\nMeasure how far the mount moved.")
        print("You can use a protractor, polar scope, or star drift.")
        
        degrees_moved = float(input("Enter movement in DEGREES: "))
        
        if degrees_moved > 0:
            arcsec_moved = degrees_moved * 3600
            steps_per_arcsec = test_steps / arcsec_moved
            
            print(f"\n=== CALCULATION ===")
            print(f"Steps moved: {test_steps}")
            print(f"Degrees moved: {degrees_moved}°")
            print(f"Arcseconds: {arcsec_moved}")
            print(f"Result: {steps_per_arcsec:.2f} steps/arcsecond")
            
            confirm = input("\nSave this calibration? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                cal_cmd = f"CAL:{axis}:{arcsec_moved}:{test_steps}"
                response = self.send_command(cal_cmd)
                print(response)
                return True
        
        return False
    
    def calibrate_backlash(self, axis):
        """Calibrate backlash for ALT or AZ"""
        axis_name = "ALTITUDE" if axis == "ALT" else "AZIMUTH"
        
        self.print_header(f"Calibrating {axis_name} Backlash")
        
        print(f"""
Backlash is the "dead zone" when you reverse direction.
This happens due to gear play, belt slack, or screw clearance.

PROCEDURE:
1. We'll move in one direction
2. Then reverse direction
3. You count how many steps before actual movement starts
4. That count = backlash in steps

You'll need to observe the mount carefully (or use indicator)
""")
        
        perform = input("Perform backlash test? (yes/no): ").strip().lower()
        
        if perform != 'yes':
            return False
        
        # Enable motors
        self.send_command("E")
        
        # Move forward first
        print("\n--- Moving forward 2000 steps ---")
        move_cmd = f"A2000" if axis == "ALT" else f"Z2000"
        self.send_command(move_cmd)
        time.sleep(2)
        
        print("\n--- Now reversing direction ---")
        print("Watch carefully! Count steps until you see actual movement.")
        print("Movement may be subtle - look for knob/screw to start turning.")
        
        input("\nPress ENTER to start reverse movement (slow)...")
        
        # Set slow speed for observation
        self.send_command("V100")
        
        # Move slowly in reverse
        reverse_steps = 500
        move_cmd = f"A-{reverse_steps}" if axis == "ALT" else f"Z-{reverse_steps}"
        self.send_command(move_cmd)
        
        print(f"\nMoving {reverse_steps} steps in reverse at slow speed...")
        
        input("\nPress ENTER when done...")
        
        backlash = int(input(f"\nHow many steps before {axis_name} moved? "))
        
        if backlash >= 0:
            print(f"\nBacklash measured: {backlash} steps")
            
            # Reset speed
            self.send_command("V800")
            
            confirm = input("Save this backlash value? (yes/no): ").strip().lower()
            
            if confirm == 'yes':
                cal_cmd = f"CAL:{axis}BL:{backlash}"
                response = self.send_command(cal_cmd)
                print(response)
                return True
        
        return False
    
    def run_wizard(self):
        """Run complete calibration wizard"""
        self.clear_screen()
        print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    Star Adventurer GTi Calibration Wizard                     ║
║    Version 3.0                                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

This wizard will guide you through calibrating your polar alignment
automation system. Calibration is essential for accurate positioning.

What we'll calibrate:
  1. ALT (Altitude) steps per arcsecond
  2. AZ (Azimuth) steps per arcsecond
  3. ALT backlash
  4. AZ backlash

Calibration data is saved to Arduino EEPROM (permanent storage).

REQUIREMENTS:
  - Mount assembled and working
  - Motors connected and powered
  - Arduino connected via USB
  - Clear sky (for star drift method) OR
  - Access to polar scope reticle
  
Press ENTER to begin or Ctrl+C to exit...
""")
        
        try:
            input()
        except KeyboardInterrupt:
            print("\nCalibration cancelled.")
            return
        
        # Connect to Arduino
        if not self.connect():
            return
        
        # Check current calibration
        print("\n--- Checking current calibration ---")
        response = self.send_command("CAL:SHOW")
        print(response)
        
        input("\nPress ENTER to continue...")
        
        # Calibrate ALT
        self.calibrate_steps_per_arcsec("ALT")
        
        # Calibrate AZ
        self.calibrate_steps_per_arcsec("AZ")
        
        # Calibrate ALT backlash
        self.calibrate_backlash("ALT")
        
        # Calibrate AZ backlash
        self.calibrate_backlash("AZ")
        
        # Show final calibration
        self.print_header("Final Calibration")
        response = self.send_command("CAL:SHOW")
        print(response)
        
        # Save to EEPROM
        print("\n--- Saving Calibration to EEPROM ---")
        save = input("Save calibration permanently? (yes/no): ").strip().lower()
        
        if save == 'yes':
            response = self.send_command("CAL:SAVE")
            print(response)
            print("\n✓ Calibration saved!")
            print("This data will persist across power cycles.")
        else:
            print("\nCalibration NOT saved (will be lost on power cycle)")
        
        # Final message
        print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    Calibration Complete!                                       ║
║                                                                ║
║    Your polar alignment system is now calibrated.              ║
║    You can re-run this wizard anytime to recalibrate.         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
""")
        
        self.serial.close()

def main():
    port = sys.argv[1] if len(sys.argv) > 1 else None
    
    wizard = CalibrationWizard(port)
    wizard.run_wizard()

if __name__ == "__main__":
    main()

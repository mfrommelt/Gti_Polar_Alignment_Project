#!/usr/bin/env python3
"""
Automatic Polar Alignment Integration for Star Adventurer GTi
Monitors SharpCap/NINA log files and automatically adjusts mount

Based on OpenAstroTracker AutoPA architecture
Adapted for Star Adventurer GTi with calibration support

Usage:
    python plate_solving_autopa.py [--software sharpcap|nina] [--port COM3]
"""

import os
import re
import time
import argparse
import sys
from pathlib import Path
from datetime import datetime

# Import your existing controller
try:
    from polar_align_control import PolarAlignController
except ImportError:
    print("ERROR: Could not import polar_align_control.py")
    print("Make sure it's in the same directory as this script")
    sys.exit(1)

class PlateS olvingAutoPA:
    """Automatic Polar Alignment using plate solving software"""
    
    def __init__(self, software='sharpcap', port=None, target_error=30.0):
        """
        Initialize AutoPA
        
        Args:
            software: 'sharpcap' or 'nina'
            port: Serial port for Arduino (auto-detect if None)
            target_error: Target alignment error in arcseconds
        """
        self.software = software
        self.target_error = target_error
        self.controller = PolarAlignController(port)
        
        # Load calibration from Arduino
        self.calibration = self.get_calibration()
        
        # Log file configuration
        self.log_patterns = {
            'sharpcap': {
                'path': self.get_sharpcap_log_path(),
                'pattern': r'(?:Info)\W*(\d{2}:\d{2}:\d{2}\.\d{6}).*(?:AltAzCor=)(?:Alt=)([-\d.]+)[,](?:Az=)([-\d.]+)',
                'name': 'SharpCap'
            },
            'nina': {
                'path': self.get_nina_log_path(),
                'pattern': r'(\d{2}:\d{2}:\d{2}\.\d{3})\s-\s(\{.*\})',
                'name': 'NINA'
            }
        }
        
        self.last_entry_time = None
        self.iteration = 0
        
    def get_sharpcap_log_path(self):
        """Get SharpCap log file path"""
        base_path = Path(os.getenv('LOCALAPPDATA', '')) / 'SharpCap' / 'logs'
        if not base_path.exists():
            print(f"WARNING: SharpCap log directory not found: {base_path}")
            return None
        
        # Get most recent log file
        try:
            log_files = list(base_path.glob('*.log'))
            if not log_files:
                print(f"WARNING: No log files found in {base_path}")
                return None
            latest_log = max(log_files, key=os.path.getmtime)
            return latest_log
        except Exception as e:
            print(f"ERROR: Could not find SharpCap log: {e}")
            return None
    
    def get_nina_log_path(self):
        """Get NINA log file path"""
        today = datetime.now().strftime("%Y-%m-%d")
        base_path = Path.home() / 'Documents' / 'N.I.N.A' / 'PolarAlignment'
        
        if not base_path.exists():
            print(f"WARNING: NINA log directory not found: {base_path}")
            return None
        
        log_file = base_path / f'{today}.log'
        if not log_file.exists():
            print(f"WARNING: NINA log for today not found: {log_file}")
            return None
        
        return log_file
    
    def get_calibration(self):
        """Retrieve calibration from Arduino"""
        print("Loading calibration from Arduino...")
        response = self.controller.send_command('CAL:SHOW')
        
        # Parse calibration response
        cal = {
            'alt_steps_per_arcsec': 89.5,  # Default
            'az_steps_per_arcsec': 25.0,   # Default
            'alt_backlash': 0,
            'az_backlash': 0,
            'calibrated': False
        }
        
        # Try to parse actual calibration
        for line in response.split('\n'):
            if 'ALT:' in line and 'steps/arcsec' in line:
                try:
                    val = float(re.search(r'([\d.]+)\s+steps/arcsec', line).group(1))
                    cal['alt_steps_per_arcsec'] = val
                    cal['calibrated'] = True
                except:
                    pass
            elif 'AZ:' in line and 'steps/arcsec' in line:
                try:
                    val = float(re.search(r'([\d.]+)\s+steps/arcsec', line).group(1))
                    cal['az_steps_per_arcsec'] = val
                except:
                    pass
        
        if not cal['calibrated']:
            print("WARNING: Using default calibration values")
            print("Run calibration_wizard.py for accurate results")
        else:
            print(f"✓ Calibration loaded:")
            print(f"  ALT: {cal['alt_steps_per_arcsec']:.2f} steps/arcsec")
            print(f"  AZ:  {cal['az_steps_per_arcsec']:.2f} steps/arcsec")
        
        return cal
    
    def parse_sharpcap_log_entry(self, line):
        """Parse SharpCap log entry"""
        pattern = self.log_patterns['sharpcap']['pattern']
        match = re.search(pattern, line)
        
        if match:
            timestamp = match.group(1)
            alt_error = float(match.group(2))  # arcminutes
            az_error = float(match.group(3))   # arcminutes
            
            # Convert arcminutes to arcseconds
            alt_error *= 60.0
            az_error *= 60.0
            
            return {
                'timestamp': timestamp,
                'alt_error': alt_error,
                'az_error': az_error,
                'total_error': (alt_error**2 + az_error**2)**0.5
            }
        
        return None
    
    def parse_nina_log_entry(self, line):
        """Parse NINA log entry"""
        pattern = self.log_patterns['nina']['pattern']
        match = re.search(pattern, line)
        
        if match:
            timestamp = match.group(1)
            json_str = match.group(2)
            
            try:
                import json
                data = json.loads(json_str)
                
                return {
                    'timestamp': timestamp,
                    'alt_error': data.get('Alt', 0),
                    'az_error': data.get('Az', 0),
                    'total_error': data.get('Total', 0)
                }
            except:
                return None
        
        return None
    
    def monitor_logs(self):
        """Monitor log files for polar alignment corrections"""
        config = self.log_patterns[self.software]
        log_path = config['path']
        
        if not log_path or not Path(log_path).exists():
            print(f"ERROR: Log file not found for {config['name']}")
            print(f"Expected: {log_path}")
            print("\nMake sure you:")
            print(f"1. Have {config['name']} installed")
            print(f"2. Started the Polar Alignment routine")
            print(f"3. {config['name']} has created a log file")
            return
        
        print(f"\n{'='*70}")
        print(f"  Automatic Polar Alignment - {config['name']} Integration")
        print(f"{'='*70}\n")
        print(f"Monitoring: {log_path}")
        print(f"Target accuracy: {self.target_error} arcseconds")
        print(f"\nWaiting for {config['name']} polar alignment to start...")
        print("(Start the polar alignment routine in the software now)\n")
        
        last_position = 0
        if Path(log_path).exists():
            # Start from end of file
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                f.seek(0, 2)  # Seek to end
                last_position = f.tell()
        
        try:
            while True:
                if not Path(log_path).exists():
                    print(f"WARNING: Log file disappeared: {log_path}")
                    time.sleep(5)
                    continue
                
                with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = f.tell()
                    
                    for line in new_lines:
                        # Parse based on software
                        if self.software == 'sharpcap':
                            error = self.parse_sharpcap_log_entry(line)
                        else:
                            error = self.parse_nina_log_entry(line)
                        
                        if error:
                            self.process_alignment_error(error)
                
                time.sleep(1)  # Check every second
                
        except KeyboardInterrupt:
            print("\n\nAutoPA stopped by user")
            self.controller.send_command('D')  # Disable motors
            print("Motors disabled")
    
    def process_alignment_error(self, error):
        """Process polar alignment error and adjust mount"""
        self.iteration += 1
        
        print(f"\n{'─'*70}")
        print(f"Iteration #{self.iteration} - {error['timestamp']}")
        print(f"{'─'*70}")
        print(f"Polar Alignment Error:")
        print(f"  ALT: {error['alt_error']:+7.2f} arcseconds")
        print(f"  AZ:  {error['az_error']:+7.2f} arcseconds")
        print(f"  TOTAL: {error['total_error']:6.2f} arcseconds")
        
        # Check if we've achieved target
        if error['total_error'] < self.target_error:
            print(f"\n{'='*70}")
            print(f"  ✓ POLAR ALIGNMENT ACHIEVED!")
            print(f"{'='*70}")
            print(f"Final error: {error['total_error']:.2f} arcseconds")
            print(f"Iterations: {self.iteration}")
            print(f"\nYou may now start imaging!")
            
            # Disable motors
            self.controller.send_command('D')
            sys.exit(0)
        
        # Calculate corrections
        alt_steps = int(error['alt_error'] * self.calibration['alt_steps_per_arcsec'])
        az_steps = int(error['az_error'] * self.calibration['az_steps_per_arcsec'])
        
        print(f"\nCalculating corrections:")
        print(f"  ALT: {alt_steps:+6d} steps ({error['alt_error']:.1f} * {self.calibration['alt_steps_per_arcsec']:.1f})")
        print(f"  AZ:  {az_steps:+6d} steps ({error['az_error']:.1f} * {self.calibration['az_steps_per_arcsec']:.1f})")
        
        # Safety check
        max_steps = 50000
        if abs(alt_steps) > max_steps or abs(az_steps) > max_steps:
            print(f"\nWARNING: Correction exceeds safety limit ({max_steps} steps)")
            print("This might indicate:")
            print("  - Incorrect calibration")
            print("  - Mount is far from polar alignment")
            print("  - Error in plate solving")
            print("\nSkipping this correction for safety.")
            return
        
        # Send corrections
        print(f"\nAdjusting mount...")
        
        # Enable motors
        self.controller.send_command('E')
        
        # Move ALT
        if alt_steps != 0:
            print(f"  Moving ALT {alt_steps:+d} steps...")
            self.controller.send_command(f'A{alt_steps}')
        
        # Move AZ
        if az_steps != 0:
            print(f"  Moving AZ {az_steps:+d} steps...")
            self.controller.send_command(f'Z{az_steps}')
        
        print(f"  ✓ Movement complete")
        print(f"\nWaiting for {self.log_patterns[self.software]['name']} to re-solve...")
    
    def run(self):
        """Run automatic polar alignment"""
        try:
            self.monitor_logs()
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Always disable motors on exit
            try:
                self.controller.send_command('D')
            except:
                pass

def main():
    parser = argparse.ArgumentParser(
        description='Automatic Polar Alignment for Star Adventurer GTi',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python plate_solving_autopa.py --software sharpcap
    python plate_solving_autopa.py --software nina --target 20
    python plate_solving_autopa.py --port COM3 --target 30

Supported Software:
    sharpcap - SharpCap Pro (requires paid license)
    nina     - NINA with Three Point Polar Alignment plugin (free)

Workflow:
    1. Start this script first
    2. Open SharpCap or NINA
    3. Start the Polar Alignment routine
    4. Watch the mount automatically adjust
    5. Script exits when target accuracy achieved
"""
    )
    
    parser.add_argument('--software', '-s',
                      choices=['sharpcap', 'nina'],
                      default='sharpcap',
                      help='Plate solving software to use')
    
    parser.add_argument('--port', '-p',
                      help='Serial port (auto-detect if not specified)')
    
    parser.add_argument('--target', '-t',
                      type=float,
                      default=30.0,
                      help='Target alignment error in arcseconds (default: 30)')
    
    args = parser.parse_args()
    
    print("""
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║    Star Adventurer GTi - Automatic Polar Alignment            ║
║    Plate Solving Integration                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
    """)
    
    autopa = PlateS olvingAutoPA(
        software=args.software,
        port=args.port,
        target_error=args.target
    )
    
    autopa.run()

if __name__ == '__main__':
    main()

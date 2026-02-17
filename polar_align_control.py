#!/usr/bin/env python3
"""
Star Adventurer GTi - Polar Alignment Control Software

This software provides control over the automated polar alignment motors
for the Sky-Watcher Star Adventurer GTi mount.

Features:
- Serial communication with Arduino controller
- Manual motor control
- Position tracking
- Speed adjustment
- Simple CLI interface

Requirements:
- Python 3.7+
- pyserial

Author: Polar Align Automation Project
Version: 1.0
"""

import serial
import serial.tools.list_ports
import time
import sys
import threading
from typing import Optional, Tuple


class PolarAlignController:
    """
    Controller class for Star Adventurer GTi polar alignment automation
    """
    
    def __init__(self, port: Optional[str] = None, baudrate: int = 115200):
        """
        Initialize the controller
        
        Args:
            port: Serial port name (e.g., 'COM3' or '/dev/ttyUSB0')
            baudrate: Serial communication speed
        """
        self.port = port
        self.baudrate = baudrate
        self.serial: Optional[serial.Serial] = None
        self.connected = False
        self.alt_position = 0
        self.az_position = 0
        self.current_speed = 800
        
        # Movement presets (in steps)
        self.FINE_STEP = 10      # Very fine adjustment
        self.SMALL_STEP = 50     # Small adjustment
        self.MEDIUM_STEP = 200   # Medium adjustment
        self.LARGE_STEP = 800    # Large adjustment
        
    def list_ports(self) -> list:
        """
        List all available serial ports
        
        Returns:
            List of available port names
        """
        ports = serial.tools.list_ports.comports()
        return [port.device for port in ports]
    
    def connect(self, port: Optional[str] = None) -> bool:
        """
        Connect to the Arduino controller
        
        Args:
            port: Serial port to connect to (uses auto-detect if None)
            
        Returns:
            True if connection successful, False otherwise
        """
        if port:
            self.port = port
            
        if not self.port:
            # Try to auto-detect Arduino
            ports = self.list_ports()
            if not ports:
                print("ERROR: No serial ports found")
                return False
            
            # Try each port
            for p in ports:
                try:
                    print(f"Trying port {p}...")
                    test_serial = serial.Serial(p, self.baudrate, timeout=2)
                    time.sleep(2)  # Wait for Arduino reset
                    
                    # Check for READY message
                    if test_serial.in_waiting:
                        response = test_serial.readline().decode('utf-8').strip()
                        if 'READY' in response:
                            self.port = p
                            self.serial = test_serial
                            self.connected = True
                            print(f"Connected to {p}")
                            
                            # Read startup messages
                            time.sleep(0.5)
                            while self.serial.in_waiting:
                                msg = self.serial.readline().decode('utf-8').strip()
                                print(msg)
                            
                            return True
                    
                    test_serial.close()
                except Exception as e:
                    continue
            
            print("ERROR: Could not auto-detect controller")
            return False
        
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino reset
            
            # Check for READY message
            if self.serial.in_waiting:
                response = self.serial.readline().decode('utf-8').strip()
                if 'READY' in response:
                    self.connected = True
                    print(f"Connected to {self.port}")
                    
                    # Read startup messages
                    time.sleep(0.5)
                    while self.serial.in_waiting:
                        msg = self.serial.readline().decode('utf-8').strip()
                        print(msg)
                    
                    return True
            
            return False
            
        except Exception as e:
            print(f"ERROR: Connection failed - {e}")
            return False
    
    def disconnect(self):
        """Disconnect from the controller"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            self.connected = False
            print("Disconnected")
    
    def send_command(self, command: str) -> Optional[str]:
        """
        Send a command to the controller
        
        Args:
            command: Command string to send
            
        Returns:
            Response from controller or None if error
        """
        if not self.connected or not self.serial:
            print("ERROR: Not connected")
            return None
        
        try:
            # Send command
            self.serial.write(f"{command}\n".encode('utf-8'))
            self.serial.flush()
            
            # Wait for response
            time.sleep(0.1)
            
            # Read response
            if self.serial.in_waiting:
                response = self.serial.readline().decode('utf-8').strip()
                return response
            
            return None
            
        except Exception as e:
            print(f"ERROR: Command failed - {e}")
            return None
    
    def move_altitude(self, steps: int) -> bool:
        """
        Move altitude motor
        
        Args:
            steps: Number of steps (positive = up, negative = down)
            
        Returns:
            True if successful
        """
        response = self.send_command(f"A{steps}")
        if response and 'OK:ALT_MOVE' in response:
            print(f"Altitude moved {steps} steps")
            self.update_position()
            return True
        return False
    
    def move_azimuth(self, steps: int) -> bool:
        """
        Move azimuth motor
        
        Args:
            steps: Number of steps (positive = CW, negative = CCW)
            
        Returns:
            True if successful
        """
        response = self.send_command(f"Z{steps}")
        if response and 'OK:AZ_MOVE' in response:
            print(f"Azimuth moved {steps} steps")
            self.update_position()
            return True
        return False
    
    def stop(self) -> bool:
        """
        Stop all motor movement
        
        Returns:
            True if successful
        """
        response = self.send_command("S")
        if response and 'OK:STOPPED' in response:
            print("Motors stopped")
            return True
        return False
    
    def enable_motors(self, enable: bool = True) -> bool:
        """
        Enable or disable motors
        
        Args:
            enable: True to enable, False to disable
            
        Returns:
            True if successful
        """
        command = "E" if enable else "D"
        response = self.send_command(command)
        
        if response:
            if enable and 'OK:ENABLED' in response:
                print("Motors enabled")
                return True
            elif not enable and 'OK:DISABLED' in response:
                print("Motors disabled")
                return True
        return False
    
    def get_position(self) -> Tuple[int, int]:
        """
        Get current motor positions
        
        Returns:
            Tuple of (altitude_position, azimuth_position)
        """
        response = self.send_command("P")
        if response and response.startswith('POS:'):
            # Parse: POS:ALT:1234:AZ:5678
            parts = response.split(':')
            if len(parts) >= 5:
                self.alt_position = int(parts[2])
                self.az_position = int(parts[4])
                return (self.alt_position, self.az_position)
        
        return (0, 0)
    
    def update_position(self):
        """Update internal position tracking"""
        self.get_position()
    
    def reset_position(self) -> bool:
        """
        Reset position counters to zero
        
        Returns:
            True if successful
        """
        response = self.send_command("R")
        if response and 'OK:RESET' in response:
            self.alt_position = 0
            self.az_position = 0
            print("Position reset to 0,0")
            return True
        return False
    
    def set_speed(self, speed: int) -> bool:
        """
        Set motor speed
        
        Args:
            speed: Speed in steps per second (1-2000)
            
        Returns:
            True if successful
        """
        if speed < 1 or speed > 2000:
            print("ERROR: Speed must be between 1 and 2000")
            return False
        
        response = self.send_command(f"V{speed}")
        if response and 'OK:SPEED' in response:
            self.current_speed = speed
            print(f"Speed set to {speed} steps/sec")
            return True
        return False
    
    def get_status(self) -> dict:
        """
        Get controller status
        
        Returns:
            Dictionary with status information
        """
        response = self.send_command("?")
        
        status = {
            'connected': self.connected,
            'alt_position': self.alt_position,
            'az_position': self.az_position,
            'speed': self.current_speed
        }
        
        if response:
            print(response)
            # Read multi-line status
            time.sleep(0.2)
            while self.serial.in_waiting:
                line = self.serial.readline().decode('utf-8').strip()
                print(line)
        
        return status


def print_menu():
    """Print the main menu"""
    print("\n" + "="*60)
    print("STAR ADVENTURER GTi - POLAR ALIGNMENT CONTROLLER")
    print("="*60)
    print("\nALTITUDE CONTROLS:")
    print("  Q/W/E/R - Move UP (Fine/Small/Medium/Large)")
    print("  A/S/D/F - Move DOWN (Fine/Small/Medium/Large)")
    print("\nAZIMUTH CONTROLS:")
    print("  T/Y/U/I - Move CCW (Fine/Small/Medium/Large)")
    print("  G/H/J/K - Move CW (Fine/Small/Medium/Large)")
    print("\nOTHER COMMANDS:")
    print("  P - Get current position")
    print("  0 - Reset position to 0,0")
    print("  V - Set speed")
    print("  X - Stop all motors")
    print("  + - Enable motors")
    print("  - - Disable motors")
    print("  ? - Show status")
    print("  M - Show this menu")
    print("  C - Clear position display")
    print("  Q - Quit")
    print("="*60)


def main():
    """Main control loop"""
    print("Star Adventurer GTi Polar Alignment Controller")
    print("Version 1.0\n")
    
    # Create controller
    controller = PolarAlignController()
    
    # List available ports
    ports = controller.list_ports()
    if ports:
        print("Available serial ports:")
        for i, port in enumerate(ports):
            print(f"  {i+1}. {port}")
        print()
    
    # Connect
    print("Attempting to connect...")
    if not controller.connect():
        print("Failed to connect to controller")
        
        # Manual port selection
        if ports:
            try:
                choice = input("Enter port number to try manually (or 'q' to quit): ")
                if choice.lower() == 'q':
                    return
                
                port_idx = int(choice) - 1
                if 0 <= port_idx < len(ports):
                    if not controller.connect(ports[port_idx]):
                        print("Connection failed. Exiting.")
                        return
                else:
                    print("Invalid port number. Exiting.")
                    return
            except ValueError:
                print("Invalid input. Exiting.")
                return
        else:
            return
    
    # Show menu
    print_menu()
    
    # Main control loop
    try:
        while True:
            command = input("\nCommand (M for menu): ").strip().upper()
            
            if not command:
                continue
            
            # Altitude controls
            if command == 'Q':
                controller.move_altitude(controller.FINE_STEP)
            elif command == 'W':
                controller.move_altitude(controller.SMALL_STEP)
            elif command == 'E':
                controller.move_altitude(controller.MEDIUM_STEP)
            elif command == 'R':
                controller.move_altitude(controller.LARGE_STEP)
            elif command == 'A':
                controller.move_altitude(-controller.FINE_STEP)
            elif command == 'S':
                controller.move_altitude(-controller.SMALL_STEP)
            elif command == 'D':
                controller.move_altitude(-controller.MEDIUM_STEP)
            elif command == 'F':
                controller.move_altitude(-controller.LARGE_STEP)
            
            # Azimuth controls
            elif command == 'T':
                controller.move_azimuth(-controller.FINE_STEP)
            elif command == 'Y':
                controller.move_azimuth(-controller.SMALL_STEP)
            elif command == 'U':
                controller.move_azimuth(-controller.MEDIUM_STEP)
            elif command == 'I':
                controller.move_azimuth(-controller.LARGE_STEP)
            elif command == 'G':
                controller.move_azimuth(controller.FINE_STEP)
            elif command == 'H':
                controller.move_azimuth(controller.SMALL_STEP)
            elif command == 'J':
                controller.move_azimuth(controller.MEDIUM_STEP)
            elif command == 'K':
                controller.move_azimuth(controller.LARGE_STEP)
            
            # Other commands
            elif command == 'P':
                alt, az = controller.get_position()
                print(f"Position - ALT: {alt} steps, AZ: {az} steps")
            
            elif command == '0':
                controller.reset_position()
            
            elif command == 'V':
                try:
                    speed = int(input("Enter speed (1-2000 steps/sec): "))
                    controller.set_speed(speed)
                except ValueError:
                    print("Invalid speed value")
            
            elif command == 'X':
                controller.stop()
            
            elif command == '+':
                controller.enable_motors(True)
            
            elif command == '-':
                controller.enable_motors(False)
            
            elif command == '?':
                controller.get_status()
            
            elif command == 'M':
                print_menu()
            
            elif command == 'C':
                # Clear screen (simple version)
                print("\n" * 50)
                print_menu()
            
            elif command == 'QUIT' or command == 'EXIT':
                break
            
            else:
                print(f"Unknown command: {command}")
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
    
    finally:
        # Cleanup
        controller.stop()
        controller.enable_motors(False)
        controller.disconnect()
        print("Goodbye!")


if __name__ == "__main__":
    main()

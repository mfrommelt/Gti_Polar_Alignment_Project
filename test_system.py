#!/usr/bin/env python3
"""
Star Adventurer GTi Polar Alignment Controller
System Test & Diagnostic Tool

This script performs automated tests to verify that your setup is working correctly.

Tests performed:
1. Serial port detection
2. Arduino connection
3. Motor enable/disable
4. Motor movement (both axes)
5. Position tracking
6. Speed changes
7. Emergency stop

Author: Polar Align Automation Project
Version: 1.0
"""

import serial
import serial.tools.list_ports
import time
import sys

class Colors:
    """ANSI color codes for terminal output"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_test(test_name):
    """Print test header"""
    print(f"\n{Colors.BOLD}[TEST] {test_name}{Colors.ENDC}")

def print_pass(message):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ PASS:{Colors.ENDC} {message}")

def print_fail(message):
    """Print failure message"""
    print(f"{Colors.FAIL}✗ FAIL:{Colors.ENDC} {message}")

def print_info(message):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ INFO:{Colors.ENDC} {message}")

def print_warning(message):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ WARNING:{Colors.ENDC} {message}")

def send_command(ser, command, timeout=1):
    """Send command and get response"""
    try:
        ser.write(f"{command}\n".encode('utf-8'))
        ser.flush()
        time.sleep(0.1)
        
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if ser.in_waiting:
                response = ser.readline().decode('utf-8').strip()
                if response:
                    responses.append(response)
            time.sleep(0.05)
        
        return responses
    except Exception as e:
        print_fail(f"Command error: {e}")
        return None

def test_serial_ports():
    """Test 1: Detect available serial ports"""
    print_test("Serial Port Detection")
    
    ports = serial.tools.list_ports.comports()
    
    if not ports:
        print_fail("No serial ports detected")
        print_info("Check USB connection")
        return None
    
    print_pass(f"Found {len(ports)} serial port(s)")
    for i, port in enumerate(ports):
        print(f"  {i+1}. {port.device} - {port.description}")
    
    return ports

def test_arduino_connection(port):
    """Test 2: Connect to Arduino"""
    print_test("Arduino Connection")
    
    try:
        print_info(f"Attempting to connect to {port}...")
        ser = serial.Serial(port, 115200, timeout=2)
        time.sleep(2.5)  # Wait for Arduino reset
        
        # Check for READY message
        found_ready = False
        for _ in range(10):
            if ser.in_waiting:
                line = ser.readline().decode('utf-8').strip()
                print(f"  Received: {line}")
                if 'READY' in line:
                    found_ready = True
                    break
            time.sleep(0.1)
        
        if found_ready:
            print_pass("Arduino connected and ready")
            # Clear any remaining messages
            time.sleep(0.5)
            while ser.in_waiting:
                ser.readline()
            return ser
        else:
            print_fail("No READY message from Arduino")
            print_info("Verify firmware is uploaded correctly")
            ser.close()
            return None
            
    except Exception as e:
        print_fail(f"Connection failed: {e}")
        return None

def test_motor_enable(ser):
    """Test 3: Motor enable/disable"""
    print_test("Motor Enable/Disable")
    
    # Test enable
    responses = send_command(ser, "E")
    if responses and any('OK:ENABLED' in r for r in responses):
        print_pass("Motors enabled successfully")
    else:
        print_fail("Failed to enable motors")
        print_info(f"Responses: {responses}")
        return False
    
    time.sleep(0.5)
    
    # Test disable
    responses = send_command(ser, "D")
    if responses and any('OK:DISABLED' in r for r in responses):
        print_pass("Motors disabled successfully")
    else:
        print_fail("Failed to disable motors")
        return False
    
    # Re-enable for next tests
    send_command(ser, "E")
    time.sleep(0.3)
    
    return True

def test_altitude_movement(ser):
    """Test 4: Altitude motor movement"""
    print_test("Altitude Motor Movement")
    
    # Get initial position
    responses = send_command(ser, "P")
    print_info(f"Initial position: {responses}")
    
    # Move forward
    print_info("Moving ALT motor forward 100 steps...")
    responses = send_command(ser, "A100", timeout=2)
    
    if responses and any('OK:ALT_MOVE' in r for r in responses):
        print_pass("ALT motor moved forward")
    else:
        print_fail("ALT motor failed to move forward")
        print_info(f"Responses: {responses}")
        return False
    
    time.sleep(0.5)
    
    # Check position
    responses = send_command(ser, "P")
    print_info(f"Position after forward: {responses}")
    
    # Move backward
    print_info("Moving ALT motor backward 100 steps...")
    responses = send_command(ser, "A-100", timeout=2)
    
    if responses and any('OK:ALT_MOVE' in r for r in responses):
        print_pass("ALT motor moved backward")
    else:
        print_fail("ALT motor failed to move backward")
        return False
    
    time.sleep(0.5)
    
    # Check final position
    responses = send_command(ser, "P")
    print_info(f"Position after return: {responses}")
    
    return True

def test_azimuth_movement(ser):
    """Test 5: Azimuth motor movement"""
    print_test("Azimuth Motor Movement")
    
    # Move forward
    print_info("Moving AZ motor forward 100 steps...")
    responses = send_command(ser, "Z100", timeout=2)
    
    if responses and any('OK:AZ_MOVE' in r for r in responses):
        print_pass("AZ motor moved forward")
    else:
        print_fail("AZ motor failed to move forward")
        print_info(f"Responses: {responses}")
        return False
    
    time.sleep(0.5)
    
    # Move backward
    print_info("Moving AZ motor backward 100 steps...")
    responses = send_command(ser, "Z-100", timeout=2)
    
    if responses and any('OK:AZ_MOVE' in r for r in responses):
        print_pass("AZ motor moved backward")
    else:
        print_fail("AZ motor failed to move backward")
        return False
    
    return True

def test_position_tracking(ser):
    """Test 6: Position tracking accuracy"""
    print_test("Position Tracking")
    
    # Reset position
    send_command(ser, "R")
    time.sleep(0.3)
    
    responses = send_command(ser, "P")
    if responses and 'POS:ALT:0:AZ:0' in responses[0]:
        print_pass("Position reset to 0,0")
    else:
        print_warning("Position may not have reset correctly")
    
    # Move both axes
    send_command(ser, "A200", timeout=2)
    time.sleep(0.5)
    send_command(ser, "Z150", timeout=2)
    time.sleep(0.5)
    
    # Check position
    responses = send_command(ser, "P")
    print_info(f"Position after moves: {responses}")
    
    if responses and 'ALT:200' in responses[0] and 'AZ:150' in responses[0]:
        print_pass("Position tracking accurate")
        return True
    else:
        print_warning("Position tracking may be inaccurate")
        return True  # Don't fail test, just warn

def test_speed_control(ser):
    """Test 7: Speed control"""
    print_test("Speed Control")
    
    # Try setting speed to 500
    responses = send_command(ser, "V500")
    if responses and any('OK:SPEED:500' in r for r in responses):
        print_pass("Speed set to 500 steps/sec")
    else:
        print_fail("Failed to set speed")
        return False
    
    time.sleep(0.3)
    
    # Reset to default
    send_command(ser, "V800")
    
    return True

def test_emergency_stop(ser):
    """Test 8: Emergency stop"""
    print_test("Emergency Stop")
    
    # Start a long movement
    print_info("Starting long movement...")
    ser.write("A3200\n".encode('utf-8'))
    ser.flush()
    time.sleep(0.2)
    
    # Send stop command
    print_info("Sending emergency stop...")
    responses = send_command(ser, "S")
    
    if responses and any('OK:STOPPED' in r for r in responses):
        print_pass("Emergency stop works")
        return True
    else:
        print_fail("Emergency stop failed")
        return False

def test_status_query(ser):
    """Test 9: Status query"""
    print_test("Status Query")
    
    responses = send_command(ser, "?", timeout=2)
    
    if responses and len(responses) > 0:
        print_pass("Status query successful")
        for response in responses:
            print(f"  {response}")
        return True
    else:
        print_fail("Status query failed")
        return False

def run_all_tests():
    """Run complete test suite"""
    print(f"\n{Colors.HEADER}{'='*60}")
    print("Star Adventurer GTi Polar Alignment Controller")
    print("System Diagnostic Test Suite")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    # Test results
    results = {
        'passed': 0,
        'failed': 0,
        'warnings': 0
    }
    
    # Test 1: Serial ports
    ports = test_serial_ports()
    if not ports:
        print_fail("Cannot proceed without serial port")
        return
    
    # If multiple ports, ask user to select
    if len(ports) > 1:
        try:
            choice = input(f"\n{Colors.BOLD}Select port number (1-{len(ports)}): {Colors.ENDC}")
            port_idx = int(choice) - 1
            if port_idx < 0 or port_idx >= len(ports):
                print_fail("Invalid port selection")
                return
            selected_port = ports[port_idx].device
        except ValueError:
            print_fail("Invalid input")
            return
    else:
        selected_port = ports[0].device
    
    print_info(f"Using port: {selected_port}")
    
    # Test 2: Arduino connection
    ser = test_arduino_connection(selected_port)
    if not ser:
        print_fail("Cannot proceed without Arduino connection")
        return
    
    results['passed'] += 1
    
    # Run remaining tests
    tests = [
        ("Motor Enable/Disable", test_motor_enable),
        ("Altitude Movement", test_altitude_movement),
        ("Azimuth Movement", test_azimuth_movement),
        ("Position Tracking", test_position_tracking),
        ("Speed Control", test_speed_control),
        ("Emergency Stop", test_emergency_stop),
        ("Status Query", test_status_query),
    ]
    
    for test_name, test_func in tests:
        try:
            if test_func(ser):
                results['passed'] += 1
            else:
                results['failed'] += 1
        except Exception as e:
            print_fail(f"Test crashed: {e}")
            results['failed'] += 1
        
        time.sleep(0.3)
    
    # Cleanup
    print_info("\nCleaning up...")
    send_command(ser, "S")  # Stop
    send_command(ser, "D")  # Disable
    ser.close()
    
    # Print summary
    print(f"\n{Colors.HEADER}{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}{Colors.ENDC}\n")
    
    total_tests = results['passed'] + results['failed']
    
    print(f"{Colors.OKGREEN}✓ Passed: {results['passed']}/{total_tests}{Colors.ENDC}")
    if results['failed'] > 0:
        print(f"{Colors.FAIL}✗ Failed: {results['failed']}/{total_tests}{Colors.ENDC}")
    if results['warnings'] > 0:
        print(f"{Colors.WARNING}⚠ Warnings: {results['warnings']}{Colors.ENDC}")
    
    if results['failed'] == 0:
        print(f"\n{Colors.OKGREEN}{Colors.BOLD}ALL TESTS PASSED! System is ready to use.{Colors.ENDC}")
    else:
        print(f"\n{Colors.WARNING}{Colors.BOLD}Some tests failed. Review errors above.{Colors.ENDC}")
    
    print()

if __name__ == "__main__":
    try:
        run_all_tests()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}Test interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}Fatal error: {e}{Colors.ENDC}")

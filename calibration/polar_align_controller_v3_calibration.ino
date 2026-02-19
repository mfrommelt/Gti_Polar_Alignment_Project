/*
 * Star Adventurer GTi - Automated Polar Alignment Controller
 * DIFFERENTIAL AZIMUTH VERSION WITH CALIBRATION
 * 
 * Version: 3.0 - Adds calibration routines for steps/arcsec and backlash
 * 
 * New Features:
 * - Calibration mode for measuring steps per arcsecond
 * - Backlash detection and compensation
 * - EEPROM storage of calibration data
 * - Automatic backlash compensation in movements
 * 
 * Commands:
 * Basic:
 *   A<steps> - Move altitude
 *   Z<steps> - Move azimuth (differential)
 *   S - Stop all motors
 *   P - Get position
 *   R - Reset position to 0,0
 *   V<speed> - Set speed (1-2000)
 *   E - Enable motors
 *   D - Disable motors
 *   ? - Status
 * 
 * Calibration:
 *   CAL:ALT:<arcsec>:<steps> - Set ALT calibration (arcsec moved in steps)
 *   CAL:AZ:<arcsec>:<steps> - Set AZ calibration  
 *   CAL:ALTBL:<steps> - Set ALT backlash
 *   CAL:AZBL:<steps> - Set AZ backlash
 *   CAL:SAVE - Save calibration to EEPROM
 *   CAL:LOAD - Load calibration from EEPROM
 *   CAL:SHOW - Display current calibration
 *   CAL:RESET - Reset to defaults
 */

#include <EEPROM.h>

// ============================================
// PIN DEFINITIONS
// ============================================
#define ALT_STEP_PIN 2
#define ALT_DIR_PIN 3
#define ALT_ENABLE_PIN 4

#define AZ_WEST_STEP_PIN 5
#define AZ_WEST_DIR_PIN 6
#define AZ_WEST_ENABLE_PIN 7

#define AZ_EAST_STEP_PIN 8
#define AZ_EAST_DIR_PIN 9
#define AZ_EAST_ENABLE_PIN 10

// ============================================
// MOTOR PARAMETERS
// ============================================
#define STEPS_PER_REV 200
#define MICROSTEPS 16
#define MAX_SPEED 2000
#define MIN_PULSE_WIDTH 2

// ============================================
// CALIBRATION DATA STRUCTURE
// ============================================
struct CalibrationData {
  // Magic number to verify EEPROM data is valid
  uint16_t magic;
  
  // Steps per arcsecond (calculated from measurements)
  float altStepsPerArcsec;
  float azStepsPerArcsec;
  
  // Backlash in steps (dead zone when reversing direction)
  int16_t altBacklash;
  int16_t azBacklash;
  
  // Maximum safe speed
  int16_t maxSpeed;
  
  // Calibration status
  bool isCalibrated;
  
  // Checksum for validation
  uint16_t checksum;
};

CalibrationData cal;

// EEPROM address for calibration data
#define CAL_EEPROM_ADDR 0
#define CAL_MAGIC 0xC411  // Magic number to verify valid data

// ============================================
// POSITION & MOVEMENT STATE
// ============================================
long altPosition = 0;
long azPosition = 0;

int altSpeed = 800;
int azSpeed = 800;

// Track last direction for backlash compensation
int lastAltDirection = 0;  // 0=unknown, 1=forward, -1=backward
int lastAzDirection = 0;

bool isMoving = false;
String inputString = "";
bool stringComplete = false;

// ============================================
// CALIBRATION FUNCTIONS
// ============================================

uint16_t calculateChecksum(CalibrationData* data) {
  // Simple checksum: sum of all bytes except checksum field
  uint16_t sum = 0;
  byte* ptr = (byte*)data;
  int size = sizeof(CalibrationData) - sizeof(uint16_t);
  for (int i = 0; i < size; i++) {
    sum += ptr[i];
  }
  return sum;
}

void initCalibration() {
  // Default values (approximate estimates)
  cal.magic = CAL_MAGIC;
  
  // ALT: Assuming 4:1 belt + 90:1 worm = 360:1 total reduction
  // 3200 motor steps * 360 = 1,152,000 steps per 360 degrees
  // 1,152,000 / 360 / 3600 = 89 steps per arcsecond
  cal.altStepsPerArcsec = 89.0;
  
  // AZ: Assuming 3:1 belt reduction, differential screws
  // Estimate: 20-30 steps per arcsecond
  cal.azStepsPerArcsec = 25.0;
  
  cal.altBacklash = 0;
  cal.azBacklash = 0;
  cal.maxSpeed = 1000;
  cal.isCalibrated = false;
  cal.checksum = calculateChecksum(&cal);
}

void saveCalibration() {
  cal.checksum = calculateChecksum(&cal);
  EEPROM.put(CAL_EEPROM_ADDR, cal);
  Serial.println("OK:CAL_SAVED");
  Serial.print("INFO:Calibration saved to EEPROM at address ");
  Serial.println(CAL_EEPROM_ADDR);
}

bool loadCalibration() {
  CalibrationData temp;
  EEPROM.get(CAL_EEPROM_ADDR, temp);
  
  // Verify magic number and checksum
  if (temp.magic != CAL_MAGIC) {
    Serial.println("WARN:No valid calibration in EEPROM (magic mismatch)");
    return false;
  }
  
  uint16_t expectedChecksum = temp.checksum;
  temp.checksum = 0;
  uint16_t actualChecksum = calculateChecksum(&temp);
  
  if (expectedChecksum != actualChecksum) {
    Serial.println("WARN:Calibration checksum failed");
    return false;
  }
  
  // Data is valid, load it
  cal = temp;
  cal.checksum = expectedChecksum;
  Serial.println("OK:CAL_LOADED");
  return true;
}

void showCalibration() {
  Serial.println("=== CALIBRATION DATA ===");
  Serial.print("Calibrated: ");
  Serial.println(cal.isCalibrated ? "YES" : "NO");
  Serial.println();
  
  Serial.println("Steps per arcsecond:");
  Serial.print("  ALT: ");
  Serial.print(cal.altStepsPerArcsec, 2);
  Serial.println(" steps/arcsec");
  Serial.print("  AZ:  ");
  Serial.print(cal.azStepsPerArcsec, 2);
  Serial.println(" steps/arcsec");
  Serial.println();
  
  Serial.println("Backlash:");
  Serial.print("  ALT: ");
  Serial.print(cal.altBacklash);
  Serial.println(" steps");
  Serial.print("  AZ:  ");
  Serial.print(cal.azBacklash);
  Serial.println(" steps");
  Serial.println();
  
  Serial.print("Max Speed: ");
  Serial.print(cal.maxSpeed);
  Serial.println(" steps/sec");
  Serial.println("========================");
}

void processCalibrationCommand(String cmd) {
  // CAL:ALT:<arcsec>:<steps>
  if (cmd.startsWith("CAL:ALT:") && !cmd.startsWith("CAL:ALTBL:")) {
    int firstColon = cmd.indexOf(':', 8);
    if (firstColon > 0) {
      float arcsec = cmd.substring(8, firstColon).toFloat();
      int steps = cmd.substring(firstColon + 1).toInt();
      
      if (arcsec > 0 && steps > 0) {
        cal.altStepsPerArcsec = (float)steps / arcsec;
        cal.isCalibrated = true;
        Serial.println("OK:ALT_CAL_SET");
        Serial.print("INFO:ALT calibration: ");
        Serial.print(cal.altStepsPerArcsec, 2);
        Serial.println(" steps/arcsec");
      } else {
        Serial.println("ERROR:Invalid ALT calibration values");
      }
    }
  }
  
  // CAL:AZ:<arcsec>:<steps>
  else if (cmd.startsWith("CAL:AZ:") && !cmd.startsWith("CAL:AZBL:")) {
    int firstColon = cmd.indexOf(':', 7);
    if (firstColon > 0) {
      float arcsec = cmd.substring(7, firstColon).toFloat();
      int steps = cmd.substring(firstColon + 1).toInt();
      
      if (arcsec > 0 && steps > 0) {
        cal.azStepsPerArcsec = (float)steps / arcsec;
        cal.isCalibrated = true;
        Serial.println("OK:AZ_CAL_SET");
        Serial.print("INFO:AZ calibration: ");
        Serial.print(cal.azStepsPerArcsec, 2);
        Serial.println(" steps/arcsec");
      } else {
        Serial.println("ERROR:Invalid AZ calibration values");
      }
    }
  }
  
  // CAL:ALTBL:<steps>
  else if (cmd.startsWith("CAL:ALTBL:")) {
    int backlash = cmd.substring(10).toInt();
    if (backlash >= 0) {
      cal.altBacklash = backlash;
      Serial.println("OK:ALT_BACKLASH_SET");
      Serial.print("INFO:ALT backlash: ");
      Serial.print(cal.altBacklash);
      Serial.println(" steps");
    }
  }
  
  // CAL:AZBL:<steps>
  else if (cmd.startsWith("CAL:AZBL:")) {
    int backlash = cmd.substring(9).toInt();
    if (backlash >= 0) {
      cal.azBacklash = backlash;
      Serial.println("OK:AZ_BACKLASH_SET");
      Serial.print("INFO:AZ backlash: ");
      Serial.print(cal.azBacklash);
      Serial.println(" steps");
    }
  }
  
  // CAL:SAVE
  else if (cmd == "CAL:SAVE") {
    saveCalibration();
  }
  
  // CAL:LOAD
  else if (cmd == "CAL:LOAD") {
    if (loadCalibration()) {
      showCalibration();
    } else {
      Serial.println("ERROR:Failed to load calibration");
    }
  }
  
  // CAL:SHOW
  else if (cmd == "CAL:SHOW") {
    showCalibration();
  }
  
  // CAL:RESET
  else if (cmd == "CAL:RESET") {
    initCalibration();
    Serial.println("OK:CAL_RESET");
    Serial.println("INFO:Calibration reset to defaults");
    showCalibration();
  }
  
  else {
    Serial.println("ERROR:Unknown calibration command");
  }
}

// ============================================
// MOTOR CONTROL WITH BACKLASH COMPENSATION
// ============================================

void stepMotor(int stepPin) {
  digitalWrite(stepPin, HIGH);
  delayMicroseconds(MIN_PULSE_WIDTH);
  digitalWrite(stepPin, LOW);
  delayMicroseconds(MIN_PULSE_WIDTH);
}

void moveAltitude(long steps) {
  if (steps == 0) return;
  
  int direction = (steps > 0) ? 1 : -1;
  steps = abs(steps);
  
  // Backlash compensation
  if (lastAltDirection != 0 && lastAltDirection != direction && cal.altBacklash > 0) {
    Serial.print("INFO:Compensating ALT backlash: ");
    Serial.print(cal.altBacklash);
    Serial.println(" steps");
    
    // Take up backlash without counting position
    digitalWrite(ALT_DIR_PIN, direction > 0 ? HIGH : LOW);
    for (int i = 0; i < cal.altBacklash; i++) {
      stepMotor(ALT_STEP_PIN);
      delayMicroseconds(1000000 / altSpeed);
    }
  }
  
  lastAltDirection = direction;
  
  // Normal movement
  digitalWrite(ALT_DIR_PIN, direction > 0 ? HIGH : LOW);
  
  for (long i = 0; i < steps; i++) {
    stepMotor(ALT_STEP_PIN);
    altPosition += direction;
    delayMicroseconds(1000000 / altSpeed);
    
    // Check for stop command every 100 steps
    if (i % 100 == 0 && stringComplete) {
      break;
    }
  }
}

void moveAzimuthDifferential(long steps) {
  if (steps == 0) return;
  
  int direction = (steps > 0) ? 1 : -1;  // Positive = EAST
  steps = abs(steps);
  
  // Backlash compensation
  if (lastAzDirection != 0 && lastAzDirection != direction && cal.azBacklash > 0) {
    Serial.print("INFO:Compensating AZ backlash: ");
    Serial.print(cal.azBacklash);
    Serial.println(" steps");
    
    // Take up backlash in both motors
    if (direction > 0) {  // Moving EAST
      digitalWrite(AZ_WEST_DIR_PIN, HIGH);   // West forward
      digitalWrite(AZ_EAST_DIR_PIN, LOW);    // East backward
    } else {  // Moving WEST
      digitalWrite(AZ_WEST_DIR_PIN, LOW);    // West backward
      digitalWrite(AZ_EAST_DIR_PIN, HIGH);   // East forward
    }
    
    for (int i = 0; i < cal.azBacklash; i++) {
      stepMotor(AZ_WEST_STEP_PIN);
      stepMotor(AZ_EAST_STEP_PIN);
      delayMicroseconds(1000000 / azSpeed);
    }
  }
  
  lastAzDirection = direction;
  
  // Normal differential movement
  if (direction > 0) {  // Moving EAST
    digitalWrite(AZ_WEST_DIR_PIN, HIGH);   // Tighten west screw
    digitalWrite(AZ_EAST_DIR_PIN, LOW);    // Loosen east screw
  } else {  // Moving WEST
    digitalWrite(AZ_WEST_DIR_PIN, LOW);    // Loosen west screw
    digitalWrite(AZ_EAST_DIR_PIN, HIGH);   // Tighten east screw
  }
  
  for (long i = 0; i < steps; i++) {
    stepMotor(AZ_WEST_STEP_PIN);
    stepMotor(AZ_EAST_STEP_PIN);
    azPosition += direction;
    delayMicroseconds(1000000 / azSpeed);
    
    if (i % 100 == 0 && stringComplete) {
      break;
    }
  }
}

// ============================================
// COMMAND PROCESSING
// ============================================

void processCommand(String command) {
  command.trim();
  command.toUpperCase();
  
  if (command.length() == 0) return;
  
  // Calibration commands
  if (command.startsWith("CAL:")) {
    processCalibrationCommand(command);
    return;
  }
  
  // Movement commands
  if (command.startsWith("A")) {
    long steps = command.substring(1).toInt();
    moveAltitude(steps);
    Serial.println("OK:ALT_MOVE");
    return;
  }
  
  if (command.startsWith("Z")) {
    long steps = command.substring(1).toInt();
    moveAzimuthDifferential(steps);
    Serial.println("OK:AZ_MOVE");
    return;
  }
  
  // Stop
  if (command == "S") {
    digitalWrite(ALT_ENABLE_PIN, HIGH);
    digitalWrite(AZ_WEST_ENABLE_PIN, HIGH);
    digitalWrite(AZ_EAST_ENABLE_PIN, HIGH);
    Serial.println("OK:STOPPED");
    return;
  }
  
  // Position
  if (command == "P") {
    Serial.print("POS:ALT=");
    Serial.print(altPosition);
    Serial.print(",AZ=");
    Serial.println(azPosition);
    return;
  }
  
  // Reset position
  if (command == "R") {
    altPosition = 0;
    azPosition = 0;
    lastAltDirection = 0;
    lastAzDirection = 0;
    Serial.println("OK:RESET");
    return;
  }
  
  // Set speed
  if (command.startsWith("V")) {
    int speed = command.substring(1).toInt();
    if (speed > 0 && speed <= MAX_SPEED) {
      altSpeed = speed;
      azSpeed = speed;
      Serial.print("OK:SPEED=");
      Serial.println(speed);
    } else {
      Serial.println("ERROR:Invalid speed");
    }
    return;
  }
  
  // Enable motors
  if (command == "E") {
    digitalWrite(ALT_ENABLE_PIN, LOW);
    digitalWrite(AZ_WEST_ENABLE_PIN, LOW);
    digitalWrite(AZ_EAST_ENABLE_PIN, LOW);
    Serial.println("OK:ENABLED");
    return;
  }
  
  // Disable motors
  if (command == "D") {
    digitalWrite(ALT_ENABLE_PIN, HIGH);
    digitalWrite(AZ_WEST_ENABLE_PIN, HIGH);
    digitalWrite(AZ_EAST_ENABLE_PIN, HIGH);
    Serial.println("OK:DISABLED");
    return;
  }
  
  // Status
  if (command == "?") {
    Serial.println("=== STATUS ===");
    Serial.println("Firmware: v3.0 with Calibration");
    Serial.print("Position: ALT=");
    Serial.print(altPosition);
    Serial.print(", AZ=");
    Serial.println(azPosition);
    Serial.print("Speed: ");
    Serial.println(altSpeed);
    Serial.print("Calibrated: ");
    Serial.println(cal.isCalibrated ? "YES" : "NO");
    Serial.println("==============");
    return;
  }
  
  Serial.println("ERROR:Unknown command");
}

// ============================================
// SETUP
// ============================================

void setup() {
  Serial.begin(115200);
  while (!Serial) {
    ;
  }
  
  // Configure pins
  pinMode(ALT_STEP_PIN, OUTPUT);
  pinMode(ALT_DIR_PIN, OUTPUT);
  pinMode(ALT_ENABLE_PIN, OUTPUT);
  
  pinMode(AZ_WEST_STEP_PIN, OUTPUT);
  pinMode(AZ_WEST_DIR_PIN, OUTPUT);
  pinMode(AZ_WEST_ENABLE_PIN, OUTPUT);
  
  pinMode(AZ_EAST_STEP_PIN, OUTPUT);
  pinMode(AZ_EAST_DIR_PIN, OUTPUT);
  pinMode(AZ_EAST_ENABLE_PIN, OUTPUT);
  
  // Start with motors disabled
  digitalWrite(ALT_ENABLE_PIN, HIGH);
  digitalWrite(AZ_WEST_ENABLE_PIN, HIGH);
  digitalWrite(AZ_EAST_ENABLE_PIN, HIGH);
  
  // Initialize calibration
  initCalibration();
  
  // Try to load saved calibration
  if (!loadCalibration()) {
    Serial.println("INFO:Using default calibration values");
  }
  
  Serial.println("Star Adventurer GTi Polar Alignment Controller v3.0");
  Serial.println("With Calibration Support");
  Serial.println("Ready. Type '?' for status or 'CAL:SHOW' for calibration.");
  
  inputString.reserve(200);
}

// ============================================
// MAIN LOOP
// ============================================

void loop() {
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
}

void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    if (inChar == '\n') {
      stringComplete = true;
    } else if (inChar != '\r') {
      inputString += inChar;
    }
  }
}

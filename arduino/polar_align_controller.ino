/*
 * Star Adventurer GTi - Automated Polar Alignment Controller
 * DIFFERENTIAL AZIMUTH VERSION
 * 
 * Controls two stepper motors:
 * - ALT motor: Single knob control (independent)
 * - AZ motors: Dual opposing screws (synchronized differential)
 * 
 * AZ Control Logic:
 * - Moving WEST: Loosen west screw, tighten east screw
 * - Moving EAST: Tighten west screw, loosen east screw
 * - Both motors move simultaneously in opposite directions
 * 
 * Hardware:
 * - Arduino Nano/Uno
 * - 3x TMC2208/TMC2209 stepper drivers (1 for ALT, 2 for AZ)
 * - 3x NEMA 17 stepper motors
 * 
 * Author: Polar Align Automation Project
 * Version: 2.0 - Differential AZ Control
 */

// Pin definitions for Motor 1 (ALT - Altitude)
#define ALT_STEP_PIN 2
#define ALT_DIR_PIN 3
#define ALT_ENABLE_PIN 4

// Pin definitions for Motor 2 (AZ WEST screw)
#define AZ_WEST_STEP_PIN 5
#define AZ_WEST_DIR_PIN 6
#define AZ_WEST_ENABLE_PIN 7

// Pin definitions for Motor 3 (AZ EAST screw)
#define AZ_EAST_STEP_PIN 8
#define AZ_EAST_DIR_PIN 9
#define AZ_EAST_ENABLE_PIN 10

// Motor parameters
#define STEPS_PER_REV 200        // Standard NEMA 17
#define MICROSTEPS 16            // TMC2208 microstepping setting
#define MAX_SPEED 2000           // Steps per second
#define ACCELERATION 1000        // Steps per second^2
#define MIN_PULSE_WIDTH 2        // Microseconds

// Position tracking
long altPosition = 0;
long azPosition = 0;  // Positive = East, Negative = West

// Speed settings (steps per second)
int altSpeed = 800;
int azSpeed = 800;

// Direction flags
bool altDirection = true;

// Movement state
bool isMoving = false;
unsigned long lastStepTime = 0;
unsigned long stepInterval = 1000; // Microseconds between steps

// Command buffer
String inputString = "";
bool stringComplete = false;

void setup() {
  // Initialize serial communication
  Serial.begin(115200);
  while (!Serial) {
    ; // Wait for serial port to connect
  }
  
  // Configure motor pins
  pinMode(ALT_STEP_PIN, OUTPUT);
  pinMode(ALT_DIR_PIN, OUTPUT);
  pinMode(ALT_ENABLE_PIN, OUTPUT);
  
  pinMode(AZ_WEST_STEP_PIN, OUTPUT);
  pinMode(AZ_WEST_DIR_PIN, OUTPUT);
  pinMode(AZ_WEST_ENABLE_PIN, OUTPUT);
  
  pinMode(AZ_EAST_STEP_PIN, OUTPUT);
  pinMode(AZ_EAST_DIR_PIN, OUTPUT);
  pinMode(AZ_EAST_ENABLE_PIN, OUTPUT);
  
  // Enable motors (LOW = enabled for TMC2208)
  digitalWrite(ALT_ENABLE_PIN, LOW);
  digitalWrite(AZ_WEST_ENABLE_PIN, LOW);
  digitalWrite(AZ_EAST_ENABLE_PIN, LOW);
  
  // Set initial directions
  digitalWrite(ALT_DIR_PIN, HIGH);
  digitalWrite(AZ_WEST_DIR_PIN, HIGH);
  digitalWrite(AZ_EAST_DIR_PIN, HIGH);
  
  // Reserve space for input string
  inputString.reserve(200);
  
  // Send ready message
  Serial.println("READY");
  Serial.println("Star Adventurer GTi Polar Alignment Controller v2.0");
  Serial.println("Differential AZ Control Enabled");
  printHelp();
}

void loop() {
  // Check for serial commands
  if (stringComplete) {
    processCommand(inputString);
    inputString = "";
    stringComplete = false;
  }
  
  // Handle any ongoing movements
  updateMotors();
}

/*
 * Serial event handler - called when data is available
 */
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    
    if (inChar == '\n') {
      stringComplete = true;
    } else {
      inputString += inChar;
    }
  }
}

/*
 * Process incoming commands
 */
void processCommand(String cmd) {
  cmd.trim();
  
  if (cmd.length() == 0) {
    return;
  }
  
  char command = cmd.charAt(0);
  String param = cmd.substring(1);
  
  switch (command) {
    case 'H':
    case 'h':
      printHelp();
      break;
      
    case 'S':  // Stop all motors
    case 's':
      stopMotors();
      Serial.println("OK:STOPPED");
      break;
      
    case 'E':  // Enable motors
    case 'e':
      enableMotors(true);
      Serial.println("OK:ENABLED");
      break;
      
    case 'D':  // Disable motors
    case 'd':
      enableMotors(false);
      Serial.println("OK:DISABLED");
      break;
      
    case 'A':  // Move ALT motor
    case 'a':
      if (param.length() > 0) {
        long steps = param.toInt();
        moveAltitude(steps);
        Serial.print("OK:ALT_MOVE:");
        Serial.println(steps);
      } else {
        Serial.println("ERROR:NO_PARAMETER");
      }
      break;
      
    case 'Z':  // Move AZ motors (differential)
    case 'z':
      if (param.length() > 0) {
        long steps = param.toInt();
        moveAzimuthDifferential(steps);
        Serial.print("OK:AZ_MOVE:");
        Serial.println(steps);
      } else {
        Serial.println("ERROR:NO_PARAMETER");
      }
      break;
      
    case 'P':  // Get position
    case 'p':
      Serial.print("POS:ALT:");
      Serial.print(altPosition);
      Serial.print(":AZ:");
      Serial.println(azPosition);
      break;
      
    case 'R':  // Reset position counters
    case 'r':
      altPosition = 0;
      azPosition = 0;
      Serial.println("OK:RESET");
      break;
      
    case 'V':  // Set speed (velocity)
    case 'v':
      if (param.length() > 0) {
        int speed = param.toInt();
        if (speed > 0 && speed <= MAX_SPEED) {
          altSpeed = speed;
          azSpeed = speed;
          stepInterval = 1000000L / speed;
          Serial.print("OK:SPEED:");
          Serial.println(speed);
        } else {
          Serial.println("ERROR:INVALID_SPEED");
        }
      }
      break;
      
    case 'B':  // Balance AZ screws (find center tension)
    case 'b':
      balanceAzimuth();
      break;
      
    case '?':  // Status query
      printStatus();
      break;
      
    default:
      Serial.print("ERROR:UNKNOWN_COMMAND:");
      Serial.println(command);
      break;
  }
}

/*
 * Move altitude motor by specified steps
 */
void moveAltitude(long steps) {
  if (steps == 0) return;
  
  // Set direction
  digitalWrite(ALT_DIR_PIN, steps > 0 ? HIGH : LOW);
  altDirection = steps > 0;
  
  // Execute steps
  long absSteps = abs(steps);
  for (long i = 0; i < absSteps; i++) {
    digitalWrite(ALT_STEP_PIN, HIGH);
    delayMicroseconds(MIN_PULSE_WIDTH);
    digitalWrite(ALT_STEP_PIN, LOW);
    delayMicroseconds(stepInterval);
    
    // Update position
    altPosition += altDirection ? 1 : -1;
  }
}

/*
 * Move azimuth motors in differential mode
 * 
 * Positive steps = Move EAST (tighten west screw, loosen east screw)
 * Negative steps = Move WEST (loosen west screw, tighten east screw)
 */
void moveAzimuthDifferential(long steps) {
  if (steps == 0) return;
  
  long absSteps = abs(steps);
  
  if (steps > 0) {
    // Move EAST: West screw tightens (forward), East screw loosens (backward)
    digitalWrite(AZ_WEST_DIR_PIN, HIGH);   // Tighten
    digitalWrite(AZ_EAST_DIR_PIN, LOW);    // Loosen
  } else {
    // Move WEST: West screw loosens (backward), East screw tightens (forward)
    digitalWrite(AZ_WEST_DIR_PIN, LOW);    // Loosen
    digitalWrite(AZ_EAST_DIR_PIN, HIGH);   // Tighten
  }
  
  // Execute synchronized steps on both motors
  for (long i = 0; i < absSteps; i++) {
    // Step both motors simultaneously
    digitalWrite(AZ_WEST_STEP_PIN, HIGH);
    digitalWrite(AZ_EAST_STEP_PIN, HIGH);
    delayMicroseconds(MIN_PULSE_WIDTH);
    
    digitalWrite(AZ_WEST_STEP_PIN, LOW);
    digitalWrite(AZ_EAST_STEP_PIN, LOW);
    delayMicroseconds(stepInterval);
    
    // Update position (positive = east, negative = west)
    azPosition += (steps > 0) ? 1 : -1;
  }
}

/*
 * Balance azimuth screws to find neutral center position
 * This helps establish equal tension on both screws
 */
void balanceAzimuth() {
  Serial.println("BALANCE:START");
  Serial.println("BALANCE:This is a manual procedure");
  Serial.println("BALANCE:1. Manually adjust screws to center position");
  Serial.println("BALANCE:2. Use small test moves to verify balance");
  Serial.println("BALANCE:3. Reset position when centered");
  Serial.println("BALANCE:READY");
  
  // User should now manually center the mount and then send 'R' to reset position
}

/*
 * Stop all motor movement
 */
void stopMotors() {
  isMoving = false;
  // Motors will naturally stop when no more step pulses are sent
}

/*
 * Enable or disable motors
 */
void enableMotors(bool enable) {
  // TMC2208: LOW = enabled, HIGH = disabled
  digitalWrite(ALT_ENABLE_PIN, enable ? LOW : HIGH);
  digitalWrite(AZ_WEST_ENABLE_PIN, enable ? LOW : HIGH);
  digitalWrite(AZ_EAST_ENABLE_PIN, enable ? LOW : HIGH);
}

/*
 * Update motor positions (for future non-blocking movement)
 */
void updateMotors() {
  // Placeholder for future acceleration/deceleration implementation
}

/*
 * Print help message
 */
void printHelp() {
  Serial.println("===================================");
  Serial.println("COMMANDS:");
  Serial.println("  H or h          - Show this help");
  Serial.println("  S or s          - Stop all motors");
  Serial.println("  E or e          - Enable motors");
  Serial.println("  D or d          - Disable motors");
  Serial.println("  A<steps>        - Move ALT motor (+/- steps)");
  Serial.println("  Z<steps>        - Move AZ (+ = East, - = West)");
  Serial.println("  P or p          - Get current positions");
  Serial.println("  R or r          - Reset position counters to 0");
  Serial.println("  V<speed>        - Set speed (steps/sec)");
  Serial.println("  B or b          - Balance AZ screws (guide)");
  Serial.println("  ?               - Print status");
  Serial.println("===================================");
  Serial.println("AZIMUTH DIFFERENTIAL CONTROL:");
  Serial.println("  Z100   - Move EAST (west tightens, east loosens)");
  Serial.println("  Z-100  - Move WEST (west loosens, east tightens)");
  Serial.println("===================================");
  Serial.println("EXAMPLES:");
  Serial.println("  A1600          - Move ALT 1600 steps forward");
  Serial.println("  A-800          - Move ALT 800 steps backward");
  Serial.println("  Z200           - Move AZ 200 steps EAST");
  Serial.println("  Z-200          - Move AZ 200 steps WEST");
  Serial.println("  V1000          - Set speed to 1000 steps/sec");
  Serial.println("===================================");
}

/*
 * Print current status
 */
void printStatus() {
  Serial.println("STATUS:");
  Serial.print("  ALT Position: ");
  Serial.println(altPosition);
  Serial.print("  AZ Position: ");
  Serial.print(azPosition);
  Serial.println(" (+ = East, - = West)");
  Serial.print("  Speed: ");
  Serial.print(altSpeed);
  Serial.println(" steps/sec");
  Serial.print("  Microsteps: ");
  Serial.println(MICROSTEPS);
  Serial.print("  Steps/Rev: ");
  Serial.println(STEPS_PER_REV * MICROSTEPS);
  Serial.println("  AZ Mode: DIFFERENTIAL (synchronized opposing screws)");
}

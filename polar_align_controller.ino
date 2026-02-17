/*
 * Star Adventurer GTi - Automated Polar Alignment Controller
 * 
 * Controls two stepper motors for ALT and AZ adjustments
 * Communicates via USB Serial with host computer
 * 
 * Hardware:
 * - Arduino Nano/Uno
 * - 2x TMC2208/TMC2209 stepper drivers
 * - 2x NEMA 17 stepper motors
 * 
 * Protocol:
 * - Commands are single characters followed by optional parameters
 * - Format: <command>[value]\n
 * 
 * Author: Polar Align Automation Project
 * Version: 1.0
 */

// Pin definitions for Motor 1 (ALT - Altitude)
#define ALT_STEP_PIN 2
#define ALT_DIR_PIN 3
#define ALT_ENABLE_PIN 4

// Pin definitions for Motor 2 (AZ - Azimuth)
#define AZ_STEP_PIN 5
#define AZ_DIR_PIN 6
#define AZ_ENABLE_PIN 7

// Motor parameters
#define STEPS_PER_REV 200        // Standard NEMA 17
#define MICROSTEPS 16            // TMC2208 microstepping setting
#define MAX_SPEED 2000           // Steps per second
#define ACCELERATION 1000        // Steps per second^2
#define MIN_PULSE_WIDTH 2        // Microseconds

// Position tracking
long altPosition = 0;
long azPosition = 0;

// Speed settings (steps per second)
int altSpeed = 800;
int azSpeed = 800;

// Direction flags
bool altDirection = true;  // true = CW, false = CCW
bool azDirection = true;

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
  
  pinMode(AZ_STEP_PIN, OUTPUT);
  pinMode(AZ_DIR_PIN, OUTPUT);
  pinMode(AZ_ENABLE_PIN, OUTPUT);
  
  // Enable motors (LOW = enabled for TMC2208)
  digitalWrite(ALT_ENABLE_PIN, LOW);
  digitalWrite(AZ_ENABLE_PIN, LOW);
  
  // Set initial directions
  digitalWrite(ALT_DIR_PIN, HIGH);
  digitalWrite(AZ_DIR_PIN, HIGH);
  
  // Reserve space for input string
  inputString.reserve(200);
  
  // Send ready message
  Serial.println("READY");
  Serial.println("Star Adventurer GTi Polar Alignment Controller v1.0");
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
      
    case 'Z':  // Move AZ motor
    case 'z':
      if (param.length() > 0) {
        long steps = param.toInt();
        moveAzimuth(steps);
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
 * Move azimuth motor by specified steps
 */
void moveAzimuth(long steps) {
  if (steps == 0) return;
  
  // Set direction
  digitalWrite(AZ_DIR_PIN, steps > 0 ? HIGH : LOW);
  azDirection = steps > 0;
  
  // Execute steps
  long absSteps = abs(steps);
  for (long i = 0; i < absSteps; i++) {
    digitalWrite(AZ_STEP_PIN, HIGH);
    delayMicroseconds(MIN_PULSE_WIDTH);
    digitalWrite(AZ_STEP_PIN, LOW);
    delayMicroseconds(stepInterval);
    
    // Update position
    azPosition += azDirection ? 1 : -1;
  }
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
  digitalWrite(AZ_ENABLE_PIN, enable ? LOW : HIGH);
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
  Serial.println("  Z<steps>        - Move AZ motor (+/- steps)");
  Serial.println("  P or p          - Get current positions");
  Serial.println("  R or r          - Reset position counters to 0");
  Serial.println("  V<speed>        - Set speed (steps/sec)");
  Serial.println("  ?               - Print status");
  Serial.println("===================================");
  Serial.println("EXAMPLES:");
  Serial.println("  A1600          - Move ALT 1600 steps forward");
  Serial.println("  A-800          - Move ALT 800 steps backward");
  Serial.println("  Z3200          - Move AZ 3200 steps forward");
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
  Serial.println(azPosition);
  Serial.print("  Speed: ");
  Serial.print(altSpeed);
  Serial.println(" steps/sec");
  Serial.print("  Microsteps: ");
  Serial.println(MICROSTEPS);
  Serial.print("  Steps/Rev: ");
  Serial.println(STEPS_PER_REV * MICROSTEPS);
}

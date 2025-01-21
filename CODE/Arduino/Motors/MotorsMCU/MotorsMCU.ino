// Pin definitions
const int limitSwitchPin = 2;
const int stepPin = 3;
const int dirPin = 4;
const int enPin = 9;
const int enA = 7;
const int in1 = 6;
const int in2 = 5;

// Motor control variables
int speed = 0;
bool motorEnabled = false;
bool checkstop = false;
int stepperDirection = 1;
unsigned long previousMillis = 0;
const long interval = 50;
int timebt = 0;

// Define states for the state machine
enum State {
  IDLE,
  RUN_DC_MOTOR,
  RUN_STEPPER_MOTOR,
};

State currentState = IDLE;
unsigned long previousMillisDCMotor = 0;
unsigned long previousMillisStepperMotor = 0;

// Stepper motor feed rates (delay between steps)
const int stepperDelayHigh = 1000;  // Faster feed rate (smaller delay)
const int stepperDelayLow = 5000;   // Slower feed rate (larger delay)
int currentStepperDelay = stepperDelayLow; // Start with slow feed rate
int currentPosition = 0; // Track current position for feedback

// Setup serial communication
void setup() {
  Serial.begin(9600);      // Serial Monitor on Arduino Mega
  pinMode(enA, OUTPUT);
  pinMode(in1, OUTPUT);
  pinMode(in2, OUTPUT);
  pinMode(stepPin, OUTPUT);
  pinMode(dirPin, OUTPUT);
  pinMode(enPin, OUTPUT);
  digitalWrite(enPin, LOW);
  pinMode(limitSwitchPin, INPUT_PULLUP);
  digitalWrite(in1, LOW);
  digitalWrite(in2, LOW);

  Serial.println("Arduino Ready");
  while (!Serial.available() || Serial.readStringUntil('\n') != "Python Ready") {
    delay(100);
  }
}

void loop() {
  int limitSwitchState = digitalRead(limitSwitchPin);
  
  // Handle emergency stop at the start of each loop
  checkSerialForEmergencyStop();

  // Process serial commands
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    handleCommand(command);
  }

  // State machine logic
  switch (currentState) {
    case IDLE:
      if (motorEnabled) {
        currentState = RUN_DC_MOTOR;
      }
      break;
    case RUN_DC_MOTOR:
      runDCMotor(speed);
      if (!motorEnabled) {
        currentState = IDLE;
      }
      break;
    case RUN_STEPPER_MOTOR:
      runStepperMotor(timebt);
      currentState = IDLE;
      break;
  }

  // Limit switch handling
  if (limitSwitchState == HIGH) {
    handleLimitSwitch();
  }
  
  // Feedback to Python
  Serial.println("CURRENT SPEED:" + String(speed));
  Serial.println("CURRENT POSITION:" + String(currentPosition));
}

void checkSerialForEmergencyStop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    if (command == "stopmachine") {
      emergencyStop();
    }
  }
}

void handleCommand(String command) {
  if (command == "stopmachine") {
    emergencyStop();
    Serial.println("STOPPED");
  } else if (command.startsWith("setSpeed")) {
    int newSpeed = command.substring(8).toInt();
    if (newSpeed >= 0 && newSpeed <= 255) {
      speed = newSpeed;
      motorEnabled = true;
      timebt = 10;
      Serial.println("SPEED SET TO: " + String(speed));
    } else {
      Serial.println("Invalid speed. Please enter a value between 0 and 255.");
    }
  } else if (command == "slowdrill") {
    speed = 100; // Set to a slower speed
    motorEnabled = true;
    timebt = 10;
    runDCMotor(speed);
    Serial.println("Slow drill mode activated");
  } else if (command == "fastdrill") {
    speed = 255; // Set to maximum speed
    motorEnabled = true;
    timebt = 10;
    runDCMotor(speed);
    Serial.println("Fast drill mode activated");
  } else if (command == "highFeedRate") {
    currentStepperDelay = stepperDelayHigh;
    Serial.println("High Feed Rate selected.");
  } else if (command == "slowFeedRate") {
    currentStepperDelay = stepperDelayLow;
    Serial.println("Slow Feed Rate selected.");
  }
}

void emergencyStop() {
  analogWrite(enA, 0);
  digitalWrite(enPin, HIGH);
  timebt = 0;
  speed = 0;
  motorEnabled = false;
  checkstop = true;
}

void runDCMotor(int speed) {
  digitalWrite(in1, LOW);
  digitalWrite(in2, HIGH);
  analogWrite(enA, speed); // Set the speed via PWM
}

void runStepperMotor(int steps) {
  digitalWrite(dirPin, LOW);
  digitalWrite(enPin, LOW);

  for (int i = 0; i < steps; i++) {
    digitalWrite(stepPin, HIGH);
    delayMicroseconds(currentStepperDelay);
    digitalWrite(stepPin, LOW);
    delayMicroseconds(currentStepperDelay);
    currentPosition++; // Increment position counter
  }
}

void handleLimitSwitch() {
  for (int m = 0; m < 5 && !checkstop; m++) {
    for (int i = 0; i < 600 && !checkstop; i++) {
      digitalWrite(dirPin, HIGH);
      digitalWrite(enPin, LOW);
      
      // Step the motor
      digitalWrite(stepPin, HIGH);
      delayMicroseconds(currentStepperDelay);
      digitalWrite(stepPin, LOW);
      delayMicroseconds(currentStepperDelay);
      currentPosition++;
      
      checkSerialForEmergencyStop(); // Check for emergency stop during operation
    }
  }
}
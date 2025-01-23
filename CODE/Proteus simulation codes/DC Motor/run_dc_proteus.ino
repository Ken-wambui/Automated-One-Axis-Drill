const int enA = 10;  // Enable pin connected to L298 module
const int in1Pin = 11;    // Input 1 pin connected to L298 module
const int in2Pin = 12;    // Input 2 pin connected to L298 module

void setup() {
  pinMode(enA, OUTPUT);
  pinMode(in1Pin, OUTPUT);
  pinMode(in2Pin, OUTPUT);

  digitalWrite(in1Pin,LOW);
  digitalWrite(in2Pin,LOW);
}

void loop() {
  // Set the motor direction to forward
  //analogWrite(enA, 0);

    for (int speed = 0; speed <= 255; speed++) {
      analogWrite(enA, speed);
      digitalWrite(in1Pin, HIGH);
       digitalWrite(in2Pin, LOW);
      delay(10);
  }
  
  delay(1000); // Pause for 1 second
}
  // Vary the motor speed using PWM



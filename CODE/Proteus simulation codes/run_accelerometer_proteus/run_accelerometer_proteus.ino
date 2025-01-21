const int potPinx = A0; // Connect the potentiometer to analog pin A0
const int potPiny = A1; // Connect the potentiometer to analog pin A0
const int potPinz = A2; // Connect the potentiometer to analog pin A0
void setup() {
  Serial.begin(9600);
}

void loop() {
  int potValuex = analogRead(potPinx);
  int potValuey = analogRead(potPiny);
  int potValuez = analogRead(potPinz);
  
  float xDisplacement = map(potValuex, 0, 1023, -4, 4);
  float yDisplacement = map(potValuey, 0, 1023, -4, 4);
  float zDisplacement = map(potValuez, 0, 1023, -4, 4);
  Serial.print("Displacement X axis: ");
  Serial.print(xDisplacement);
   Serial.print("Displacement Y axis: ");
  Serial.print(yDisplacement);
   Serial.print("Displacement Z axis : ");
  Serial.println(zDisplacement);
  
  delay(500); // Adjust the delay as per your requirement
}

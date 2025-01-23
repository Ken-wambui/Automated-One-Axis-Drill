#include <Arduino.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 21;
const int LOADCELL_SCK_PIN = 20;
 HX711 scale;

const int buttonpinEND=45;
const int buttonpinSTART=53;
int buttonstateSTART=0;
int buttonstateEND=0;
const int enA = 10;  // Enable pin connected to L298 module
const int in1Pin = 11;    // Input 1 pin connected to L298 module
const int in2Pin = 12; 
int IN1 = 7;
int IN2= 6;
int IN3 = 5;
int IN4 = 4;
int delayTime =50;
int delayTime1= 100;
int delayTime2=200;

const int potXPin = A0; // Potentiometer for X-axis
const int potYPin = A1; // Potentiometer for Y-axis
const int potZPin = A2; // Potentiometer for Z-axis

void setup() {
    pinMode(buttonpinEND, INPUT);
   
    pinMode(enA, OUTPUT);
    pinMode(in1Pin, OUTPUT);
    pinMode(in2Pin, OUTPUT);
    pinMode(IN1, OUTPUT);
    pinMode(IN2, OUTPUT);
    pinMode(IN3, OUTPUT);
    pinMode(IN4, OUTPUT);
    Serial.begin (9600);
    digitalWrite(in1Pin,LOW);
    digitalWrite(in2Pin,LOW);
    Serial.begin(9600);
    setuploadcell();
}

void loop() {
  buttonstateEND=digitalRead(buttonpinEND);
    buttonstateSTART=digitalRead(buttonpinSTART);
    
  if(buttonstateEND==HIGH){
    //digitalWrite(ledpin,HIGH);
      getloadcelldata();
      getdataaccel();
       analogWrite(enA,0);
       digitalWrite(in1Pin, LOW);
       digitalWrite(in2Pin, LOW);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime);
      delay(1000);
      
          digitalWrite(in1Pin, LOW);
          digitalWrite(in2Pin, LOW);
         digitalWrite(IN1, LOW);
          digitalWrite(IN2, LOW);
         digitalWrite(IN3, LOW);
         digitalWrite(IN4,LOW);  
         getloadcelldata();
         getdataaccel();
  }
  else if (buttonstateSTART==HIGH){
    getloadcelldata();
    getdataaccel();
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime1);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime1);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime1);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime1);
      delay(1000);    
      getloadcelldata();
      getdataaccel();
      analogWrite(enA,255);
      digitalWrite(in1Pin, HIGH);
      digitalWrite(in2Pin, LOW);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime2);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime2);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime2);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime2);
   }
   else{
     getloadcelldata();
     getdataaccel();
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4,HIGH);
      delay(delayTime);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, HIGH);
      delay(delayTime);
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime);
      digitalWrite(IN1, LOW);
      digitalWrite(IN2,HIGH);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      delay(delayTime);  
   }
}
   void getloadcelldata() {
  Serial.print("Weight in KG:\t");
  Serial.println(scale.get_units()/1000, 1);
 // delay(500);
}
void setuploadcell()
  {
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
   Serial.println("Preparing and calibrating....");
  scale.read();
  scale.read_average(20);
  scale.get_value(5);
  scale.get_units(5), 1;
  scale.set_scale(36.059);
  scale.tare();
  scale.read();
  scale.get_value(5);
  scale.get_units(5), 1;
   Serial.println("Calibration complete");
  }

void getdataaccel(){
  // Read the potentiometer values
  int potXValue = analogRead(potXPin);
  int potYValue = analogRead(potYPin);
  int potZValue = analogRead(potZPin);

  // Map the potentiometer values to a range of -100 to +100
  float xDisplacement = map(potXValue, 0, 1023, -4, 4);
  float yDisplacement = map(potYValue, 0, 1023, -4, 4);
  float zDisplacement = map(potZValue, 0, 1023, -4, 4);

  // Print the displacements on the serial monitor
  Serial.print("X Displacement: ");
  Serial.print(xDisplacement);
  Serial.print("\tY Displacement: ");
  Serial.print(yDisplacement);
  Serial.print("\tZ Displacement: ");
  Serial.println(zDisplacement);

  delay(500); // Delay for smoother serial monitor output (adjust if needed)
}




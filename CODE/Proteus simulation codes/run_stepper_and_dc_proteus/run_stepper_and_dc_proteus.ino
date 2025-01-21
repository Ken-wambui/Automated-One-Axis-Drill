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
}

void loop() {
  buttonstateEND=digitalRead(buttonpinEND);
    buttonstateSTART=digitalRead(buttonpinSTART);
    
  if(buttonstateEND==HIGH){
    //digitalWrite(ledpin,HIGH);
    
       analogWrite(enA,0);
       digitalWrite(in1Pin, LOW);
       digitalWrite(in2Pin, LOW);
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
      delay(1000);
          digitalWrite(in1Pin, LOW);
          digitalWrite(in2Pin, LOW);
         digitalWrite(IN1, LOW);
          digitalWrite(IN2, LOW);
         digitalWrite(IN3, LOW);
         digitalWrite(IN4,LOW);  
  }
  else if (buttonstateSTART==HIGH){
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

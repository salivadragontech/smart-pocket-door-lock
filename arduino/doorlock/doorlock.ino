#include <SoftwareSerial.h>
#include <Servo.h>

/**********************
 * pin 2: servoB's power interface
 * pin 3: Red LED power
 * pin 4: Green LED power
 * pin 5: Switch A 
 * pin 6: servoA's data interface
 * pin 7: servoA's power interface
 * pin 8: reading digital input for switch
 * pin 9: Switch B
 * pin 10: RX
 * pin 11: Tx
 * pin 12: servoB's data interface
 * pin 13: LED_BUILTIN
***********************/

int servoBnum = 115;
Servo myservoB;  // create servo for arm
Servo myservoA;  // create servo for hand
SoftwareSerial mySerial(10, 11);// RX, TX

boolean CheckSwichType()
{
  return digitalRead(8);
}

void OpenDoor()
{  
  digitalWrite(3, LOW);
  digitalWrite(4, HIGH);

  if(!CheckSwichType())
  {
    digitalWrite(2, HIGH);
    myservoB.write(servoBnum);
    delay(500);
  }

  digitalWrite(7, HIGH);
  myservoA.write(40); 
  delay(1500);
  digitalWrite(7, LOW);
  digitalWrite(2, LOW);
  
}

void CloseDoor()
{
  digitalWrite(4, LOW);
  digitalWrite(3, HIGH);

  if(!CheckSwichType())
  {
    digitalWrite(2, HIGH);  
    myservoB.write(servoBnum);
    delay(500);
  }

  digitalWrite(7, HIGH);
  myservoA.write(180); 
  delay(1500);
  digitalWrite(7, LOW);   
  digitalWrite(2, LOW);
}

void setup() 
{
  myservoB.attach(12);
  myservoA.attach(6);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(2, OUTPUT);
  pinMode(3, OUTPUT);
  pinMode(4, OUTPUT);
  pinMode(5, INPUT);
  pinMode(7, OUTPUT);
  pinMode(8, INPUT);
  pinMode(9, INPUT);
  Serial.println("Start");
}

String readSerialString()
{
  String s = "";
  while(Serial.available())
  {
      char c = (char)Serial.read();
      if(c!='\n'){
          s += c;
      }
      delay(8);
  }
  return s;
}

void loop() {
  if (Serial.available()) {
    String str = readSerialString();
    Serial.println(str);
    if(str == "OpEn"){
      Serial.println("Door Open");
      digitalWrite(LED_BUILTIN, HIGH);   
      OpenDoor();
    }else if(str == "ClOsE"){
      Serial.println("Door Close");
      digitalWrite(LED_BUILTIN, LOW);   
      CloseDoor();
    }
  }

  if(!digitalRead(5)){
    OpenDoor();
    Serial.println("Open");
  } 
  if(!digitalRead(9)){
    CloseDoor();
    Serial.println("Close");
  } 
}

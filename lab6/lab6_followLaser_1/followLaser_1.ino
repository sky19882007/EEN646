#include <Servo.h>                           

#define MIDDLE 160
#define RANGE  50
Servo servoLeft;
Servo servoRight;
int x = 0;

void setup()                                
{
  Serial.begin(9600);
  servoLeft.attach(12);   
  servoRight.attach(11);     
  servoLeft.writeMicroseconds(1510);
  servoRight.writeMicroseconds(1510);
}  

void turnLeft(){
           servoLeft.writeMicroseconds(1460);
           servoRight.writeMicroseconds(1510);
           delay(100);
}
void turnRight(){
           servoLeft.writeMicroseconds(1510);
           servoRight.writeMicroseconds(1560);
           delay(100);
}
void shortForward(){
           servoLeft.writeMicroseconds(1560);
           servoRight.writeMicroseconds(1460); 
           delay(250);
}
void stayput(){
           servoLeft.writeMicroseconds(1510);
           servoRight.writeMicroseconds(1510);
           delay(100);
}
void loop()                                 
{                   
  if ( Serial.available() > 0 ){
       x = Serial.read();
       x = x + 32;
       if (x> ( MIDDLE + RANGE)){
           turnRight();
       }
       else if (x < ( MIDDLE - RANGE )){
           turnLeft();
       }
       else{
           shortForward();
       }       
  }
  else{
       stayput();
  }
}

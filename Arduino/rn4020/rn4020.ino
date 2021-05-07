#include <stdlib.h>


int diode1 = 11;
int diode2 = 10;
int diode3 = 9;
int diode1Value = 0;
int diode2Value = 0;
int diode3Value = 0;
int swWakeUp = 2;
int hwWakeUp = 3;

void setup(){
  
  //---------------------------------------------- Set PWM frequency for D9 & D10 ------------------------------
 
  TCCR1B = TCCR1B & B11111000 | B00000001;    // set timer 1 divisor to     1 for PWM frequency of 31372.55 Hz
  //TCCR1B = TCCR1B & B11111000 | B00000010;    // set timer 1 divisor to     8 for PWM frequency of  3921.16 Hz
  //TCCR1B = TCCR1B & B11111000 | B00000011;    // set timer 1 divisor to    64 for PWM frequency of   490.20 Hz (The DEFAULT)
  //TCCR1B = TCCR1B & B11111000 | B00000100;    // set timer 1 divisor to   256 for PWM frequency of   122.55 Hz
  //TCCR1B = TCCR1B & B11111000 | B00000101;    // set timer 1 divisor to  1024 for PWM frequency of    30.64 Hz
   
  //---------------------------------------------- Set PWM frequency for D3 & D11 ------------------------------
   
  TCCR2B = TCCR2B & B11111000 | B00000001;    // set timer 2 divisor to     1 for PWM frequency of 31372.55 Hz
  //TCCR2B = TCCR2B & B11111000 | B00000010;    // set timer 2 divisor to     8 for PWM frequency of  3921.16 Hz
  //TCCR2B = TCCR2B & B11111000 | B00000011;    // set timer 2 divisor to    32 for PWM frequency of   980.39 Hz
  //TCCR2B = TCCR2B & B11111000 | B00000100;    // set timer 2 divisor to    64 for PWM frequency of   490.20 Hz (The DEFAULT)
  //TCCR2B = TCCR2B & B11111000 | B00000101;    // set timer 2 divisor to   128 for PWM frequency of   245.10 Hz
  //TCCR2B = TCCR2B & B11111000 | B00000110;    // set timer 2 divisor to   256 for PWM frequency of   122.55 Hz
  //TCCR2B = TCCR2B & B11111000 | B00000111;    // set timer 2 divisor to  1024 for PWM frequency of    30.64 Hz
      
    pinMode(diode1,OUTPUT);
    pinMode(diode2,OUTPUT);
    pinMode(diode3,OUTPUT);
    analogWrite(diode1, 255);
    analogWrite(diode2, 255);
    analogWrite(diode3, 255);
    
    // Wake SW
    pinMode(swWakeUp,OUTPUT);
    digitalWrite(swWakeUp,HIGH);
    delay(500);
    
  
    Serial.begin(115200);
    delay(1000);
    
    
    // Reset HW
    pinMode(hwWakeUp,OUTPUT);
    digitalWrite(hwWakeUp, HIGH);
    delay(200);
    digitalWrite(hwWakeUp, LOW);
    delay(200);
    digitalWrite(hwWakeUp, HIGH);
    delay(200);
    digitalWrite(hwWakeUp, LOW);
    delay(200);
    digitalWrite(hwWakeUp, HIGH);
    delay(200);
    digitalWrite(hwWakeUp, LOW);
    delay(200);
    digitalWrite(hwWakeUp, HIGH);
    delay(3000);
    

    // Set Config
    Serial.println("+"); //Set baudrate
    delay(500);
    Serial.println("SB,4"); //Set baudrate
    delay(500);
    Serial.println("R,1"); //Reboot
    delay(2000);
    Serial.println("SN,LEDBOARD"); //Set Device Name
    delay(500);
    Serial.println("SR,20000000"); //Set device in peripheral mode and set turn on auto advertising
    delay(500);
    Serial.println("SS,C0000001"); //Enable private Services
    delay(500);
    Serial.println("PZ"); //Clear current private Services and Characteristics
    delay(500);
    Serial.println("PS,36ae4f48419b421a95a1af80b7f418ec"); //Create private Service
    delay(500);
    Serial.println("PC,36ae4f48419b421a95a1af80b7f418ec,18,20"); //Create private characteristic
    delay(500);
    //Serial.println("CHW,2902,0100"); //Set on notifications
    //delay(500);
    Serial.println("R,1"); //Reboot
    delay(2000);
    Serial.setTimeout(50);
    delay(200);
    
    
    
}


void loop() {
  
  if (Serial.available() > 0) {
      String message = Serial.readString(); //read the incoming data as string

      if(message.startsWith("WV,001C,")){
        
        char onOffVal[7];
        char messVal1[3];
        char messVal2[3];
        char messVal3[3];
        
        message.substring(8).toCharArray(onOffVal, 7); //cut off the part with the values
        message.substring(14,16).toCharArray(messVal1, 3);
        message.substring(16,18).toCharArray(messVal2, 3);
        message.substring(18,20).toCharArray(messVal3, 3);
        
        
        if(onOffVal[1] == '1'){ //get state of Diode1
          diode1Value = (int)(strtol(messVal1, NULL, 16)); // get value of Diode1
          analogWrite(diode1, 255 - diode1Value);
        } else {
          analogWrite(diode1, 255); 
        }
        
        if(onOffVal[3] == '1'){ //get state of Diode2
          diode2Value = (int)(strtol(messVal2, NULL, 16)); // get value of Diode2
          analogWrite(diode2, 255 - diode2Value);
        } else {
          analogWrite(diode2, 255); 
        }
        
        if(onOffVal[5] == '1'){ //get state of Diode3
          diode3Value = (int)(strtol(messVal3, NULL, 16)); // get value of Diode3
          analogWrite(diode3, 255 - diode3Value);
        } else {
          analogWrite(diode3, 255); 
        }
      }
  }
  
}

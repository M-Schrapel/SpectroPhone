

void setup(){
  
    // Wake SW
    pinMode(2,OUTPUT);
    digitalWrite(2,HIGH);
    delay(200);
    
    
    Serial.begin(115200);
    delay(1000);
    Serial.println("+"); //Set baudrate
    delay(500);
    Serial.println("SF,1"); // Factory default config
    delay(500);
    Serial.println("SR,00000000"); // Set as peripheral
    delay(500);
    Serial.println("R,1"); //Reboot
    delay(500);
    Serial.println("A"); //start advertising
    delay(500);
}

void loop(){
  
}

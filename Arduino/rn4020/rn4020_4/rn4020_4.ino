void setup(){

    pinMode(3,OUTPUT);
    //Nach Stromversorgung in den ersten 5 Sekunden 3 mal von High auf Low wechseln. F�hrt zu vollst�ndigem Reset.
    digitalWrite(3, HIGH);
    delay(200);
    digitalWrite(3, LOW);
    delay(200);
    digitalWrite(3, HIGH);
    delay(200);
    digitalWrite(3, LOW);
    delay(200);
    digitalWrite(3, HIGH);
    delay(200);
    digitalWrite(3, LOW);
    delay(200);
    digitalWrite(3, HIGH);
    delay(3000);
}


void loop() {
  
    
}



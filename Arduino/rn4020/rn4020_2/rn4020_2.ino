int Diode1 = 11;
int Diode2 = 10;
int Diode3 = 9;

void setup(){
  
    pinMode(Diode1,OUTPUT);
    pinMode(Diode2,OUTPUT);
    pinMode(Diode3,OUTPUT);
    pinMode(3,OUTPUT);
    
    reset();
    initiali();
}


void loop() {
  
    
}


void reset() {
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

void initiali() {
  
  String notification = "";
  
  Serial.begin(115200);
  delay(800);
  
  Serial.println("SB,0");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  
  Serial.println("R,1");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  delay(2000);
  
  if ( notification.length()>0){
    Serial.begin(2400);
  }else{
    Serial.begin(19200);
  }
  
  Serial.println("V");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  
  Serial.println("SN, LEDBOARD");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
	
  Serial.println("SR,20000000");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();

  Serial.println("SS,C0000001");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();	
   
  Serial.println("PZ"); 
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  
  Serial.println("PS,454d532d536572766963652d424c4531"); 
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  
  Serial.println("PC,454d532d536572766963652d424c4531,18,20"); 
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();

  Serial.println("SB,2");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
  
  Serial.println("R,1");
  delay(200);
  if (Serial.available() > 0) {
    notification = Serial.readStringUntil('\n');
    Serial.print(notification);
  }
  Serial.println();
	
  Serial.begin(19200);
  delay(2000);

}

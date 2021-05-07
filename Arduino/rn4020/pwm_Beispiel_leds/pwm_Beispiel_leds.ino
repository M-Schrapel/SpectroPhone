

int Diode1 = 11;
int Diode2 = 10;
int Diode3 = 9;

void setup()  { 
  analogWrite(Diode1, 255);
  analogWrite(Diode2, 255);
  analogWrite(Diode3, 255);
} 

void loop()  { 
  
  // --------------------------------------------------- Diode 1 ---------------------------------------------------
  // fade in from min to max
  for(int fadeValue = 255 ; fadeValue >= 200; fadeValue -=1) { 
    analogWrite(Diode1, fadeValue);           
    delay(30);                            
  } 
  
  // fade out from max to min
  for(int fadeValue = 200 ; fadeValue <= 255; fadeValue +=1) { 
    analogWrite(Diode1, fadeValue);            
    delay(30);                            
  } 
  
  // --------------------------------------------------- Diode 2 ---------------------------------------------------
  // fade in from min to max
  for(int fadeValue = 255 ; fadeValue >= 200; fadeValue -=1) { 
    analogWrite(Diode2, fadeValue);           
    delay(30);                            
  } 
  
  // fade out from max to min
  for(int fadeValue = 200 ; fadeValue <= 255; fadeValue +=1) { 
    analogWrite(Diode2, fadeValue);            
    delay(30);                            
  } 
  
  // --------------------------------------------------- Diode 3 ---------------------------------------------------
  // fade in from min to max
  for(int fadeValue = 255 ; fadeValue >= 200; fadeValue -=1) { 
    analogWrite(Diode3, fadeValue);           
    delay(30);                            
  } 
  
  // fade out from max to min
  for(int fadeValue = 200 ; fadeValue <= 255; fadeValue +=1) { 
    analogWrite(Diode3, fadeValue);            
    delay(30);                            
  } 
  
  // --------------------------------------------------- All Diodes ---------------------------------------------------
  // fade in from min to max
  for(int fadeValue = 255 ; fadeValue >= 200; fadeValue -=1) { 
    analogWrite(Diode1, fadeValue); 
    analogWrite(Diode2, fadeValue);
    analogWrite(Diode3, fadeValue);
    delay(30);                            
  } 
  
  // fade out from max to min
  for(int fadeValue = 200 ; fadeValue <= 255; fadeValue +=1) { 
    analogWrite(Diode1, fadeValue); 
    analogWrite(Diode2, fadeValue);
    analogWrite(Diode3, fadeValue);            
    delay(30);                            
  } 

}



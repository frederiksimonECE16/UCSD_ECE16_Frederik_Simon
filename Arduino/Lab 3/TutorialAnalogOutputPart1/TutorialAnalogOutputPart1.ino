// setting PWM properties 
const int pwmFrequency = 5000;  // Set the PWM frequency to 5KHz
const int pwmPin = LED_BUILTIN;       // Use the built-in LED pin
const int pwmBitResolution = 8; // Set a PWM resolution of 8 bits

void setup() {
  // configure PWM for the specified pin
  // and attach the PWM channel to the output GPIO to be controlled
  ledcAttach(pwmPin, pwmFrequency, pwmBitResolution);

}

void loop() {
  
  //achieve different brightenss levels by setting different duty cycles
  ledcWrite(pwmPin, 0);
  delay(2000);
  ledcWrite(pwmPin,127);
  delay(2000);
  ledcWrite(pwmPin, 255);
  delay(2000);
  ledcWrite(pwmPin, 90);
  delay(2000);

}

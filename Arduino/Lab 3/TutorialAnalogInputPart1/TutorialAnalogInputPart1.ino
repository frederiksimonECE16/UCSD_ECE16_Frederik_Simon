const int accelX = A2;

void setup() {

  // Begin the Serial communication (you did this in the last lab!)
  Serial.begin(115200);
  // Define the analog pin as input
  pinMode(accelX, INPUT);


}

void loop() {
  // put your main code here, to run repeatedly:
  int accel_val = analogRead(accelX);
  // Print the value (you did this in the last lab too)
  Serial.println(accel_val);
}

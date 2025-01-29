//define global vairiable and initialize the values to 0
int ax = 0;
int ay = 0;
int az = 0;

void setup() {
  
  //begin the serial communication
  Serial.begin(9600);

  //setup the Acceleration sensor by calling the function
  setupAccelSensor();


}

void loop() {
  
  //update ax, ay and az by calling the predifined function
  readAccelSensor();

  //Sens to Serial Plotter 
  Serial.print(ax);
  Serial.print(",");
  Serial.print(ay);
  Serial.print(",");
  Serial.println(az);

}

// define pins for x,y and z acceleration
const int accelX = A2;
const int accelY = A3;
const int accelZ = A4;

void setupAccelSensor(){

  //Assign pins as inpiut pins
  pinMode(accelX, INPUT);
  pinMode(accelY, INPUT);
  pinMode(accelZ, INPUT);
}

void readAccelSensor(){

  //read the pins and store the values
  ax = analogRead(accelX);
  ay = analogRead(accelY);
  az = analogRead(accelZ);

}
// set PWM properties
const int pwmFrequency = 5000;  // set the PWM frequency to 5KHz
const int pwmBitResolution = 8; // set a PWM resolution of 8 bits
const int MOTOR_PIN = 18;       // define GPIO pin 18 as pin for the motor

//setup the Motor 
void setupMotor(){

//configure PWM for motor pin and specify frequency and resolution
ledcAttach(MOTOR_PIN, pwmFrequency, pwmBitResolution);

}

//activate Motor: set duty cycle to motorPower
void activateMotor(int motorPower){

//set duty cycle of motor to input of the function
ledcWrite(MOTOR_PIN, motorPower);

}

//deactivate the motor by setting duty cycle of motor to 0
void deactivateMotor(){

  //set duty cycle of motor to 0
  ledcWrite(MOTOR_PIN, 0);

}


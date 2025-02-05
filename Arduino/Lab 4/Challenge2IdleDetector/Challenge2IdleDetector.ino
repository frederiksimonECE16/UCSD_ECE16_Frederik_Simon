int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

//define pin for Motor, LED and BUTTON
int LED_PIN = 13;
int BUTTON_PIN = 12;
int MOTOR_PIN = 16;

//variable to store the last press for button debouncing and last blink for LED blinking 
unsigned long lastPress = 0;
unsigned long lastBlink = 0; 

//blink LED with 5Hz
const unsigned long blink_Interval = 1/5;

//specify the time where no button push is registered
const unsigned long debounceTime = 500;

int last_button_state = HIGH;
int button_state;
int LED_state = LOW;

 


void setup() {
  
  //set up Accelerometer, Communication and Display
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = true;
  
  pinMode(LED_PIN, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  //receive message 
  String command = receiveMessage();
  //if active is sent display a message
  if(command == "active") {
    sending = true;
    writeDisplay("Stay Active!", 0, true);
  }
  //if person is inactive for 5s display a message and blink LED
  else if(command == "inactive5") {
    sending = true;
    writeDisplay("Get UP!", 0, true);
    //blink LED 
    unsigned long current_time = millis()
    if(current_time - lastBlink >= blink_Interval)
    {
      LED_state != LED_state;
      analogWrite = (LED_PIN, LED_STATE);
    }

  }
  //if person is inactive for 10s and motor has buzzed for a second print a message
  else if(command == "inactive10") {
    sending = true;
    writeDisplay("Get UP!", 0, true);
  
  //if buzz is sent buzz the motor and print a message
  else if(command == "buzz") {
    sending = true;
    writeDisplay("Get UP!", 0, true);
    analogWrite(MOTOR_PIN, HIGH);

  //send data 
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}

void detectButton() {

  unsigned long current_time = millis();

  //get current state of Button
  button_state = digitalRead(BUTTON_PIN);

  //check if last state was high and current state is low tht means button has been pressed
  //prevent button debouncing
  if (button_state == LOW && last_button_state == HIGH && current_time - lastPress >= debounceTime) {
    
    //store time of button press and send "pressed" to the python script indicating the button has been pressed
    lastPress = current_time;
    sendMessage("pressed");

    //reset Display to have no remaining characters left that were not overwritten 
    writeDisplay("",0,true);
  }else{
    //button has not been pressed
    sendMessage("notpressed");
  }

  //store last button state
  last_button_state = button_state;
}
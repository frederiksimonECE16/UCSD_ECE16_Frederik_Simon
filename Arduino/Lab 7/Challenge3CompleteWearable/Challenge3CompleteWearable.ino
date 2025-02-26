/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

//specify pin for button and Buzzer 
const int BUTTON_PIN = 13;
const int SwitchButton = 17;

//store current and last button state of both buttons 
int last_button_state = HIGH;
int button_state;

int last_switch_button_state = HIGH;
int switch_button_state;

//variable to store the last press for button debouncing
unsigned long lastPress = 0;
unsigned long lastSwitchPress;

//specify the time where no button push is registered
const unsigned long debounceTime = 500;


void setup() {

  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;
  writeDisplay("Sleep", 0, true);

  //define pin mode for button
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(SwitchButton, INPUT_PULLUP);
}

void loop() {

  //check if button has been pressed 
  detectButton();
  detectSwitchButton();

  String command = receiveMessage();
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if(command != "")
  {
    if(command[0] == '0'){

      command = command.substring(1);
      writeDisplayCSV(command,3);

    }
    else{
      
      writeDisplay(command.c_str(), 0, true);

    } 
    
    
  
  }

  if(sending && sampleSensors()) {
    String response = String(sampleTime);
    response += "," + String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
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
  }

  //store last button state
  last_button_state = button_state;
}

void detectSwitchButton() {

  unsigned long current_time = millis();

  //get current state of Button
  switch_button_state = digitalRead(SwitchButton);

  //check if last state was high and current state is low tht means button has been pressed
  //prevent button debouncing
  if (switch_button_state == LOW && last_switch_button_state == HIGH && current_time - lastSwitchPress >= debounceTime) {
    
    //store time of button press and send "pressed" to the python script indicating the button has been pressed
    lastSwitchPress = current_time;
    sendMessage("statepressed");

    //reset Display to have no remaining characters left that were not overwritten 
    writeDisplay("",0,true);
  }

  //store last button state
  last_switch_button_state = switch_button_state;
}
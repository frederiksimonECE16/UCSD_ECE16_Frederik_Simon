//specify pin for button
const int BUTTON_PIN = 13;

//store current and last button state
int last_button_state = HIGH;
int button_state;

//variable to store the last press for button debouncing
unsigned long lastPress = 0;

//specify the time where no button push is registered
const unsigned long debounceTime = 500;


void setup() {

  // put your setup code here, to run once:
  setupCommunication();
  setupDisplay();

  //define pin mode for button
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {

  //check if button has been pressed 
  detectButton();

  //receive message and print it out if the string is not empty using the Csv function
  String message = receiveMessage();
  if (message != ""){

     
      //Serial.println(message);
      writeDisplayCSV(message, 4);
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
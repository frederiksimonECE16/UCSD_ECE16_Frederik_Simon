/*
 * Global variables
 */
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending;

int LED_PIN1 = 21;
int LED_PIN2 = 15;
int LED_PIN3  = 32;
int BUTTON_PIN = 13;

int lastOrientation = 0;
int currentOrientation = 0;

bool send_pause = false;
unsigned long last_paused = 0;
unsigned long pause_interval = 1000;

//variable to store the last press for button debouncing
unsigned long lastPress = 0;

//specify the time where no button push is registered
const unsigned long debounceTime = 50;

unsigned long lastSendTime = 0;

//store current and last button state of both buttons 
int last_button_state = HIGH;
int button_state;

bool buttonPressed = false;

String message = "";

/*
 * Initialize the various components of the wearable
 */
void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  setupPhotoSensor();
  sending = false;

  pinMode(LED_PIN1, OUTPUT);
  pinMode(LED_PIN2, OUTPUT);
  pinMode(LED_PIN3, OUTPUT);
  pinMode(BUTTON_PIN, INPUT_PULLUP);

  writeDisplay("Ready...", 1, true);
  writeDisplay("Set...", 2, false);
  writeDisplay("Play!", 3, false);
}

/*
 * The main processing loop
 */
void loop() {
  // Parse command coming from Python (either "stop" or "start")
  String command = receiveMessage();
  if(command == "stop") {
    sending = false;
    writeDisplay("Controller: Off", 0, true);
  }
  else if(command == "start") {
    sending = true;
    writeDisplay("Controller: On", 0, true);
  }
  else if(command == "resume") {
    sending = true;
  }
  else if(command == "3"){
    //three lives remaining, power every LED 
    digitalWrite(LED_PIN3, HIGH);
    digitalWrite(LED_PIN2, HIGH);
    digitalWrite(LED_PIN1, HIGH);
    //write to Display
    writeDisplay("lives: 3", 0, true);

  }else if(command == "2"){
    //two lives remaining, power two LEDs
    digitalWrite(LED_PIN3, LOW);
    digitalWrite(LED_PIN2, HIGH);
    digitalWrite(LED_PIN1, HIGH);
    writeDisplay("lives: 2", 0, true);
  
  }else if(command == "1"){
    //one live remaining, power one LED
    digitalWrite(LED_PIN3, LOW);
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN1, HIGH);
    writeDisplay("lives: 1", 0, true);
  }
  else if(command == "0"){
    //no lives remaining, power no LED 
    digitalWrite(LED_PIN3, LOW);
    digitalWrite(LED_PIN2, LOW);
    digitalWrite(LED_PIN1, LOW);
    writeDisplay("lives: 0", 0, true);
  }
  else if(command.charAt(0) == 'T'){

    writeDisplayCSV(command.c_str(), 3);
  }
  

 

  // Send the orientation of the board
  if(sampleSensors()) {
    if(ppg < 10000 && millis() - last_paused >= pause_interval){
      
      sendMessage("0,5");
      last_paused = millis();
      sending = !sending;
      
    }
    else if(sending){
      message = "";
      buttonPressed = detectButton();
      
      // indicate if Button has been presed
      if(buttonPressed){
       message += "1,";
        
      }else{
        message += "0,";
      }

      currentOrientation = getOrientation();
      message += String(currentOrientation);
      //if there is new orientation sent to MCU
      if(currentOrientation != lastOrientation || buttonPressed){

        sendMessage(String(message));
        //lastOrientaion = currentOrientation;
      }
    }
  }
}


bool detectButton() {

  unsigned long current_time = millis();

  //get current state of Button
  button_state = digitalRead(BUTTON_PIN);

  //check if last state was high and current state is low tht means button has been pressed
  //prevent button debouncing
  if (button_state == LOW && last_button_state == HIGH && current_time - lastPress >= debounceTime) {
    
    //store time of button press and send "pressed" to the python script indicating the button has been pressed
    lastPress = current_time;
    //store last button state
    
    last_button_state = button_state;
    return true;
    
    
  }else{
    
    //store last button state
    last_button_state = button_state;
    return false;
  }

  
}
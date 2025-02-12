int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;
bool reset = false;

//specify pin for button
const int BUTTON_PIN = 13;

//store current and last button state
int last_button_state = HIGH;
int button_state;

//variable to store the last press for button debouncing
unsigned long lastPress = 0;

//specify the time where no button push is registered
const unsigned long debounceTime = 500;

int xArray[512];
int yArray[512];
int zArray[512];

// declare indices for reading and writing
int i= 0;
int readindex = 0;

bool activated = false;



void setup() {
  // put your setup code here, to run once:
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
  
  //define pin mode for button
  pinMode(BUTTON_PIN, INPUT_PULLUP);
}

void loop() {
  
  String command = receiveMessage();
  if(command == "sleep") {
    activated = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    activated = true;
    writeDisplay("Activated", 0, true);
  }
  if(activated){
    
    //detect if button was pressed 
    detectButton();
    if(!sending){
      
      //get accelerometer measurements 
      readAccelSensor();
      //tell the user to start making movements 
      writeDisplay("Collect Data", 0, true);
      
      //if data is available update the array and the index with modulo 512 to get a circular buffer
      if(sampleSensors()) {
        xArray[i] = ax;
        yArray[i] = ay;
        zArray[i] = az;
        i = (i + 1) % 512;
      }
    }else if(sending) 
    {
      //send most recent 
      for(int j = 0; j < 512; j++){
        
        readindex = (i + j) % 512;
        
        String response = String(sampleTime) + ",";
        response += String(xArray[readindex]) + "," + String(yArray[readindex]) + "," + String(zArray[readindex]);
        sendMessage(response);

      }
    }
  
    if(reset){
      i = 0;
      reset = false;
      sending = false;
      for(int i = 0; i < 512; i++) 
      {
        xArray[i] = 0;
        yArray[i] = 0;
        zArray[i] = 0;
      }
      writeDisplay("reset", 0 , true);
    }
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
    if(!sending){
      //if previously data was recorded and button is pressed send data 
      sending = true;
      reset = false;

    }else if(sending)
    {
      reset = true;
      
    }

    //reset Display to have no remaining characters left that were not overwritten 
    writeDisplay("",0,true);
  }

  //store last button state
  last_button_state = button_state;
}
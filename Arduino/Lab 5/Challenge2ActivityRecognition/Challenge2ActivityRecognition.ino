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

int xArray[512] = {0};
int yArray[512] = {0};
int zArray[512] ={0};

// declare indices for reading and writing
int i= 0;
int readindex = 0;

bool activated = false;
int state = 0; // 0 = collecting, 1 = sending, 2 = display, 3 = reset


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
  //string to store last command and to prevent constant updating and flashing of the OLED displayS
  static String last_command("");
  String command = receiveMessage();
  if(command == "sleep") {
    activated = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    activated = true;
    writeDisplay("Activated", 0, true);
  }
  else if(command != "") {
    sending = true;
    if(command != last_command){
    writeDisplay("",0,true);
    writeDisplayCSV(command.c_str(), 1);
    last_command = command;
    }
  }
  if(activated){
    
    detectButton();
    
    if(state == 0){
    
    //detect if button was pressed 
    
      
    //get accelerometer measurements 
    readAccelSensor();
    //tell the user to start making movements 
    writeDisplay("Collect", 0, true);
      
    //if data is available update the array and the index with modulo 512 to get a circular buffer
    if(sampleSensors()) {
      xArray[i] = ax;
      yArray[i] = ay;
      zArray[i] = az;
      i = (i + 1) % 512;
      }
    }
    //send the most recent data to the PC 
    else if(state ==1) 
    {
      //send most recent 
      for(int j = 0; j < 512; j++){
        
        readindex = (i + j) % 512;
        
        String response = String(sampleTime) + ",";
        response += String(xArray[readindex]) + "," + String(yArray[readindex]) + "," + String(zArray[readindex]);
        sendMessage(response);

      }
      state = 2;
    }
  
    // reset the program and loop over arrays to set the entries to 0
    if(state == 3){
      i = 0;
      state = 0;
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
    if(state == 0){
      //if previously data was recorded and button is pressed send data 
      state = 1;

    }else if(state == 2)
    {
      state = 3;
      
    }

    //reset Display to have no remaining characters left that were not overwritten 
    writeDisplay("",0,true);
  }

  //store last button state
  last_button_state = button_state;
}
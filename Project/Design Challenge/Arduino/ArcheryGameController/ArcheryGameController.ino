#include <Wire.h>
// Acceleration values recorded from the readAccelSensor() function
int ax = 0; int ay = 0; int az = 0;
int ppg = 0;        // PPG from readPhotoSensor() (in Photodetector tab)
int sampleTime = 0; // Time of last sample (in Sampling tab)
bool sending = false;

//store current and last button state of both buttons 
int last_button_state = HIGH;
int button_state;

const int BUTTON_PIN = 13;

unsigned long lastPress = 0;
//specify the time where no button push is registered
const unsigned long debounceTime = 500;

// Variables to store sensor data
int16_t accelX, accelY, accelZ;
float anglePitch, angleRoll;

String gameState = "1";

unsigned long sendingInterval = 100;
unsigned long lastSendTime = 0;

void setup() {
  // put your setup code here, to run once:
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  Serial.begin(115200);
  setupMPU6050();
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  
}

void loop() {
  
  detectButton();
  String command = "";
  command += receiveMessage();
  writeDisplay(command.c_str(),0, true);

  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  else if(command != ""){
    
    gameState = command;

  }
  
  unsigned long current_time = millis();

  if(sending && sampleSensors() && current_time - lastSendTime >= sendingInterval ) {
    lastSendTime = current_time;
    
    /*String response = String(sampleTime);
    response += "," + String(ax) + "," + String(ay) + "," + String(az);
    response += "," + String(ppg);
    
    sendMessage(response);
    //Serial.println(angleRoll);*/
    //writeDisplay("sending", 0, true );
    
    if(gameState == "2"){
      String response = "";
      response += String(sampleTime);
      response += "," + String(int(angleRoll));
      sendMessage(response);
      writeDisplay("2", 0, true);
    }
    else if(gameState == "3"){

      String response = "";
      response += String(sampleTime);
      response += "," + String(accelY);
       sendMessage(response);
    }
    
    writeDisplay(String(int(angleRoll)).c_str(),0,true);
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
int sampleTime = 0; // Time of last sample (in Sampling tab)
int ax = 0; int ay = 0; int az = 0; // Acceleration (from readAccelSensor())
bool sending;

void setup() {
  setupAccelSensor();
  setupCommunication();
  setupDisplay();
  sending = false;
  writeDisplay("Sleep", 0, true);
}

void loop() {
  static String last_command("");
  String command = receiveMessage();
  //if "sleep" is sent do not send anymore and if "wearable is send start sending"
  if(command == "sleep") {
    sending = false;
    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    sending = true;
    writeDisplay("Wearable", 0, true);
  }
  //if received message is not empty it is the step counter, update the display only if step counter increments
  else if(command != "") {
    sending = true;
    if(command != last_command){
    writeDisplay(command.c_str(), 0, true);
    last_command = command;
    }
  }
  //send acceleration data to python
  if(sending && sampleSensors()) {
    String response = String(sampleTime) + ",";
    response += String(ax) + "," + String(ay) + "," + String(az);
    sendMessage(response);    
  }
}

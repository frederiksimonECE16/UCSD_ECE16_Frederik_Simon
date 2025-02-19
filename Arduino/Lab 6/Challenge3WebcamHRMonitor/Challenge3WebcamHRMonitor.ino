void setup() {

  setupCommunication();
  setupDisplay();
  writeDisplay("Sleep", 0, true);
}

/*
 * The main processing loop
 */
void loop() {
  String command = receiveMessage();
  if(command == "sleep") {

    writeDisplay("Sleep", 0, true);
  }
  else if(command == "wearable") {
    
    writeDisplay("Wearable", 0, true);
  }
  else if(command != "")
  {
    writeDisplay(command.c_str(), 0, true);
  }
}
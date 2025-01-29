void setup() {
  
  //setup motor by calling predifined function from Motor tb
  setupMotor();

}

void loop() {
  
  //activate motor with different duty cycles and interrupts between them
  deactivateMotor();
     delay(2000);
     activateMotor(127);
     delay(2000);
     activateMotor(255);
     delay(2000);
     activateMotor(90);
     delay(2000);

}

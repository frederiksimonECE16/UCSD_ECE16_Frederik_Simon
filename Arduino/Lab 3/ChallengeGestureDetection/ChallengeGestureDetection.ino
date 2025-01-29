int sampleTime = 0; // Time of last sample (in Sampling tab)

/* states: 0 == Accelerometer startup, 1 == start, 2 = wait for Tab, 3 == Countdown
4== Buzz
*/ 
int stateWatch = 0;

//specify pin for button
const int BUTTON_PIN = 13;

//specify pin for buzz motor
const int MOTOR_PIN = 12;

//define global vairiable and initialize the values to 0
int ax = 0;
int ay = 0;
int az = 0;

//initialize tab counter 
int numTab = 0;

//initialize string to display onto the OLED
String numTabString;

//create varaibles to store the last time the accelorometer was tapped, when the timer last counted down and when the button was last pressed
unsigned long lastTab = 0;
unsigned long lastCountdown = 0;
unsigned long lastPress = 0;

//specify after which time the program should decrement, after which time the countdown should start and for how long the button should be pressed for reset
const unsigned long CountdownInterval = 1000;
const unsigned long noTabTime = 5000;
const unsigned long PressTime = 2000;

//store current and last button state 
int last_button_state = HIGH;
int button_state;

//prevent multiple resets
bool press_reset = false;



void setup() {
  
  //define pin modes for motor and button
  pinMode(BUTTON_PIN, INPUT_PULLUP);
  pinMode(MOTOR_PIN, OUTPUT);
  
  //setup Serial connection, Accelorometer and Display
  setupAccelSensor();
  setupDisplay();
  Serial.begin(115200);
  
}

void loop() {

  detectbutton();
  
  //detect tabs and store them as string 
  numTabString = String(detectTaps(az));
  
  
  if(stateWatch == 3)
  {
    countdown();
  }
  if(stateWatch ==4)
  {
    digitalWrite(MOTOR_PIN, HIGH);
  }else 
  {
    digitalWrite(MOTOR_PIN, LOW);
  }

  Serial.println(stateWatch);
  
  //Display numTab onto the OLED
  writeDisplay(numTabString.c_str(), 2, true);
  
}

int detectTaps(int az){
  
  unsigned long time_now = millis();

 
  //check if new samples have been collected
  if(sampleSensors() && Serial.availableForWrite()) {
    
    if(stateWatch == 2 && time_now - lastTab >= noTabTime)
    {
      Serial.print("set 3");
      stateWatch = 3;

    }

    //check if az broke out of defined corridor and increment numTab
    if( az > 2480|| az < 2320){
      
      //check if az is out of corridor because of startup
      if(stateWatch == 0){

        stateWatch = 1;    
      
      }else{
      
        //increment Counter
        numTab++;
        //set state to wait for Tab
        stateWatch = 2;
      
        //store the time the button has been pressed last
        lastTab = time_now;

      }
    }
  }
  return numTab;
}


void countdown(){
  
  Serial.println("count");
  unsigned long current_time = millis();

 //decrement every second and if numTab is zero set state to 4 
  if(current_time - lastCountdown >= CountdownInterval)
  {
    Serial.println("inloop");
    if(numTab == 0){
      
      stateWatch = 4;

    }else{

    numTab--;
    lastCountdown = current_time;

    }
  }
}

void detectbutton(){

  unsigned long current_time = millis();

  //get current state of Button
  button_state = digitalRead(BUTTON_PIN);

  if(button_state == LOW && last_button_state == HIGH) {     
    //store time of button press
    lastPress = current_time;
  }

  //if button is pushed fown check if sufficient time has gone by to do a reset
  if(button_state == LOW)
  {
    
    if(stateWatch == 2 || stateWatch == 3){
     
      if(millis() - lastPress >= PressTime){
    
        stateWatch = 4;
        numTab = 0;
      }
    }
  }
  last_button_state = button_state;
}
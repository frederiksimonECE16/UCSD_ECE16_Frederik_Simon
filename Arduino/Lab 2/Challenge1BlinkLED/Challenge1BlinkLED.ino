const int LED_pin = 13; //Specify the LED pin 

//different periods for different LEDs in ms
const int period_red_1Hz = 1000; //period of 1s 
const int period_blue_5Hz = 200; //period of 200 ms
const int period_yellow_25Hz = 40; //period of 4s

//create periods for second part of Challenge in ms
int period_red;
int on_period_red = 2000;
int off_period_red = 100;

int period_blue;
int on_period_blue = 200;
int off_period_blue = 500;

int period_yellow;
int on_period_yellow = 20;
int off_period_yellow = 20;


//initialize before time 
unsigned long before_time = 0;

//create a boolean that tracks LED state and start with LED off
bool LED_state = LOW;



void setup() {
  
  //set LED pin to output
  pinMode(LED_pin, OUTPUT);

}

//let Red LED blink at an rate of 1 Hz
void LED_red_1Hz()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_red_1Hz/2){

    //update before time 
    before_time = now_time;

    //Switch LED state
    LED_state = !LED_state;
    digitalWrite(LED_pin, LED_state);
    
  }
}

void LED_blue_5Hz()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_blue_5Hz/2){

    //update before time 
    before_time = now_time;

    //Switch LED state
    LED_state = !LED_state;
    digitalWrite(LED_pin, LED_state);
    
  }
}

void LED_yellow_25Hz()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_yellow_25Hz/2){

    //update before time 
    before_time = now_time;

    //Switch LED state
    LED_state = !LED_state;
    digitalWrite(LED_pin, LED_state);
    
  }
}

//implement functions for specific sequences
void LED_red_sequence()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_red){

    //update before time 
    before_time = now_time;

    if(LED_state == LOW){
      LED_state = HIGH;
      period_red = on_period_red;
    }
    else{
      LED_state = LOW;
      period_red = off_period_red;
    }
    digitalWrite(LED_pin, LED_state);
    
  }
}

void LED_blue_sequence()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_blue){

    //update before time 
    before_time = now_time;

    if(LED_state == LOW){
      LED_state = HIGH;
      period_blue = on_period_blue;
    }
    else{
      LED_state = LOW;
      period_blue = off_period_blue;
    }
    digitalWrite(LED_pin, LED_state);
    
  }
}

void LED_yellow_sequence()
{
  //define now time in each loop
  unsigned long now_time = millis();
  
  //check if half of the period period has elapsed 
  if(now_time - before_time >= period_yellow){

    //update before time 
    before_time = now_time;

    if(LED_state == LOW){
      LED_state = HIGH;
      period_yellow = on_period_yellow;
    }
    else{
      LED_state = LOW;
      period_yellow = off_period_yellow;
    }
    digitalWrite(LED_pin, LED_state);
    
  }
}

void loop() {
 
 //call respective function
 //LED_red_1Hz();
 //LED_blue_5Hz();
 //LED_yellow_25Hz();
 LED_red_sequence();
 //LED_blue_sequence();
 //LED_yellow_sequence();

}

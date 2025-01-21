//Specify button pin
const int BUTTON_pin = 13;

//create the timer varaible which indicates the seconds that will elapse until reaching 0 when the timer is started
int timer = 0;

//Interval in which the counter variable should be printed
const unsigned long print_Interval = 100;
//
const unsigned decrement_Interval = 1000;
//define how long the button should be pressed before the stopwatch resets
const unsigned long reset_period = 3000;
//define after which period the timer should start
const unsigned long timer_start = 3000;


//create boolean that indicates if the stopwatch is activated
bool is_timing = false;

//Current and previous button state
int button_state;
int last_button_state = HIGH;

//create variable to store previous time for printing and counting 
unsigned long counting_time_before;
unsigned long printing_time_before;

//store button press time to detect a long press
unsigned long button_press_time;

//store if the button was pressed to reset the stopwatch
bool press_reset = false;
//boolean to prevent constant printing of the timer value 0
bool reached_zero = false;

//specify time where no button push should be recorded
const unsigned long button_delay = 200;

//track if 0 was printed
bool zero_printed = false;


void setup() {
  //define pin 13 as Input with automatic pullup
  pinMode(BUTTON_pin, INPUT_PULLUP);
  
  //define baud rate
  Serial.begin(9600);
  
  //print setup message
  Serial.println("\n");
  Serial.println("Timer initialized");
}

void loop() {
  
  //check what the state of the input pin is
  button_state = digitalRead(BUTTON_pin);

  unsigned long current_time = millis();

  //catch the push of the button if the last push of the button is sufficiently long ago
  if(button_state == LOW && last_button_state == HIGH && (current_time - button_press_time > button_delay )) {
    
    //stop timing, increment timer and state that zero is not reached
    is_timing = false;
    timer++;
    Serial.println(timer);

    reached_zero = false;
      
  //store time of button press
  button_press_time = current_time;
  
  }

  //if button is pushed fown check if sufficient time has gone by to do a reset
  if(button_state == LOW)
  {
    
    if(!press_reset && millis() - button_press_time >= reset_period){

    //reset counter, stop counting and print a reset message
    timer = 0;
    is_timing = false; 
    Serial.println("Timer reset");
    
    
    //set press_reset to true to prevent multiple reset if the button is pushed longer than 3s
    press_reset = true;
    }
  }else {
    //when button is not pressed set press_reset to false
    press_reset = false;
  }

  //if button is not pushed check if sufficient time has gone by to start counting if yes start timing 
  if(button_state == HIGH )
  {
    unsigned long start_time_now = millis();
    
    if(!is_timing && millis()-button_press_time >= timer_start && !reached_zero)
    {
      is_timing = true;

    }
    
  }

  //if timing is active decrement the timer every second and print every 100ms
  if(is_timing){
    
    unsigned long counting_time_now= millis();

    if(counting_time_now - counting_time_before >= decrement_Interval && timer != 0){

      //decrement time counter and store update time for comparison
      timer--;
      counting_time_before = counting_time_now;
      

    }
    
    unsigned long printing_time_now = millis();

    if(printing_time_now - printing_time_before >= print_Interval && is_timing)
    {
      //print counter every 100ms an store print time for comparison
      Serial.println(timer);
      printing_time_before = printing_time_now;
      if(timer == 0){
        zero_printed = true;
      }
    }
   }
   //prevent the timer costantly printing zero by indicating that the zero has been reached and stop the timing
   if(timer == 0){
    
      if(!zero_printed && is_timing){
      
        Serial.println(timer);
      }
      is_timing = false;
      reached_zero = true;
      zero_printed = false;
      
      }
  //store previous button state for next loop
  last_button_state = button_state;

}

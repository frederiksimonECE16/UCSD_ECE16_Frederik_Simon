//Specify button pin
const int BUTTON_pin = 13;

//create the counter variable which reecords time elapsed in seconds
int counter = 0;

//increment counter every second
const unsigned long increment_Interval = 1000;
//Interval in which the counter variable should be printed
const unsigned long print_Interval = 100;
//define how long the button should be pressed before the stopwatch resets
const unsigned long reset_period = 3000;

//create boolean that indicates if the stopwatch is activated
bool is_counting = false;

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

void setup() {
  //define pin 13 as Input with automatic pullup
  pinMode(BUTTON_pin, INPUT_PULLUP);
  
  //define baud rate
  Serial.begin(9600);
  
  //print setup message
  Serial.println("\n");
  Serial.println("Stopwatch started");
}

void loop() {
  
  //check what the state of the input pin is
  button_state = digitalRead(BUTTON_pin);

  //catch the push of the button
  if(button_state == LOW && last_button_state == HIGH) {
    
    unsigned long current_time = millis();
    
    if(is_counting)
    {    
      is_counting = false;

    }else {
      
      is_counting = true;
    }
  
  //store time of button press
  button_press_time = current_time;
  }

//catch if the button is pressed down long enough to reset 
  if(button_state == LOW)
  {
    
    if(!press_reset && millis() - button_press_time >= reset_period){

    //reset counter, stop counting and print a reset message
    counter = 0;
    is_counting = false; 
    Serial.println("Stopwatch.reset.");
    
    //set press_reset to true to prevent multiple reset if the button is pushed longer than 3s
    press_reset = true;
    }
  }else {
    //when button is not pressed set press_reset to false
    press_reset = false;
  }

  

  //print and increment stopwatch if it is running
  if(is_counting){
    
    unsigned long counting_time_now= millis();

    if(counting_time_now - counting_time_before >= increment_Interval){

      //increment time counter and store update time for comparison
      counter++;
      counting_time_before = counting_time_now;
      

    }
    
    unsigned long printing_time_now = millis();

    if(printing_time_now - printing_time_before >= print_Interval)
    {
      //print counter every 100ms an store print time for comparison
      Serial.println(counter);
      printing_time_before = printing_time_now;
    }
    
   
   }
   
  //store previous button state for next loop
  last_button_state = button_state;

}

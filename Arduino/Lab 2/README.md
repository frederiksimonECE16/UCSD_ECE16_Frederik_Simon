Name: Frederik Simon

PID: 10310072

# Lab 2 completed

## Lab 2 Tutorial 1 completed 

The goal of the __Tutorial 1__ was to setup the ESP32 and to get it working. For me the setup of the ESP32 worked smoothly. I had no problems while installing the Arduino IDE as well as configurating the settings and downloading the USB drivers. I was a bit confused of which port to choose to connect my board in the Arduino IDE but after getting help in the tutorial everything worked.

## Lab 2 Tutorial 2 completed 

The objective of __Tutorial 2__ was to gain familarity with the Arduino IDE and programming in it. Furthermore revistiting basic electronic circuits, learning how the ESP32 interacts with them and how the mechanical buttons work.

At first I struggled a bit with building the simple button circuit shown in the tutorial but after asking for help in the Tutorial and a short time revising the basics i managed to do it. Together with the code provided in the tutorial, i then succesfully build my circuit such that at first the built in LED was lighting up at a push of the button and later a LED from our kit.

To finish the tutorial I implemented and understood what non blocking timing is and that it is vital to be able to do multiple tasks and being able to time them consistently and reliably.


## Lab 2 Tutorial 3 completed

In the __Tutorial 3__ the goal was to gain the first experience in communicating with the MCU through the serial monitor. I tried to print on to the serial monitor which worked well for me. For reading the avialable data and printing it again on the serial monitor was a bit confusing for me because I thought for some reason that also my input would be printed into the serial monitor but when I realized that this is not the case and introduced a new line character after each letter, everything became clear. The endings that you can select in the serial monitor are appended atutomatically after your input. No line ending appends nothing, wheras new line appends a '\n' character to your input. You can also automatically add a carriage return which does nothing noticeble for me, or add both a new line and a carriage return, which then results in a new line for the next input.



## Lab 2 Challenge 1 completed 

To let my LEDS blink at the desired frequency, my sketch on the Arduino checks if half of the period 'T' as elapsed with simply using millis() to track the time now and the time it was before switching the state of the LED. If enough time has gone by it negates the state and switches the LED on or off. The period 'T' is the inverse of the the frequency and therefore is 1s for the red, 200ms for the blue and 40 ms for the yellow LED. I purposely implemented a non blocking timer as I understand this will be the most used generally and in this course.

For blinking a red LED at 1 Hz I copied the circuit of __Lab 2 Tutorial 2__. The voltage drop across a red LED is roughly 2.2V. This leads to a voltage drop accross the resistor of 1.1V. Therefore using a 220Ω resistor leads to a curennt of 5 mA. Together with the sketch the red LED blinks at 1Hz: 

![Red LED blinks at 1Hz](images/c1_part1_a.gif)


The voltage drop accross the blue LED should be bigger than for the red LED. Estimating that it is about 3.0V which leads to a voltage drop over the resistor of about 0.3V and consequently a with a 220Ω resistor to a current of 1.4mA. To make the LED shine a bit brighter I changed the resistance to 100Ω to achive a current of 3mA. 

![Blue LED blinks at 5Hz](images/c1_part1_b.gif)

As an estimate of the voltage drop accross the yellow LED I took 2.4V which together with a 220Ω resistor leads to an current of roughly 4mA. For the gif with the yellow LED you have to select the highest framerate possible to avoid loss of data.

![Yellow LED blinks at 25Hz](images/c1_part1_c.gif)


For the second part of the __Challenge 1__ I simply added a conditional clause to the functions which checks if the LED was on or off previously and adjust the following period accordingly.

Red LED with 2s on and 100 ms off:

![Red LED with 2s on and 100 ms off](images/c1_part2_a.gif)


Blue LED with 200ms and 500 ms off:

![Blue LED with 200ms and 500 ms off](images/c1_part2_b.gif)

Additionally I also used the 100Ω resistor in the circuit powering the yellow LED to let it shine brighter and configured my smartphone camera to 60 fps to make it theoretically possible to capture the blinking of the yellow LED. However the gif converter we should use has a maximum framerate of 33 fps.

Yellow LED with 20ms on and 20ms off:

![Yellow LED with 20ms on and 20ms off](images/c1_part2_c.gif)

## Lab 2 Challenge 2 completed 

The task in __Challenge 2__ was to program and build a simple stopwatch that can be operated by pushing a button that is connected to the ESP32. The stopwatch should increment every second while being able to start, stop and resume counting by a push of the button. If the button is pressed down for 3 seconds the stopwatch should reset to a conter value of 0.

To achieve this I firstly defined the pin 13 of the ESP 32 as an Input with an automatic pullup, so that I can ommit the resistor circuit. After setting up the communication with the serial monitor and defining the baud rate I check if the current voltage that my input pin is seeing is low and my last voltage that it saw is high. This means that the button was pressed down, connecting the input pin to the GND pin. Therefore I negate my boolean 'is_counting' which results in starting, stopping or resuming the stopwatch. Additionally, if the input pin sees a low voltage I check if since the moment where the transition from high to low voltage was catched, three seconds have elapsed. If this is true that means the stopwatch should reset and stop counting. To prevent that the stopwatch resets every loop of the program after the button was pressed for more than three seconds a boolean is tracking if the stopwatch has been already reset in this instance of holding the button.

If the stopwatch is counting the program increments the counter every second and prints the counter every 100ms using a decoupled timing mechanism. I tried to use one timing mechanism for incrementing and printing the counter, the problem for me was that you have to store the last time you print or increment which means you have to have a before_time for printing and incremneting, which then resulted for me in a completly decoupled mechanism that worked best for me. In the last step of the loop I store the current state of the input pin as the last button state for comparison in the next loop.

For the hardware it is the ESP32 on a breadboard, where the input pin is connected to one side of the button and the GND pin is connected to the other side of the button. When the button is pressed it shorts both sides thogether, which results in the input pin connected to the GND pin and seeing a low voltage.

The stopwatch works as desired:

![gif of the stopwatch starting, stopping, resuming and reseting at a push or press of the connected button](images/c2.gif)

## Lab 2 Challenge 3 completed 

In __Challenge 3__ a stopwatch should be programmed with the same physical setup as in Challenge 2. When pushing the button the timer should increment the timer which indicates the seconds that will elapse until the timer reaches zero. After three seconds of not pushing the button the timer should start to count the seconds down until the timer reaches 0. Similarly as in Challenge 2the timer should print its value every 100ms when counting down and should reset after 3s of holding down the button.

Because of the similiarity to Challenge 2 I modified my code to achieve the desired bahaviour in Challenge 3. The program now increments the timer once when the button is presed and stops the timer counting down. Additionally, if the button is not pressed or pushed down it is checked in every loop if since the last push of the button three seconds have elapsed. If so and the timer is not currently 0, the timer starts to count down that means decreasing the timer variable every second by one and printing out the timer every 100ms.

A problem I had was the case that the timer was equal to zero and the last time the button was pressed was more than three seconds ago. Then constantly a 0 was printed in the Serial Monitor. Therefore I introduced a boolean to track if the timer has reached 0 which then prevented the timer to go off. This boolean evaluates to true every time the button is pressed, thus the 0 is now only printed once to the serial monitor. After implementing this the program sometimes did not print the 0 at all because the printing interval did not line up with the decrement interval. That is why I also track if the zero has been printed to the serial monitor and if not print it.

Futhermore I also had a problem with the button bouncing and triggering the increment of the timer multiple times. After asking in the tutorial, the solution we found was simply increasing the time where no additional button push is detected to 200ms and then the timer works as desired:

[Video to demonstrate that timer is working as desired for Challenge 3](https://youtu.be/a_G3ALnlYdE)






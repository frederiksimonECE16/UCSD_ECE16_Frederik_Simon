from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np


if __name__ == "__main__":
  num_samples = 250              # 5 seconds of data @ 50Hz
  refresh_time = 0.1            # update the plot every 0.1s (10 FPS)

  
  previous_active_time = 0
  inactive_threshold = 5
  active_threshold = 1

  buzz_start_time = 0
  buzz_threshold = 1

  #raw data CircularLists
  times = CircularList([], num_samples)
  ax = CircularList([], num_samples)
  ay = CircularList([], num_samples)
  az = CircularList([], num_samples)

  #additional lists
  average_x = CircularList([], num_samples)
  delta_x = CircularList([], num_samples)
  L1 = CircularList([], num_samples)
  L2 = CircularList([], num_samples)
  transformed = CircularList([], num_samples) 
  deltaL2_cl = CircularList([], num_samples) 
  average_L2_5 = CircularList([], num_samples)

  comms = Communication("COM8", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  #comms.send_message("wearable")  # begin sending data


    #plot data to establish good threshold
  def plot_transformations_2():
    # Separate L1, L2, and Transformed into individual plots
        
        plt.subplot(312)
        plt.cla()
        plt.plot(times, average_L2_5, label="delta_L1", color="red")
        plt.legend()

        plt.show(block=False)
        plt.pause(0.001)

  try:
    previous_time = 0
    state = 1 #0 == off, 1 == on, 2 == active, 3 == activate1sec,  4 == inactive5, 5 == buzz, 6 == inactive10
    
    while(True):
        message = comms.receive_message()
        #check if button has pressed if yes toggle the idle detector 
        
        #strip incoming message of newline character
        if(message != None and message.strip() == "pressed"):
         
            if state == 0:
            
                state = 1  
            else:
                state = 0

            print(state)

        #if its not a button press message split the data 
        elif(message != None):
            try:
                (m1, m2, m3, m4) = message.split(',')

            except ValueError:        # if corrupted data, skip the sample
                continue


            # add the new values to the circular lists
            times.add(int(m1))
            ax.add(int(m2))
            ay.add(int(m3))
            az.add(int(m4))

            #compute L2 norm of all 3 axes 
            compute_L2 = np.sqrt(ax[-1]**2+ay[-1]**2+az[-1]**2)
            #add value to L2
            L2.add(compute_L2)
            
            samples_one_sec = 50
            deltaL2 = np.abs(L2[-1]- L2[-3])
            deltaL2_cl.add(deltaL2)
            average_L2 = np.sum(L2[-30:])/5
            average_L2_5.add(average_L2)




        #threshold for difference of L2 terms
        threshold = 30
        

        #detect activity 
        current_time_active = time()
        if(deltaL2_cl[-1]>= threshold and state != 0):
            
            print(f"State: {state}, Current Time: {current_time_active:.2f}s, Previous Active: {previous_active_time:.2f}s, Elapsed: {current_time_active - previous_active_time:.2f}s")    
            #if activity is recorded set state to active 
            if state != 2 and state != 3:  
                state = 2
                previous_active_time = current_time_active  

            
            #if activity is longer than 1 sec go to third state
            if(current_time_active - previous_active_time) >= active_threshold:
               state = 3            
            
        #check for inactivity of 5s and set to inactivity5 or inactivity10 
        elif(current_time_active - previous_active_time >= inactive_threshold):
           
           if state == 1 or state == 2 or state == 3:
              state = 4
           
           elif state == 4:
              state = 5
              buzz_start_time = time()
               

           previous_active_time = current_time_active
        
        elif state not in [0, 3, 4, 5, 6]:
           state= 1

        
        #check wich state is active and send information to the MCU 
        if state == 0:
            comms.send_message("off")
        elif state ==1:
           comms.send_message("on")

        elif state == 2:
           comms.send_message("active")

        elif state == 3:

           comms.send_message("activesec")
           
        
        elif state == 4:
           
           comms.send_message("inactive5")
           
        #if the motor has buzzed for one second jump to next state
        elif state == 5:
            
            if (time() - buzz_start_time >= buzz_threshold):
               state = 6
            else:
               comms.send_message("buzz")

        elif state == 6:
           
           comms.send_message("inactive10")



        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          
          #plot delta L2 and  print the state for debugging
          plot_transformations_2()
          print(state)
          
  
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()
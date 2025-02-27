from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np

class IdleDetector:
    def __init__(self, comms_passed, num_samples=250, refresh_time=0.1):
       
       
        #define the attributes that are passed to the class
        self.comms = comms_passed
        self.num_samples = num_samples
        self.refresh_time = refresh_time

        #define the Circularlists for the idledetector 
        self.times = CircularList([], num_samples)
        self.ax = CircularList([], num_samples)
        self.ay = CircularList([], num_samples)
        self.az = CircularList([], num_samples)
        self.L2 = CircularList([], num_samples)
        self.deltaL2_cl = CircularList([], num_samples)

        #track states and define thresholds as attributes
        self.state = 0  # 0=Off, 1=On, 2=Active, 3=Active1sec, 4=Inactive5, 5=Buzz, 6=Inactive10
        self.previous_active_time = 0
        self.buzz_start_time = 0
        self.inactive_threshold = 5  
        self.active_threshold = 1    
        self.buzz_threshold = 1     

        #clear
        #self.comms.clear()

    def run(self, message):
        #define the main function with a try exept block
    
            previous_time = 0
            
            
            #message = self.comms.receive_message()
            
            #if message is not None call the private process method 
            if message != None:
                self.__process_message(message)

       

    #private method to handle incoming messages
    def __process_message(self, message):
        
        #check if button has been pressed 
        if message.strip() == "pressed":
            if  self.state == 0:
            
                self.state = 1  
            else:
                self.state = 0
            
            return

        try:
            (m1, m2, m3, m4, m5) = message.split(',')
        except ValueError:
            return  # Ignore corrupted messages

        #add values to the circular lists
        self.times.add(int(m1))
        self.ax.add(int(m2))
        self.ay.add(int(m3))
        self.az.add(int(m4))

        self.__detect_motion()

    def __detect_motion(self):
        
        #compute L2 norm and add to the circular List
        compute_L2 = np.sqrt(self.ax[-1]**2 + self.ay[-1]**2 + self.az[-1]**2)
        self.L2.add(compute_L2)
        
        #compute the difference over 3 samples of the L2 norm
        deltaL2 = abs(self.L2[-1] - self.L2[-3])  
        self.deltaL2_cl.add(deltaL2)      

        #define threshhold
        threshold = 30
        
        current_time_active = time()

        #detect activity
        if deltaL2 >= threshold and self.state != 0:
            if self.state != 2:
                self.state = 2
                self.previous_active_time = current_time_active
                
           #if activity is longer than 1 sec go to third state
            elif self.state == 2 and (current_time_active - self.previous_active_time) >= self.active_threshold:
                self.state = 3
                
         #check for inactivity of 5s and set to inactivity5 or inactivity10 
        elif current_time_active - self.previous_active_time >= self.inactive_threshold:
            
            if self.state in [1, 2, 3]:
                self.state = 4
                
            elif self.state == 4:
                self.state = 5
                self.buzz_start_time = time()
                
            self.previous_active_time = current_time_active

        elif self.state not in [0, 3, 4, 5, 6]:
            self.state = 1

        self.__send_message()
    
    #encapsulated method to send the state indication to the MCU 
    def __send_message(self):
        
        if self.state == 0:
            
            self.comms.send_message("off")
        
        elif self.state ==1:
           
           self.comms.send_message("on")

        elif self.state == 2:
           
           self.comms.send_message("active")

        elif self.state == 3:

           self.comms.send_message("activesec")
           
        
        elif self.state == 4:
           
           self.comms.send_message("inactive5")
           
        #if the motor has buzzed for one second jump to next state
        elif self.state == 5:
            
            if (time() - self.buzz_start_time >= self.buzz_threshold):
               self.state = 6
            else:
               self.comms.send_message("buzz")

        elif self.state == 6:
           
           self.comms.send_message("inactive10")
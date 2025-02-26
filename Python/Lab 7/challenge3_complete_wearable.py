from ECE16Lib.WeatherWatch import WeatherWatch
from ECE16Lib.Communication import Communication
from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Pedometer import Pedometer
from ECE16Lib.IdleDetector import IdleDetector
import matplotlib.pyplot as plt
from time import time



if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 1                # plot every second

  wear_state = 0 #0 == Weatherwatch , 1 == HeartRate, 2 == Pedometer, 3 == Idle detector,
    
  #instantiate HR object and Pedometer object
  hr_monitor = HRMonitor(num_samples, fs)
  ped = Pedometer(num_samples, fs,[])

  #train model on all data in the data folder 
  gmm = hr_monitor.train(fs)

  
  #setup comminucation
  comms = Communication("COM8", 115200)
  comms.clear()                    # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  #instantiate WeatherWarch
  watch = WeatherWatch(comms)

  #instantiate Idle detector 
  detector = IdleDetector(comms)

  try:
    previous_time = time()
    while True:
        
        #check if state button has been pressed 
        message = comms.receive_message()
        print(wear_state, message)
        
        if message != None:
            if message.strip() == "statepressed":
                
                #increment state if it is 3 go back to 0
                wear_state = (wear_state + 1) % 4
            
            elif message.strip() == "pressed":
                message = message.strip()
        
            else:
                try:
                    (m1, m2, m3, m4, m5) = message.split(',')
                except ValueError:        # if corrupted data, skip the sample
                    continue
        
        
        if(wear_state == 0):
            print(message)
            watch.main(message) 
            
        elif(wear_state == 1):

            try:       
                #convert time into seconds and time and ppg into integer   
                t = int(m1)/1e3
                ppg = int(m5)
                hr_monitor.add(t,ppg)
            except:
                continue

            # if enough time has elapsed, clear the axes, and plot the 4 plots
            current_time = time()
            if (current_time - previous_time > refresh_time):
                    previous_time = current_time

            #print("loop")
            #process data 
            #hr, peaks, filtered = hr_monitor.process()
            #print(hr)

            hr_est, filtered  = hr_monitor.predict(gmm, fs)
                
            #only display the heart rate if the ppg is over 25000 a value that in most cases is exceeded when a finger 
            #is placed on the ppg sensor to prevent the normalized noise to be displayed
                
            #only display the heart rate if the ppg is over 25000 a value that in most cases is exceeded when a finger 
            #is placed on the ppg sensor to prevent the normalized noise to be displayed
            if ppg > 25000:
                hr_str = f"HR: --"
            else:
                hr_str = f"HR: {round(hr_est, 2)}"
                
            #print heart rate into console and send it to MCU
            print(hr_str)
            comms.send_message(hr_str)

            plt.cla()
            plt.plot(filtered)
            plt.show(block=False)
            plt.pause(0.001)

        elif(wear_state == 2):
            
            try:
                # Collect data in the pedometer
                ped.add(int(m2),int(m3),int(m4))
            except:
                continue

            # if enough time has elapsed, process the data and plot it
            current_time = time()
            if (current_time - previous_time > refresh_time):
                previous_time = current_time

          
                #process data by calling the method of the pedometer class
                steps, peaks, filtered = ped.process()
                
                #create a step string to make it easier to display

                #send the step counter to the MCU as a string 
                comms.send_message(str(steps))

                print("Step count: {:d}".format(steps))
        
                #plot data 
                plt.cla()
                plt.plot(filtered, label= 'Filtered Signal')
                plt.title("Step Count: %d" % steps)
                plt.show(block=False)
                plt.pause(0.001)

        elif(wear_state == 3):

            detector.run()
                

  finally:
    comms.close()
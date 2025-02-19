from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Communication import Communication
import matplotlib.pyplot as plt
import numpy as np
import cv2
import time 
#from time import time



if __name__ == "__main__":
  fs = 20                         # sampling rate
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 1                # plot every second
    
  #capture video
  cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
  
  #instantiate HR object 
  hr_monitor = HRMonitor(num_samples, fs)

  #setup comminucation
  comms = Communication("COM8", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = time.time()
    while(True):
        
        #read video 
        _, frame = cap.read()

        #get red channel brightness value 
        new_sample = frame.mean(axis=0).mean(axis=0)
        new_sample = new_sample[2] # replace the ? with index of the RED channel 
                             # which is 2 because OpenCV stores in the BGR format

        #get current time in nanoseconds
        current_time = time.time_ns()/1e9

        t = int(current_time)
        ppg = new_sample
        hr_monitor.add(t,ppg)

        # if enough time has elapsed, clear the axes, and plot the 4 plots
        current_time = time.time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          print("loop")
          hr, peaks, filtered, ppg_raw = hr_monitor.process()
          #print(hr)
          
          hr_str = f"HR: {round(hr, 2)}"
          print(hr_str)
          comms.send_message(hr_str)

          plt.cla()
          plt.plot(filtered)
          #plt.plot(ppg_raw)
          plt.show(block=False)
          plt.pause(0.001)



  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()

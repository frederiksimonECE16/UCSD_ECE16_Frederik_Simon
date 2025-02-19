from ECE16Lib.HRMonitor import HRMonitor
from ECE16Lib.Communication import Communication
import numpy as np
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from time import time



if __name__ == "__main__":
  fs = 50                         # sampling rate
  num_samples = 250               # 5 seconds of data @ 50Hz
  refresh_time = 1                # plot every second
    
  #instantiate HR object 
  hr_monitor = HRMonitor(num_samples, fs)

  #setup comminucation
  comms = Communication("COM8", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  try:
    previous_time = time()
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2) = message.split(',')
        except ValueError:        # if corrupted data, skip the sample
          continue

        t = int(m1)/1e3
        ppg = int(m2)
        hr_monitor.add(t,ppg)

        # if enough time has elapsed, clear the axes, and plot the 4 plots
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time

          print("loop")
          hr, peaks, filtered = hr_monitor.process()
          #print(hr)
          hr_str = f"HR: {round(hr, 2)}"
          print(hr_str)
          comms.send_message(hr_str)

          plt.cla()
          plt.plot(filtered)
          plt.show(block=False)
          plt.pause(0.001)



  except(Exception, KeyboardInterrupt) as e:
    print(e) # exiting the program due to exception
  finally:
    print("Closing connection.")
    comms.send_message("sleep")  # stop sending data
    comms.close()

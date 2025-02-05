from ECE16Lib.Communication import Communication
from ECE16Lib.CircularList import CircularList
from matplotlib import pyplot as plt
from time import time
import numpy as np


if __name__ == "__main__":
  num_samples = 250              # 5 seconds of data @ 50Hz
  refresh_time = 0.1            # update the plot every 0.1s (10 FPS)

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


  comms = Communication("COM8", 115200)
  comms.clear()                   # just in case any junk is in the pipes
  comms.send_message("wearable")  # begin sending data

  def plot_rawdata():
    # Plot raw acceleration data
       

        plt.subplot(311)
        plt.cla()
        plt.plot(times, ax, label="ax", color="red")
        plt.legend()

        plt.subplot(312)
        plt.cla()
        plt.plot(times, ay, label="ay", color="green")
        plt.legend()

        plt.subplot(313)
        plt.cla()
        plt.plot(times, az, label="az", color="blue")
        plt.legend()

        plt.show(block=False)
        plt.pause(0.001)


  def plot_transformations_1():
        # Plot transformations
        
        plt.subplot(311)
        plt.cla()
        plt.plot(times, average_x, label="Average_x", color="purple")
        plt.legend()

        plt.subplot(312)
        plt.cla()
        plt.plot(times, delta_x, label="Delta X", color="orange")
        plt.legend()

        plt.show(block=False)
        plt.pause(0.001)

  def plot_transformations_2():
    # Separate L1, L2, and Transformed into individual plots
        plt.subplot(311)
        plt.cla()
        plt.plot(times, L1, label="L1-Norm", color="blue")
        plt.legend()

        plt.subplot(312)
        plt.cla()
        plt.plot(times, L2, label="L2-Norm", color="red")
        plt.legend()

        plt.subplot(313)
        plt.cla()
        plt.plot(times, transformed, label="Transformed Data", color="black")
        plt.legend()

        plt.show(block=False)
        plt.pause(0.001)

  try:
    previous_time = 0
    while(True):
      message = comms.receive_message()
      if(message != None):
        try:
          (m1, m2, m3, m4) = message.split(',')

        except ValueError:        # if corrupted data, skip the sample
          continue


        # add the new values to the circular lists
        times.add(int(m1))
        ax.add(int(m2))
        ay.add(int(m3))
        az.add(int(m4))

        #average over N seconds @ 50Hz
        N = 5
        num_average_samples = N*50
        
        #compute average of last N seconds
        last_average_x = np.mean(ax[-num_average_samples:])
        #add it to average_x
        average_x.add(last_average_x)

        #compare current value of x accleration to the most recent value
        delta_x.add((ax[-1]-ax[-2]))

        #compute L2 norm of all 3 axes 
        compute_L2 = np.sqrt(ax[-1]**2+ay[-1]**2+az[-1]**2)
        #add value to L2
        L2.add(compute_L2)

        #compute L1 norm 
        compute_L1 = np.abs(ax[-1]) + np.abs(ay[-1]) + np.abs(az[-1])
        #add value to L1
        L1.add(compute_L1)

        #additional Transformation: magnitude normalized acceleration
        #devide each component by computed L2 Norm which leads to a sense of the properties of the motions
        
        #prevent dividing by zero
        if  compute_L2 != 0:
            
            MN_x = ax[-1] / compute_L2
            MN_y = ay[-1] / compute_L2
            MN_z = az[-1]/  compute_L2
            
            # Sum of normalized components
            transformed_value = MN_x + MN_y + MN_z 
        else:
             # If no movement, set to zero
            transformed_value = 0 
        #add to circular list
        transformed.add(transformed_value)  

        # if enough time has elapsed, clear the axis, and plot az
        current_time = time()
        if (current_time - previous_time > refresh_time):
          previous_time = current_time
          
          #plot_rawdata()
          #plot_transformations_1()
          plot_transformations_2()
          
  
  except(Exception, KeyboardInterrupt) as e:
    print(e)                     # Exiting the program due to exception
  finally:
    comms.send_message("sleep")  # stop sending data
    comms.close()


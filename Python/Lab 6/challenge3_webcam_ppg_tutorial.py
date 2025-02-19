import cv2
import numpy as np
import matplotlib.pyplot as plt
import time

#create empty lists 
ppg = []
timestamps = [] 

#set stylo for the plots 
plt.style.use('seaborn-v0_8-whitegrid')

#cap = cv2.VideoCapture(0) # choose your appropriate camera!
cap = cv2.VideoCapture(0,cv2.CAP_DSHOW) #==> use this instead if you’re on Windows!
#print(plt.style.available)
cap.set(cv2.CAP_PROP_FPS, 60)

while(True):
  _, frame = cap.read()
  
  new_sample = frame.mean(axis=0).mean(axis=0)
  new_sample = new_sample[2] # replace the ? with index of the RED channel 
                             # which is 2 because OpenCv stores in the BGR format
  
  #get current time in nonoseconds
  current_time = time.time_ns()/1e9

  #append samples
  ppg.append(new_sample) # append new_sample to ppg
  timestamps.append(current_time)

  cv2.imshow('Input', frame)
  c = cv2.waitKey(1)
  if c == 27:
    break

p = ppg[10:] # remove the first few points because of auto-exposure
t = np.array(timestamps[10:]) # so we can easily subtract the first time

dt = np.mean(np.diff(t))
fs = 1/dt
print(fs) 

fig = plt.figure()
ax = plt.axes()
x = np.linspace(0, 1, len(p))
p = ppg[10:]

t = t - t[0]
ax.set_xlabel("time(s)")
ax.set_ylabel("Red Channel Value")

ax.plot(t, p)
plt.show()


cap.release()
cv2.destroyAllWindows()
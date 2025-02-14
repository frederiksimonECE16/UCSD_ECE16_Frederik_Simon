Name: Frederik Alexander Simon

PID: 10310072


# Lab 6 

## Lab 6 Tutorial 1

In this tutorial I learned:

* how Photoplethymography (PPG) detects volumetric blood changes by shining light of a particular spectrum into a volume and measuring the properties of the reflected light 
* an overview how we would built our own Photodetector by taking a light source, a light sensor that converts received light at a specific wavelength into a small current and a amplification circuit to produce an adewuate signal for our ADC 
* how to connect the MAX30101 sensor
* test the board with example sketches provided by the library

__Questions:__

* I can connect both the OLED display and the photodetector to the same pins of my board because they use I2C connection wich always sends the individual address of the device and the clock data and therefore each device is distinguishable
* the while(1) statement prevents further execution of the code because the code gets stuck in the while loop only a restart of the microcontroller helps to get out
* to use only the RED and IR LED set the ledMode to 2, to set the sampling rate to 200 just change the integer sampleRate to 200
* to adjust the ADC range modify the corresponding integer and to set the LED brightness to 25mA set the ledBrightness to half its digital value and therefore 127 
* the units of pulse width are micro seconds and if you increase the pulsewidth you also increase the duty cycle and therefore also the intensity
* You would need 14 bits for an ADC range of 16384
* The peak wavelengths are roughly Red: 660nm, Infrared: 880 nm, Green 530nm


Furthermore I did:

* creating a photodetector tab for easy reusable code 
* testing the code over Serial plotter and with python 
* testing the code over bluetooth and serial connection

## Lab 6 Tutorial 2 

In this tutorial I learned: 

#### how we filter ppg data:

* first the signal is detrended using our DSP module
* then moving average is applied 
* take a small window not to flatten the peaks
* implement a gradient of the signal to emphasize the large peaks 
* Normalize our data by making the minimum value of our data vector a 0 and the highest signal a 1 
* define a new function in our DSP module for normalizing the data
* detect peaks by setiing the threshhold at 0.6
* computing the heart rate by taking the mean off the time differences between the peaks and dividing 60 by it to get bpm
* I recorded 13 detected peaks and a estimated heart rate of 74.37 bpm

#### Creating and testing own HRMonitor class:

* copy code in the library folder and reinstall library 
* load data and instantiate object
* call process method and plot data 

### Lab 6 Tutorial 3:

* Recorded 5 samples of 1 min heart rate data
* tried to have a consistent hand placement
* good data with distuingishable peaks 
* data with elevated heartrate 
* correct naming of the file
* used left index finger because left hand is nearest to heart 






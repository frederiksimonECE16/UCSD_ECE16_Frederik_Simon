import serial  # the PySerial library
import time
from pyowm import OWM
from datetime import datetime, timedelta
import ECE16Lib.Communication

"""
Class for the Weather watch 
"""
class WeatherWatch:
   
    def __init__(self, comms_passed):

        self.last_updated = 0  #define a time when the OLED has been last updated
        self.refresh_time = 1   #specify refresh time in seconds
        self.comms = comms_passed
        self.cityState = 0#define a city State 0 == San Diego, 1 == Munich, 2 == Tokyo
    
    def get_Data(self):
    

        owm = OWM('c50e737ce6d4bfb007d7cca6cd4cf38e').weather_manager()

        #collect weather data for San Diego, Munich and Tokyo
        weather_SD = owm.weather_at_place('San Diego,CA,US').weather
        weather_MUC = owm.weather_at_place('Munich,DE').weather
        weather_TKY = owm.weather_at_place('Tokyo, JP').weather

        # dictionary for all kinds of temperatures in celsius
        temp_dict_celsius_SD = weather_SD.temperature('celsius')
        temp_dict_celsius_MUC = weather_MUC.temperature('celsius')
        temp_dict_celsius_TKY = weather_TKY.temperature('celsius')

        #take the weather status and format it as string
        status_SD = str(weather_SD.detailed_status)
        status_MUC = str(weather_MUC.detailed_status)
        status_TKY = str(weather_TKY.detailed_status)

        #take current temperature out of the dictionary 
        temperature_SD = str(temp_dict_celsius_SD['temp'])
        temperature_MUC = str(temp_dict_celsius_MUC['temp'])
        temperature_TKY = str(temp_dict_celsius_TKY['temp'])

        return status_SD, status_MUC, status_TKY, temperature_SD, temperature_MUC, temperature_TKY

    # Format date and time 
    def format_time(self,time):
        
        formatted_date = time.strftime("%Y-%m-%d")
        formatted_time = time.strftime("%H:%M:%S")

        formated_date_time = "Date: " + formatted_date + "," + "Time: " + formatted_time

        return formated_date_time

    #dependent on the state print the String of the respective location
    def printString(self, cityState, string_SD, string_MUC, string_TKY):
        #print(cityState)
        if self.cityState == 0:
            self.comms.send_message(string_SD)
        elif self.cityState == 1:
            self.comms.send_message(string_MUC)
        elif self.cityState == 2:
            self.comms.send_message(string_TKY)

    #main function to run the code
    def main(self, message):
        
        status_SD, status_MUC, status_TKY, temperature_SD, temperature_MUC, temperature_TKY = self.get_Data()
        
        
            
        #time now for OLED updates 
        time_now = int(time.time())

        #collect time data
        #get UTC time
        utc_now = datetime.utcnow()

        #time differences to UTC time
        san_diego_time_difference = timedelta(hours=-8)  
        munich_time_difference = timedelta(hours=1)     
        tokyo_time_difference = timedelta(hours=9)

        #add the time deltas to UTC to get the correct time 
        san_diego_time = utc_now + san_diego_time_difference
        munich_time = utc_now + munich_time_difference
        tokyo_time = utc_now + tokyo_time_difference

        #define the output string  in CSV format to be displayed by the function in the Arduino IDE 
        string_MUC = "0Munich," + self.format_time(munich_time)+ "," + "Temp: " + temperature_MUC + " C" #+ status_MUC 
        string_SD = "0San Diego," + self.format_time(san_diego_time)+ "," +"Temp: " + temperature_SD + " C" #+ status_SD  
        string_TKY = "0Tokyo," + self.format_time(tokyo_time)+ "," +"Temp: " + temperature_TKY + " C" #+status_TKY   

        #print(string_SD)

        #receive the message and if it is something meaningful strip it of its new line characters
        #message = self.comms.receive_message()
        if message != None:
            message = message.strip() 
        
        #print(message)
        #message = "pressed"
        print(message)
        #check if the button has been pressed update the state and the OLED displayy
        if message == "pressed":
        
            if self.cityState == 2:
                self.cityState = 0
                self.printString(self.cityState, string_SD, string_MUC, string_TKY)
                

            else:
                self.cityState += 1
                self.printString(self.cityState, string_SD, string_MUC, string_TKY)
                
        #update the screen every second
        if time_now - self.last_updated >= self.refresh_time:
            self.last_updated = time_now
            self.printString(self.cityState, string_SD, string_MUC, string_TKY)


    


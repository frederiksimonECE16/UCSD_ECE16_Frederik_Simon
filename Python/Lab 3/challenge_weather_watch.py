import serial  # the PySerial library
import time
from pyowm import OWM
from datetime import datetime, timedelta

#define a time when the OLED has been last updated
last_updated = 0

#specify refresh time in seconds
refresh_time = 1

#setup connection
def setup(serial_name, baud_rate):
   ser = serial.Serial(serial_name, baudrate=baud_rate)
   time.sleep(.1)
   ser.flushInput()
   ser.flushOutput()
   #send_message(ser,"test")
   time.sleep(.1)
   return ser

#close connection
def close(ser):
   ser.close()


def send_message(ser, message):
   if(message[-1] != '\n'):
       message = message + '\n'
   ser.write(message.encode('utf-8'))

"""
Receive a message from Serial and limit it to num_bytes (default of 50)
"""
def receive_message(ser, num_bytes=50):
    if(ser.in_waiting > 0):
        return ser.readline(num_bytes).decode('utf-8')
    else:
        return None


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

# Format date and time 
def format_time(time):
    
    formatted_date = time.strftime("%Y-%m-%d")
    formatted_time = time.strftime("%H:%M:%S")

    formated_date_time = "Date: " + formatted_date + "," + "Time: " + formatted_time

    return formated_date_time



#dependent on the state print the String of the respective location
def printString(ser, cityState, string_SD, string_MUC, string_TKY):
    print(cityState)
    if cityState == 0:
        send_message(ser, string_SD)
    elif cityState == 1:
        send_message(ser, string_MUC)
    elif cityState == 2:
        send_message(ser, string_TKY)

#main function to run the code
def main():
    
    #establish connection
    ser = setup("COM8", 115200)
    time.sleep(1)
    ser.flushInput()
    ser.flushOutput()
    last_updated = 0
    #define a city State 0 == San Diego, 1 == Munich, 2 == Tokyo
    cityState = 0
    try:
        while True:
            

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
            string_MUC = "Munich," + format_time(munich_time)+ "," + "Temp: " + temperature_MUC + " C," + status_MUC 
            string_SD = "San Diego," + format_time(san_diego_time)+ "," +"Temp: " + temperature_SD + " C," + status_SD  
            string_TKY = "Tokyo," + format_time(tokyo_time)+ "," +"Temp: " + temperature_TKY + " C," + status_TKY   

            #receive the message and if it is something meaningful strip it of its new line characters
            message = receive_message(ser)
            if message != None:
                message = message.strip() 
            
            #print(message)
            #message = "pressed"
            
            #check if the button has been pressed update the state and the OLED displayy
            if message == "pressed":
            
                if cityState == 2:
                    cityState = 0
                    printString(ser, cityState, string_SD, string_MUC, string_TKY)
                    

                else:
                    cityState += 1
                    printString(ser, cityState, string_SD, string_MUC, string_TKY)
                    
            #update the screen every second
            if time_now - last_updated >= refresh_time:
                last_updated = time_now
                printString(ser, cityState, string_SD, string_MUC, string_TKY)

    #after while loop is exited close serial connection
    finally:
        close(ser)

"""
Main entrypoint for the application
"""
if __name__== "__main__":
   main()
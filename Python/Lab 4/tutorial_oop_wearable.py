from ECE16Lib.Communication import Communication
import time

#establish connection
if __name__ == "__main__":
  comms = Communication("COM8", 115200)
  print(comms)

def main():
    
    #initialize counting variable
    x= 0
    
    #loop for 30 times
    for i in range(30):
        
        
        comms.clear()
        
        #increment and format as a string 
        x += 1 
        message = str(x) + " seconds"
        
        #send, wait and then receive message
        comms.send_message(message)
        time.sleep(1)
        message_received = ""
        message_received = comms.receive_message()
        
        #print only if the string is not empty 
        if message_received != "":
           
           print(message_received)



if __name__ == "__main__":

  try:
    #call main function
    main()
    print("Normal program execution finished")
  except KeyboardInterrupt:
    print("User stopped the program with CTRL+C input")
  finally:
    # Clean up code should go here (e.g., closing comms)
    comms.close()
    print("Cleaning up and exiting the program")
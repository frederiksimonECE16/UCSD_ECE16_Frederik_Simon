"""
@author: Ramsin Khoshabeh
"""

from ECE16Lib.Communication import Communication
from time import sleep
import socket, pygame
from time import time 

# Setup the Socket connection to the Space Invaders game
host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.connect((host, port))
mySocket.setblocking(False)

class PygameController:
  comms = None

  def __init__(self, serial_name, baud_rate):
    self.comms = Communication(serial_name, baud_rate)
    self.send_interval = 0.01
    self.time_last_sent = 0
    self.lives = 0
    self.top_scores = self.load_scores() #load the top scores 


  #try to load the txt file to get the top scores 
  def load_scores(self):
    
    try:
      with open("top_scores.txt", "r") as file:
        
        #convert the different lines of the file into integers 
        scores = [int(line.strip()) for line in file.readlines()]
        
        #sort the scores reversely and take only the top 3
      return sorted(scores, reverse=True)[:3]  
    
    except FileNotFoundError:
      #if the file is not found return 0 as top scores 
      return [0, 0, 0]

  def save_scores(self):
    
    #write the topscores into the txt file 
    with open("top_scores.txt", "w") as file:
      for score in self.top_scores:
        file.write(f"{score}\n")

  def update_scores(self, new_score):
    
    #if a new top score is achieved append it to the array
    self.top_scores.append(new_score)
    
    #sort and only keep top scores 
    self.top_scores = sorted(self.top_scores, reverse=True)[:3]  
    
    #write the scores to the file 
    self.save_scores()
    self.send_scores()
  

  def send_scores(self):
    #send a csv fromatted string to MCU 
     
    top_scores_str = ""

    for top_score in self.top_scores:
      top_scores_str +=  "," + str(top_score) 
    
    top_scores_str = "Top Scores: " +  top_scores_str

    print(top_scores_str)
    self.comms.send_message(top_scores_str)



  def run(self):
    # 1. make sure data sending is stopped by ending streaming
    self.comms.send_message("stop")
    self.comms.clear()

    # 2. start streaming orientation data
    input("Ready to start? Hit enter to begin.\n")
    self.comms.send_message("start")

    # 3. Forever collect orientation and send to PyGame until user exits
    print("Use <CTRL+C> to exit the program.\n")
    while True:
      
      response = None
      try:
        response, _ = mySocket.recvfrom(1024) # receive 1024 bytes
        response = response.decode('utf-8')
        
        #if response != None:
        #  print(response)
        #  print(type(response))
        
        #try: 
        #  response = int(response)
        #  print("Received:", response)
        #except ValueError:
        #  response = None
        
        print(response)
        
        if response != None: #response != self.lives:
          
          if response[0] == "!":
            
            #signal to MCU that the game is over
            #self.comms.send_message("Game Over")
            
            self.update_scores(int(response[1:]))

            print("game over received")
          else:
            #print("message sent")
            self.lives = response
            self.comms.send_message(str(response))
      
        #print(response)
        #print(type(response))

      except BlockingIOError:
        pass  # No data received



      message = self.comms.receive_message()
      if(message != None):
        command = ""
        message = message.strip()
        message_list = message.split(",")
        #print("message:", message)
        # if message == 0:
        #   command = "FLAT"
        # if message == 1:
        #   command = "UP"
         
        #indicate if the fire command was sent 
        if message_list[0] == "1":
          command += "FIRE,"
        else:
          command += "NF,"
        
        if message_list[1] == "3":
          command += "LEFT"
        elif message_list[1] == "4":
          command += "RIGHT"
        elif message_list[1] == "5":
          command += "PAUSE"

        time_now = time()

        
          


        if time_now - self.time_last_sent >= self.send_interval:
          if command is not None:
            mySocket.send(command.encode("UTF-8"))

          self.time_last_sent = time_now 


if __name__== "__main__":
  serial_name = "COM8"
  baud_rate = 115200
  controller = PygameController(serial_name, baud_rate)

  try:
    controller.run()
  except(Exception, KeyboardInterrupt) as e:
    print(e)
  finally:
    print("Exiting the program.")
    controller.comms.send_message("stop")
    controller.comms.close()
    mySocket.send("QUIT,R".encode("UTF-8"))
    mySocket.close()

  input("[Press ENTER to finish.]")

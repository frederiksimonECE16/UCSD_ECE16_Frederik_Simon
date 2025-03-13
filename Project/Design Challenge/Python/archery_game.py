import pygame
import math
import os
from ECE16Lib.Communication import Communication
import time 
from ECE16Lib.CircularList import CircularList
import numpy as np
import ECE16Lib.DSP as filt
import matplotlib.pyplot as plt


# Initialize Pygame
pygame.init()

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
IMAGE_PATH = BASE_PATH + '/images/'


#gravity constant for a window width of 800 equivalent to 50 m archery setup --> 800/50 = 16
g = 9.81*16 #pixe/s^2

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREY = (128, 128, 128)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Archery Game")
clock = pygame.time.Clock()

#load background image
background = pygame.image.load(os.path.join(IMAGE_PATH, 'background.png')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))  

# Load Archer Image
archer_img = pygame.image.load(os.path.join(IMAGE_PATH, 'archer.png')).convert_alpha()
archer_img = pygame.transform.scale(archer_img, (100, 100))

# Load Arrow image
arrow_img = pygame.image.load(os.path.join(IMAGE_PATH, 'arrow.png')).convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (30, 30))

# Archer Class
class Archer:
    def __init__(self, x, y, data =[]):
        self.x = x
        self.y = y
        self.angle = 0  # Initial angle looking straight
        self.power = 10  # Arrow speed
        
        self.fs = 50
        self.num_samples = 50
        self.time = CircularList(data, self.num_samples)
        self.accel = CircularList(data, self.num_samples)
        self.filtered = CircularList([], self.num_samples)
        self.__new_samples = 0
        #self.velocity_y = 0
        #self.distance_y = 0

        self.power_state = 0

    def add(self, t, x):
        if isinstance(t, np.ndarray):
            t = t.tolist()
        if isinstance(x, np.ndarray):
            x = x.tolist()


        if isinstance(x, int) or isinstance(x, np.float64):
            self.__new_samples += 1
        else:
            self.__new_samples += len(x)

        self.time.add(t)
        self.accel.add(x)

    def process(self):
        # Grab only the new samples into a NumPy array
        x = np.array(self.accel[ -self.__new_samples: ])
        #t = np.array(self.time[ -self.__new_samples: ])
        if len(x) < 2:
            return 0, [], []
        """
        b, a= filt.create_filter(3, 1, "lowpass",self.fs)
        x_filtered = filt.filter(b, a, x)
       
        # Compute time differences (dt)
        dt = np.diff(t)  # Time intervals
        if len(dt) == 0:
            return 0, [], []

        # First integration: Get velocity (trapz rule)
        v = np.cumsum(x_filtered[:-1] * dt)  # Approximate velocity

        v = filt.detrend(v)        

        # Second integration: Get displacement
        displacement = np.cumsum(v[:len(dt[:-1])] * dt[:-1])  
        # Approximate position

        # Update total traveled distance
        self.distance_y += displacement[-1] if len(displacement) > 0 else 0
            
        print("Approxiamated distance:", self.distance_y)

        """
        # Filter the signal 
        x = filt.detrend(x, 25)
        x = filt.moving_average(x, 5)
        x = filt.gradient(x)
        #x = filt.normalize(x)

        # Store the filtered data
        self.filtered.add(x.tolist())
        
        if max(x) >= 2000:

            self.power_state = 3

        elif max(x) >= 1000:

            self.power_state = 2

        elif max(x) >= 500:

            self.power_state = 1

        else:

            self.power_state = 0

        print(self.power_state)
        return 
    
    def reset(self):
        
        self.time.clear()
        self.accel.clear()
        self.filtered.clear()

        
    #display Archer
    def draw(self, screen):
    
        #rotate the image of the Archer according to the angle input 
        rotated_archer = pygame.transform.rotate(archer_img, self.angle)
        rect = rotated_archer.get_rect(center=(self.x, self.y))
        screen.blit(rotated_archer, rect.topleft)

    def aim(self, direction):
        #increase or decrease the angle of the Archer keep in the range of [-90, 90]
        if direction == "left" and self.angle >= -90 and self.angle < 90:
            self.angle += 2  # Decrease angle
            print(self.angle)
        elif direction == "right"  and self.angle > -90 and self.angle <= 90:
            self.angle -= 2  # Increase angle

# Target Class
class Target:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, screen):
        colors = [WHITE, BLACK, BLUE, RED, YELLOW]
        for i, color in enumerate(colors):
            pygame.draw.circle(screen, color, (self.x, self.y), self.radius - i * 15)

# Arrow Class
class Arrow:
    def __init__(self, x, y, angle, speed):
        self.x = x
        self.y = y
        
        #convert to angle to radians
        self.angle = math.radians(angle)
        self.speed = speed
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.active = True
        
        #store last update time 
        self.last_updated = pygame.time.get_ticks()
        
        self.dt = 0

        self.moving = True

    def move(self):
        
        current_time = pygame.time.get_ticks()
        self.dt = (current_time - self.last_updated)/1000
        
        #update last updated
        self.last_updated = current_time 

        if self.moving:
            #update x
            self.x += self.vx*self.dt

            #update y with euler numerical integration
            self.vy += g*self.dt
            self.y += self.vy*self.dt

            self.angle = math.atan2(self.vy,self.vx)

        # Out of bounds
        if self.x > WIDTH or self.y > HEIGHT:  
            self.active = False

        if self.x >= target.x and self.x <= target.x + target.radius and self.y >= target.y - target.radius and self.y <= target.y+ target.radius:
            
            #set x position manually 
            #self.x = target.x
            
            #print("stop")
            self.moving = False

        

    def draw(self, screen):
        
        rotated_arrow =  pygame.transform.rotate(arrow_img, -math.degrees(self.angle))
        rect = rotated_arrow.get_rect(center=(self.x, self.y))
        screen.blit(rotated_arrow, rect.topleft)



# Game Setup
archer = Archer(70, HEIGHT //2+120)
target = Target(WIDTH - 150, HEIGHT // 2+70, 75)
arrows = []


 
#setup comminucation
comms = Communication("COM8", 115200)
comms.clear()                    # just in case any junk is in the pipes
comms.send_message("wearable")  # begin sending data

m1 = 0 
m2 = 0


class ArcheryGame:
    def __init__(self):
        self.m1 = 0
        self.m2 = 0
        
        #Game state: 1 = Static game, 2 = Set Angle, 3 = Set Force
        self.game_state = 1
    
    def receive_data(self):

        
        #check if state button has been pressed 
        message = comms.receive_message()
        
        if message != None:
            
            #print(message)
            if message.strip() == "pressed":
                
                if(self.game_state == 3):

                    if archer.power_state == 0:

                        archer.power = 100

                    elif archer.power_state == 1:
                    
                        archer.power = 300

                    elif archer.power_state == 2:

                        archer.power = 400

                    elif archer.power_state == 3:

                        archer.power = 600
                        print("full_power")
                    
                    arrows.append(Arrow(archer.x + 50, archer.y - 20, -archer.angle, archer.power))
                    archer.reset()
                    archer.power_state = 0
                    
                
                
                self.game_state = (self.game_state % 3) +1
                
                comms.send_message(str(self.game_state))
                print("sent", self.game_state)
                return False
                
        
            else:
                try:
                    (m1, m2) = message.split(',')
                    m1 = int(m1)
                    m2 = int(m2)
                    self.m2 = m2
                    self.m1 = m1

                    if self.game_state == 3:
                        archer.time.add(m1/1000)
                        archer.accel.add(m2)
                    return True
                except ValueError:       
                    return False 
    
    def run(self):
        try:
            # Game Loop
            running = True
            while running:
                
                screen.blit(background, (0,0))

                if self.receive_data():

                    if self.game_state == 2:

                        archer.angle = self.m2
                    
                    elif self.game_state == 3:
                        archer.process()

                        #plt.cla()
                        #plt.plot(archer.filtered)
                        #plt.show(block=False)
                        #plt.pause(0.001)
                        
                #print(self.game_state

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                # Handle input
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    archer.aim("left")
                if keys[pygame.K_RIGHT]:
                    archer.aim("right")
                if keys[pygame.K_SPACE]:  # Shoot an arrow
                    #print(archer.angle)
                    arrows.append(Arrow(archer.x + 50, archer.y - 20, -archer.angle, archer.power))

                # Draw objects
                archer.draw(screen)
                target.draw(screen)
                
                # Move and draw arrows
                for arrow in arrows[:]:
                    arrow.move()
                    if not arrow.active:
                        arrows.remove(arrow)
                    arrow.draw(screen)

                

                pygame.display.flip()
                clock.tick(FPS)

            pygame.quit()

        finally:
            comms.send_message("sleep")
            comms.close()


if __name__ == '__main__':
    game = ArcheryGame()
    game.run()
    
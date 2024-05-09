from libdw import pyrebase
from time import sleep
import RPi.GPIO as GPIO
import pygame, sys

#--------------------- Setup motion sensor pins --------------------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(29, GPIO.IN)  #Read outpout from front motion sensor
GPIO.setup(37, GPIO.IN)  #Read output from rear motion sensor

GPIO.setup(11, GPIO.OUT)  #Front 1st LED

GPIO.setup(31, GPIO.OUT)  #Rear 1st LED


#------------------- Setup Database Variables -----------------------------#

dburl = "https://dti-prototype-2023-default-rtdb.asia-southeast1.firebasedatabase.app/"
email = "group7@test.com"
password = "group7" 
apikey = "AIzaSyC7XYj-HQkuS6jMRGuoQjG6givCY53xUes"
authdomain = dburl.replace("https://","")


config = {
    "apiKey": apikey, 
    "authDomain": authdomain,
    "databaseURL": dburl,
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password(email, password)
db = firebase.database()
user = auth.refresh(user['refreshToken'])

# ------------------------ Setup Image Database ------------------------------
class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.is_animating = False
        self.sprites.append(pygame.image.load('ver2-0.png'))
        self.sprites.append(pygame.image.load('ver2-1.png'))
        self.sprites.append(pygame.image.load('ver2-2.png'))
        self.sprites.append(pygame.image.load('ver2-3.png'))
        self.sprites.append(pygame.image.load('ver2-4.png'))
        self.sprites.append(pygame.image.load('ver2-5.png'))
        self.sprites.append(pygame.image.load('ver2-6.png'))
        self.sprites.append(pygame.image.load('ver2-7.png'))
        self.sprites.append(pygame.image.load('ver2-8.png'))
        self.sprites.append(pygame.image.load('ver2-9.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 1
            sleep(0.05) #speed of gif

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
            
        self.image = self.sprites[self.current_sprite]

#----------------------- Game Setup -----------------------------#

# General Game Setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen (width,height)
screen = pygame.display.set_mode((1000,600))
pygame.display.set_caption("Sprite Animation")

#Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(10,10)
moving_sprites.add(player)

#-------------------- Main (Update Database) -----------------------------#


"""
# Upload data function
print("Now we upload a key-value pair")
value = input("Enter a value: ")
db.child(key).set(value, user['idToken'])
print("please go to the firebase console and have a look") 

sleep(2)
"""
running = True
current_time = 0
time_marker = 0
time_interval = 1000

GPIO.output(11,1)
GPIO.output(31,1)

while running: 
    
    time_start = pygame.time.get_ticks()
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            
            print("Ending firebase (upload) script and clearing the LEDs")
            db.child("Front").set(False, user['idToken'])
            db.child("Rear").set(False, user['idToken'])
            GPIO.output(11,0)
            GPIO.output(31,0)

            running = False   
            pygame.quit()
            sys.exit()
            
    
    
    if current_time - time_marker > time_interval:
        print("-------------------------------Start------------------------")
        front = GPIO.input(29)  # READ front sensor and assign to "front" 
        rear = GPIO.input(37)  # READ rear sensor and assign to "rear"

        print("Front:" , front)
        print("Rear:" , rear)

        if front==0:  #When output from FRONT motion sensor is LOW/ start state (movement not detected)

            # Upload "Front" to database as "False"
            db.child("Front").set(False, user['idToken'])

            # 1st FRONT wisp ON
            GPIO.output(11, 1)
            print("Front ON")

            # PLAY gif ***********
            player.is_animating = True
            time_interval = 1000

        else:  #When output from front motion sensor is HIGH (movement detected)
            
            # Upload movement to database as "True"
            db.child("Front").set(True, user['idToken'])

            # 1st FRONT wisp OFF
            GPIO.output(11, 0)
            print("Front OFF")

            # STOP gif ***********
            player.is_animating = False
            player.current_sprite = 0
            time_interval = 5000
                    
        if rear==0:  #When output from REAR motion sensor is LOW/ start state
                
            # Upload "Rear" to database as "False"
            db.child("Rear").set(False, user['idToken'])

            # 1st REAR wisp ON
            GPIO.output(31, 1)
            print("Rear ON")

        else:  #When output from REAR motion sensor is HIGH
                
            # Upload "Rear" to database as "True"
            db.child("Rear").set(True, user['idToken'])

            # 1st REAR wisp OFF
            GPIO.output(31, 0)
            print("Rear OFF")
            
        time_marker = pygame.time.get_ticks()
        print("Time marker: " , time_marker)
        print("------------------------End----------------------------")
    
    
    current_time = pygame.time.get_ticks()
    print("Current time: ", current_time)
    

    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    moving_sprites.update()
    
    time_end = pygame.time.get_ticks()
    time_test = time_end - time_start
    print("Time test: " , time_test)
    
    pygame.display.flip()
    clock.tick(60)
    
    

from libdw import pyrebase
from time import sleep
import RPi.GPIO as GPIO
import pygame, sys

#--------------------- Setup motion sensor pins --------------------------#
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(13, GPIO.OUT)  #Front 2nd LED
GPIO.setup(15, GPIO.OUT)  #Front 3rd LED
GPIO.setup(16, GPIO.OUT)  #Front 4th LED

GPIO.setup(32, GPIO.OUT)  #Rear 2nd LED
GPIO.setup(33, GPIO.OUT)  #Rear 3rd LED
GPIO.setup(36, GPIO.OUT)  #Rear 4th LED


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
        self.sprites.append(pygame.image.load('blank.png'))
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

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 1

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
# Download data function
print("Now that there is data in the database, we can download the data")
node = db.child(key).get(user['idToken']) 
print("key   :", node.key())
print("value :", node.val())

sleep(2)
"""
running = True
current_time = 0
time_marker = 0
time_interval = 1000

while True:
    
    time_start = pygame.time.get_ticks() # Time test START

    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            print("Ending firebase (download) script and clearing the LEDs")
            GPIO.output(13,0)
            GPIO.output(15,0)
            GPIO.output(16,0)
            GPIO.output(32,0)
            GPIO.output(33,0)
            GPIO.output(36,0)                
            
            running = False
            pygame.quit()
            sys.exit()

    if current_time - time_marker > time_interval: # *******MOST IMPORTANT PART OF CODE**********
        
        print("-------------------------------Start Download------------------------")    
        front = db.child("Front").get(user['idToken']) # Retrieve "Front" from database
        rear = db.child("Rear").get(user['idToken']) # Retrieve "Rear" from database
        
        print("Front:" , front)
        print("Rear:" , rear)

        if front.val() == False: # When front motion is LOW

            # OFF FRONT wisp sequence
            GPIO.output(13,0)
            GPIO.output(15,0)
            GPIO.output(16,0)
            print("Front LEDs OFF")

            # STOP gif
            player.is_animating = False # stops animation
            player.current_sprite = 0 # sets frame to blank frame
            time_interval = 1000 # Downloads data every __sec
        
        else:

            # ON FRONT wisp sequence
            GPIO.output(13,1)
            sleep(0.5)
            GPIO.output(15,1)
            sleep(0.5)
            GPIO.output(16,1)
            print("Front LEDs ON")

            # PLAY gif ********
            player.is_animating = True # plays animation
            time_interval = 5000 # Downloads data again after __sec; allows gif to PLAY during this time


        if rear.val() == False:

            # OFF REAR wisp sequence
            GPIO.output(32,0)
            GPIO.output(33,0)
            GPIO.output(36,0)
            print("Rear LEDs OFF")
        
        else:

            # ON REAR wisp sequence
            GPIO.output(32,1)
            sleep(0.5)
            GPIO.output(33,1)
            sleep(0.5)
            GPIO.output(36,1)
            print("Rear LEDs ON")
        
        time_marker = pygame.time.get_ticks() # time_interval between update cycles is calculated from the end of every update cycle
        print("Time marker: ", time_marker)
        print("------------------------End Download----------------------------")
    
    
    current_time = pygame.time.get_ticks() # monitors time of every while loop iteration
    print("Current time: ", current_time)    
    

    screen.fill((0,0,0))
    moving_sprites.draw(screen)
    moving_sprites.update()
    pygame.display.flip()
    clock.tick(60)

    time_end = pygame.time.get_ticks() # Time test END
    time_test = time_end - time_start
    print("Time test: " , time_test) 

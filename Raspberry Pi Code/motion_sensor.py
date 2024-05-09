import RPi.GPIO as GPIO
from time import sleep

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup()
GPIO.setup(7, GPIO.IN)  #Read outpout from front motion sensor
GPIO.setup(37, GPIO.IN)  #Read output from rear motion sensor
GPIO.setup(11, GPIO.OUT)  #Front 1st LED
GPIO.setup(13, GPIO.OUT)  #Front 2nd LED
GPIO.setup(15, GPIO.OUT)  #Front 3rd LED
GPIO.setup(16, GPIO.OUT)  #Front 4th LED
GPIO.setup(31, GPIO.OUT)  #Rear 1st LED
GPIO.setup(32, GPIO.OUT)  #Rear 2nd LED
GPIO.setup(33, GPIO.OUT)  #Rear 3rd LED
GPIO.setup(36, GPIO.OUT)  #Rear 4th LED

while True:
    front = GPIO.input(7)  #declare front sensor as front
    rear = GPIO.input(37)  #declare rear sensor as "rear"
    if front==0:  #When output from front motion sensor is LOW/ start state
        GPIO.output(11, 1)  
        GPIO.output(13,0)
        GPIO.output(15,0)
        GPIO.output(16,0)
        time.sleep(10)
    else:  #When output from front motion sensor is HIGH
        GPIO.output(11,0)
        sleep(2000)
        GPIO.output(13,1)
        sleep(500)
        GPIO.output(15,1)
        sleep(500)
        GPIO.output(16,1)
        sleep(5000)       
    if rear==0:  #When output from rear motion sensor is LOW/ start state
        GPIO.output(31, 1)  
        GPIO.output(32,0)
        GPIO.output(33,0)
        GPIO.output(36,0)
        time.sleep(10)
    else:  #When output from rear motion sensor is HIGH
        GPIO.output(31, 0)
        sleep(2000)
        GPIO.output(32,1)
        sleep(500)
        GPIO.output(33,1)
        sleep(500)
        GPIO.output(36,1)
        sleep(5000)
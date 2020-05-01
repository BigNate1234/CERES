####################################
#         Analog Read Code         #
#         by Simon Monk            #
#         modified by Don Wilcher  #
#         Jan 1/31/15              #
####################################

# Source: https://www.allaboutcircuits.com/projects/building-raspberry-pi-controllers-part-5-reading-analog-data-with-an-rpi/

# include RPi libraries in to Python code
import RPi.GPIO as GPIO
import time

# instantiate GPIO as an object
GPIO.setmode(GPIO.BCM)

# define GPIO pins with variables a_pin and b_pin
a_pin = 18
b_pin = 23

# create discharge function for reading capacitor data
def discharge():
    GPIO.setup(a_pin, GPIO.IN)
    GPIO.setup(b_pin, GPIO.OUT)
    GPIO.output(b_pin, False)
    time.sleep(0.005)

# create time function for capturing analog count value
def charge_time():
    GPIO.setup(b_pin, GPIO.IN)
    GPIO.setup(a_pin, GPIO.OUT)
    count = 0
    GPIO.output(a_pin, True)
    while not GPIO.input(b_pin):
        count = count +1
    return count

# create analog read function for reading charging and discharging data
def analog_read():
    discharge()
    return charge_time()

t = 2
# provide a loop to display analog data count value on the screen
while t >= 0:
    print(analog_read())
    print('t=',t)
    time.sleep(.05)
    t = t-.5

GPIO.cleanup()

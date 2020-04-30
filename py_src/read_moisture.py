import RPi.GPIO as GPIO
import time
import argparse

parser = argparse.ArgumentParser(description='Select box num.')
parser.add_argument('box', metavar='box',
                    help='The box to be measured.')
args = parser.parse_args()
box = args.box

GPIO.setmode(GPIO.BCM)

# Sensor pins
a_pin = 18
b_pin = 23

# Selection pins
s0_pin = 4
s1_pin = 17
s2_pin = 27
s3_pin = 22

def discharge():
  GPIO.setup(a_pin, GPIO.IN)
  GPIO.setup(b_pin, GPIO.OUT)
  GPIO.output(b_pin, False)
  time.sleep(0.005)

def charge_time():
  GPIO.setup(b_pin, GPIO.IN)
  GPIO.setup(a_pin, GPIO.OUT)
  count = 0
  GPIO.output(a_pin, True)
  while not GPIO.input(b_pin):
      count = count +1
  return count

def analog_read():
  discharge()
  return charge_time()

def sensor_sel(sensor):
  GPIO.setup(s0_pin, GPIO.OUT)
  GPIO.setup(s1_pin, GPIO.OUT)
  GPIO.setup(s2_pin, GPIO.OUT)
  GPIO.setup(s3_pin, GPIO.OUT)
  cases = {
    0:"0000", 
    1:"0001",
    2:"0010",
    3:"0011",
    4:"0100",
    5:"0101",
    6:"0110",
    7:"0111",
    8:"1000", 
    9:"1001", 
   10:"1010",
   11:"1011",
   12:"1100",
   13:"1101",
   14:"1110",
   15:"1111"
  }
  # Get binary for the mux
  sel = cases.get(sensor, 'Invalid sensor') 
  # Changes output to correspond to selected sensor
  if(int(sel[0])):
    GPIO.output(s3_pin, True)
  else:
    GPIO.output(s3_pin, False)
  if(int(sel[1])):
    GPIO.output(s2_pin, True)
  else:
    GPIO.output(s2_pin, False)
  if(int(sel[2])):
    GPIO.output(s1_pin, True)
  else:
    GPIO.output(s1_pin, False)
  if(int(sel[3])):
    GPIO.output(s0_pin, True)
  else:
    GPIO.output(s0_pin, False)

def output_vals(box, reading):
  box_file = '../meas_data/box_' + str(box) + '/moisture.txt'
 
  try:
    with open(box_file, mode='a') as file:
      file.write(str(reading)+'\n')
      file.close()
  except IOError as err:
    print('Could not read file ', box_file)
    print(err)
    return False

# Use user set input to choose box then output reading
# only if called directly
if __name__ == '__main__':
  sensor_sel(box)
  output_vals(box,analog_read())

GPIO.cleanup()

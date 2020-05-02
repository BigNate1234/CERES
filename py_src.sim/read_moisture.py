'''
||
|| @file        read_moisture.py
|| @version     1.1
|| @author      Nathaniel Furman
|| @contact     nfurman@ieee.org
||
|| @description
|| | Select multiplexer inputs and read sensor data.
|| #
||
|| @license
|| | This library is free software; you can redistribute it and/or
|| | modify it under the terms of the GNU Lesser General Public
|| | License as published by the Free Software Foundation; version
|| | 2.1 of the License.
|| |
|| | This library is distributed in the hope that it will be useful,
|| | but WITHOUT ANY WARRANTY; without even the implied warranty of
|| | MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
|| | Lesser General Public License for more details.
|| |
|| | You should have received a copy of the GNU Lesser General Public
|| | License along with this library; if not, write to the Free Software
|| | Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
|| #
||
'''

import RPi.GPIO as GPIO
import time
import argparse

def discharge(a_pin,b_pin):
  # Required to be enabled
  return
  GPIO.setup(a_pin, GPIO.IN)
  GPIO.setup(b_pin, GPIO.OUT)
  GPIO.output(b_pin, False)
  time.sleep(0.005)
  GPIO.cleanup()

def charge_time(a_pin,b_pin):
  # Required to be enabled
  return
  GPIO.setup(b_pin, GPIO.IN)
  GPIO.setup(a_pin, GPIO.OUT)
  count = 0
  GPIO.output(a_pin, True)
  while not GPIO.input(b_pin):
      count = count +1
  GPIO.cleanup()
  return count

def analog_read(a_pin,b_pin):
  # Required to be enabled
  return 150
  discharge()
  return charge_time()

def sensor_sel(sensor,s0_pin,s1_pin,s2_pin,s3_pin):
  # Required to be enabled
  return
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
  GPIO.cleanup()

def output_vals(box, reading):
  box_file = '/home/pi/CERES/meas_data/box_' + str(box) + '/moisture.txt'
 
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
  parser = argparse.ArgumentParser(description='Select box num.')
  parser.add_argument('box', metavar='box',type=int,
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

  sensor_sel(box,s0_pin,s1_pin,s2_pin,s3_pin)
  output_vals(box,analog_read(a_pin,b_pin))

'''
|| @changelog
|| | 1.0 2020-04-30 - Nathaniel Furman : Initial Release
|| | 1.1 2020-04-30 - Nathaniel Furman : Updated importing
|| | 1.2 2020-05-01 - Nathaniel Furman : Included pin parameters
|| #
'''

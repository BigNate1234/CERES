'''
||
|| @file 	move_dist.py
|| @version	1.0
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Move a specified distance
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

import gpiozero
import time
import argparse

parser = argparse.ArgumentParser(description='Move distance?')
parser.add_argument('d', metavar='dist',default=-1, type=float,
                    help='The distance to move in mm.')
args = parser.parse_args()
dist = args.d

#print(dist)

def remap(x, oMin, oMax, nMin, nMax):

  #range check
  if oMin == oMax:
    print("Warning: Zero input range")
    return None

  if nMin == nMax:
    print("Warning: Zero output range")
    return None

  #check reversed input range
  reverseInput = False
  oldMin = min( oMin, oMax )
  oldMax = max( oMin, oMax )
  if not oldMin == oMin:
    reverseInput = True

  #check reversed output range
  reverseOutput = False   
  newMin = min( nMin, nMax )
  newMax = max( nMin, nMax )
  if not newMin == nMin :
    reverseOutput = True

  portion = (x-oldMin)*(newMax-newMin)/(oldMax-oldMin)
  if reverseInput:
    portion = (oldMax-x)*(newMax-newMin)/(oldMax-oldMin)

  result = portion + newMin
  if reverseOutput:
    result = newMax - portion

  return result

# Need to map between distance and time moved
distBound = 200 # mm
speed = 40 # mm/s
maxTime = distBound / speed # s
t = round(remap(dist, -distBound, distBound, -maxTime, maxTime),2)
# Scale time to get milliseconds
t *= 1000

print('Max time: ',maxTime,' seconds')
print(t,' milliseconds')

# Signal pin
pin = 26
# Duty cycle of signal
dc = 80.0
# Frequency of signal
freq = 10000
cont = True
while freq < 999 and cont:
  response = 'a'
  while response != 'y' and response != 'n' and cont:
    response = input('Frequency is low, are you sure? (y/n) ')
    response = response.lower()
    if response == 'n':
      while True:
        response = input('Please type new frequency or exit: ')
        if response.lower() == 'exit':
          print('Exiting...')
          exit()
        elif response.isdecimal():
          freq = int(response)
          cont = False
          break
        else:
          continue
    elif response == 'y':
      cont = False
      break
    else:
      continue
# Run Time in seconds

onTime = dc / freq
offTime = (100.0-dc) / freq
cycleNum = int(t/1000 * freq/100) # Scale because DC not 0<x<1
print('CycleNum = ',cycleNum)
print('onTime   = ',onTime)
print('offTime  = ',offTime)

# active_high=True -> Usually off, natural behavior
# mult. Freq by 100 to get smoother behavior
p = gpiozero.PWMOutputDevice(pin,active_high=True,frequency=(freq*100))
try:
   # If background False, program will wait
   # If background True , program will continue
   startTime = time.time()
   p.blink(on_time=onTime,off_time=offTime,n=cycleNum,background=False)
   endTime = time.time()
except KeyboardInterrupt:
    pass
p.off()
print('Time on: ',str(round(endTime - startTime,3)*1000),' ms')

'''
|| @changelog
|| | 1.0 2020-04-30 - Nathaniel Furman : Initial Release
|| #
'''

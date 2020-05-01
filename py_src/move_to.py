'''
||
|| @file 	move_to.py
|| @version	1.1
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Move to a specified location.
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

def get_time(dist):
  # Need to map between distance and time moved
  distBound = 200 # mm
  speed = 40 # mm/s
  maxTime = distBound / speed # s
  t = round(remap(dist, -distBound, distBound, -maxTime, maxTime),2)
  return t*1000

def move(t,pin):
  # Duty cycle of signal
  dc = 80.0
  # Frequency of signal
  freq = 10000
  onTime = dc / freq
  offTime = (100.0-dc) / freq
  cycleNum = int(t/1000 * freq/100) # Scale because DC not 0<x<1
  
  p = gpiozero.PWMOutputDevice(pin,active_high=True,frequency=(freq*100))
  try:
     p.blink(on_time=onTime,off_time=offTime,n=cycleNum,background=False)
  except KeyboardInterrupt:
     pass
  p.off()

if __name__=='__main__':
  parser = argparse.ArgumentParser(description='Move location?')
  parser.add_argument('x', metavar='xCord',default=-1, type=float,
                      help='The x location in mm.')
  parser.add_argument('y', metavar='yCord',default=-1, type=float,
                      help='The y location in mm.')
  args = parser.parse_args()
  xLoc = args.x
  yLoc = args.y
  
  if xLoc < 0.0 or yLoc < 0.0:
    while xLoc < 0.0 or yLoc < 0.0:
      print('Please input positive coordinates.')
      try:
        xLoc = float(input('X Location:'))
        yLoc = float(input('Y Location:'))
      except ValueError:
        print('Please input a valid number.')
  
  print('X Location=',xLoc,'mm')
  print('Y Location=',yLoc,'mm')
  
  print('Moving to location...')
  tx = get_time(xLoc)
  ty = get_time(yLoc)
  # Signal pin
  xPin = 26
  yPin = 13
  move(tx, xPin)
  move(ty, yPin)
  print('Done.')

'''
|| @changelog
|| | 1.0 2020-04-30 - Nathaniel Furman : Initial Release
|| | 1.1 2020-04-30 - Nathaniel Furman : Updated importing
|| #
'''

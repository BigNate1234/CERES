'''
||
|| @file 	fluid_control.py
|| @version	1.0
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Control the fluid sub-system.
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

import argparse
import gpiozero

# Turn on relays
# Turn on valves
# Wait
# Turn off automatically

parser = argparse.ArgumentParser(description='Volume required?')
parser.add_argument('v', metavar='volume',default=-1, type=float,
                    help='Volume for the pumps to flow.')
args = parser.parse_args()
vol = args.v

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

def get_time(vol):
  # Need to map between distance and time moved
  volBound = 20 # mL
  rate = 5 # mL/s
  maxTime = volBound / rate # s
  t = round(remap(vol, -distBound, distBound, -maxTime, maxTime),2)
  # Scale time to get milliseconds
  return t

def flow(t, relayPin, valvePin):
  # Duty cycle of signal
  dc = 100.0
  # Frequency of signal
  freq = 10000
  onTime = dc / freq
  offTime = 0.0
  cycleNumRelay = int(t * 1.2 * freq/100) # Gives more time for pump
  cycleNumValve = int(t * freq/100) # Scale because DC not 0<x<1
  
  pR = gpiozero.PWMOutputDevice(relayPin,active_high=True,frequency=(freq*100))
  pV = gpiozero.PWMOutputDevice(valvePin,active_high=True,frequency=(freq*100))
  try:
     pR.blink(on_time=onTime,off_time=offTime,n=cycleNumRelay,background=False)
     pV.blink(on_time=onTime,off_time=offTime,n=cycleNumValve,background=False)
  except KeyboardInterrupt:
     pass
  p.off()

if __name__=='__main__':
  print('Pumping fluid...')
  t = get_time(vol)
  # Signal pin
  rPin = 5
  vPin = 12
  flow(t, rPin, vPin)
  print('Done.')

'''
|| @changelog
|| | 1.0 YYYY-MM-DD - Nathaniel Furman : Initial Release
|| #
'''

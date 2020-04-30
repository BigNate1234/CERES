'''
||
|| @file 	lighting_control.py
|| @version	1.0
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Control the intensity and timing of the lights.
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
import time

parser = argparse.ArgumentParser(description='Light time')
parser.add_argument('t', metavar='onTime',default=-1, type=float,
                    help='The time the lights are on in hours.')
parser.add_argument('--i', metavar='intensity',default=80.0, type=float,
                    help='The intensity of the lights, between 0-100.')

args = parser.parse_args()
i = args.i
t = args.t

if t < 0.0 or i < 0.0 or i > 100.0:
  if __name__=='__main__':
    while t < 0.0 or i < 0.0 or i > 100.0:
      print('Please input positive time and intensity between 0-100.')
      try:
        t = float(input('Time on (hours):'))
        i = float(input('Intensity (0-100):'))
      except ValueError:
        print('Please input a valid number.')

def lights_on(i,t,pin):
  # Duty cycle of signal
  dc = i
  # Frequency of signal
  freq = 10000
  onTime = dc / freq
  offTime = (100.0-dc) / freq
  cycleNum = int(t*60 * freq/100) # Scale because DC not 0<x<1
  
  # active_high=True -> Usually off, natural behavior
  # mult. Freq by 100 to get smoother behavior
  p = gpiozero.PWMOutputDevice(pin,active_high=True,frequency=(freq*100))
  try:
     # If background False, program will wait
     # If background True , program will continue
     #startTime = time.time()
     p.blink(on_time=onTime,off_time=offTime,n=cycleNum,background=True)
     #endTime = time.time()
  except KeyboardInterrupt:
     pass
#  print('Time on: ',str(round(endTime - startTime,3)),' s')
  p.off()

if __name__=='__main__':
  lightingPin = 12
  lights_on(i, t, lightingPin)
  print('Done.')

'''
|| @changelog
|| | 1.0 YYYY-MM-DD - Nathaniel Furman : Initial Release
|| #
'''

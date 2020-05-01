'''
||
|| @file 	main.py
|| @version	1.0
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Integration of sub-systems.
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

import constant
import argparse
import threading
import time
import fluid_control
import lighting_control
import move_to
import read_moisture

# GPIO Pin assignments:

# Fluid sub-system:
rPin = constant.RELAY
vPin = constant.VALVE
wateringThresh = constant.WATERING_THRESHOLD
volThresh = constant.VOLUME_THRESHOLD

# Lighting sub-system:
lPin = constant.LIGHTS
lIntensity = constant.LIGHT_INTENSITY
lOnTime = constant.LIGHTS_ON
lOffTime = constant.LIGHTS_OFF

# Gantry sub-system:
xPin = constant.XMOTOR
yPin = constant.YMOTOR

# Sensor readings:
cPin = constant.CHARGE
dPin = constant.DISCHARGE
s0Pin = constant.S0
s1Pin = constant.S1
s2Pin = constant.S2
s3Pin = constant.S3

boxList = [0,1,2]

if __name__=='__main__':
  # Start thread to run lighting
  # This will exit when main.py exits (because daemon is True)
  lightThread = threading.Thread(target=lighting_control.always_cycle,
		args=(lIntensity,.01,lPin,.01), daemon=True)
  lightThread.start() 

  while True:
    try:
      for box in boxList:
        print('Reading moisture in plant:',str(box),'...')
        read_moisture.sensor_sel(box,s0Pin,s1Pin,s2Pin,s3Pin)
        value = read_moisture.analog_read(cPin,dPin)
        read_moisture.output_vals(box,value)
        print('\treading=',str(value))
        if value <= wateringThresh:
          print('** VALUE BELOW THRESHOLD **')
          # Means need to water plant
          # Retrieve coordinates of current box
          xLoc = constant.BOX_XCORDS[box]
          yLoc = constant.BOX_YCORDS[box]
      
          # Calculate time needed to move
          tx = move_to.get_time(xLoc)
          ty = move_to.get_time(yLoc)
          
          print('Moving to box...')
          # Actually move to location
          move_to.move(tx,xPin)
          move_to.move(ty,yPin)
      
          print('Pushing fluid to box...')
          # Calculate time needed to turn on pumps for
          tF = fluid_control.get_time(volThresh)
          # Actually turn pumps on for that time
          fluid_control.flow(tF,rPin,vPin)
          # Automatically waits to finish
      
          # Moves on to next box

      # Out of for loop, wait ten minutes before next measurement cycle
      print('Checked each box, entering cool-down.')
      time.sleep(10)
    except KeyboardInterrupt:
      print('\n\nExiting...')
      break

'''
|| @changelog
|| | 1.0 YYYY-MM-DD - Nathaniel Furman : Initial Release
|| #
'''

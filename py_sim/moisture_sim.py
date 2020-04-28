'''
||
|| @file 	moisture_sim.py
|| @version	1.0
|| @author	Nathaniel Furman
|| @contact	nfurman@ieee.org
||
|| @description
|| | Simulate analog moisture readings.
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

import fileinput
import random
import sys

# How many data points to include?
numPoints = 1000

# Threshold to water
thresh = 250

# Max water plants start with
max_water = 700

# Use rate (how fast plants use water)
rate = 5

# Sensor error fluctuation
error = .5

# Box Num (1 through 15)
box = 3

# Data output path
file_name= '../meas_data/box_' + str(box) + '/moisture.txt'

try:
  file = open(file_name, mode='a')
except IOError:
  print('Could not open file, ', file_name)
  sys.exit()

value = max_water
for i in range(0,numPoints):
  randVal = round(int(random.random()*100)/100 - error,2)
  value = round(value - rate + randVal,2) 
#  print('Rand: ',randVal,'\t\tVal: ',value)
  if value < thresh:
    value = max_water # Like the plant is watered
#    print(value)
  file.write(str(value)+'\n')

file.close()

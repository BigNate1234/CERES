'''
+----------------------------+                    Pin 1 Pin2
|()2#################40() +---+                +3V3 [ ] [ ] +5V
|  1#################39   |USB|      SDA1 / GPIO  2 [ ] [ ] +5V
|#D    Pi B+ / Pi 2 +-+   +---+      SCL1 / GPIO  3 [ ] [ ] GND
|#I   \/  +--+      | |   +---+             GPIO  4 [ ] [ ] GPIO 14 / TXD0
|#S  ()() |  | CAM  +-+   |USB|                 GND [ ] [ ] GPIO 15 / RXD0
|#P   ()  +--+  #         +---+             GPIO 17 [ ] [ ] GPIO 18
|#Y             #        +----+             GPIO 27 [ ] [ ] GND
|        +----+ # +-+    | NET|             GPIO 22 [ ] [ ] GPIO 23
|()+---+ |    | # |A|  ()+----+                +3V3 [ ] [ ] GPIO 24
+--|PWR|-|HDMI|---|V|--------+       MOSI / GPIO 10 [ ] [ ] GND
   +---+ +----+   +-+                MISO / GPIO  9 [ ] [ ] GPIO 25
                                     SCLK / GPIO 11 [ ] [ ] GPIO  8 / CE0#
                                                GND [ ] [ ] GPIO  7 / CE1#
                                    ID_SD / GPIO  0 [ ] [ ] GPIO  1 / ID_SC
                                            GPIO  5 [ ] [ ] GND
                                            GPIO  6 [ ] [ ] GPIO 12
                                            GPIO 13 [ ] [ ] GND
                                     MISO / GPIO 19 [ ] [ ] GPIO 16 / CE2#
                                            GPIO 26 [ ] [ ] GPIO 20 / MOSI
                                                GND [ ] [ ] GPIO 21 / SCLK
                                                 Pin 39 Pin 40
'''


# Pin assignments and other constants needed.

# Fluid
RELAY = 5
VALVE = 12
WATERING_THRESHOLD = 250.0 # Analog moisture sensor reading
VOLUME_THRESHOLD = 15 # mL of water to add

# Lighting
LIGHTS = 24
LIGHT_INTENSITY = 80.0
LIGHTS_ON = 16 # hours
LIGHTS_OFF = 8 # hours

# Gantry
XMOTOR = 26
YMOTOR = 13

# Sensors
CHARGE = 18
DISCHARGE = 23 
S0 = 4
S1 = 17
S2 = 27
S3 = 22

# Box coordinates
BOX_XCORDS = {
  0:5,
  1:25,
  2:5,
  3:25,
}

BOX_YCORDS = {
  0:5,
  1:5,
  2:25,
  3:25
}
# and so on...

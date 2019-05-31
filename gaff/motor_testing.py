import sys
from time import sleep

# config
sys.path.insert(0, "/home/pi/packages")
#import RPi.GPIO as GPIO

from RaspberryPiCommon.pidev import stepper, RPiMIB

import Slush

sys.path.insert(0, "/home/pi/packages/Adafruit_Python_ADS1x15/examples")
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()
motor_1 = stepper(port = 0, speed = 120, micro_steps = 128)

print("made motor 1")
motor_1.home(0)
print("homed motor 1")
sleep(.5)
home_pos_1 = 24.123
motor_1.go_to_position(home_pos_1)
increment = 5

clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)

def deadzone(n, abs_diff):
    if (n < abs_diff and n > -(abs_diff)):
        n = 0
        return n
    else:
        return n

def joy_val_filter(n, abs_diff, min_n, max_n):
    return deadzone(clamp(n, min_n, max_n), abs_diff)
    
def control_y1():
        current_pos_x = home_pos_1
        joy_val_x = -round((adc.read_adc(1, gain=1)-9500)/9500, 2) 
        joy_val_x = joy_val_filter(joy_val_x, 0.1, -1, 1)
        current_pos_x = current_pos_x + joy_val_x*increment
        current_pos_x = clamp(current_pos_x, home_pos_1 - 13, home_pos_1 + 13)
        motor_1.start_go_to_position(current_pos_x)
        print(joy_val_x)

current_pos_x = home_pos_1
while True:
    control_y1()
##    joy_val_x = round((adc.read_adc(3, gain=1)-9500)/9500, 2)
##    joy_val_x = joy_val_filter(joy_val_x, 0.1, -1, 1)
##    current_pos_x = current_pos_x + joy_val_x*increment
##    current_pos_x = clamp(current_pos_x, home_pos_1 - 13, home_pos_1 + 13)
##    motor_1.start_go_to_position(current_pos_x)
##    print(joy_val_x)
     

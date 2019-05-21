import board
import busio
import time
import sys
import RPi.GPIO as GPIO
sys.path.insert(0, "/home/pi/packages")
from RaspberryPiCommon.pidev import stepper, RPiMIB

import Slush
import spidev
from time import sleep
from threading import Thread
from multiprocessing import Process
sys.path.insert(0, "/home/pi/packages/Adafruit_Python_PCA9685")
from Adafruit_PCA9685 import PCA9685

sys.path.insert(0, "/home/pi/packages/Adafruit_16_Channel_PWM_Module_Easy_Library")
print("pre-import")
import Adafruit_Ease_Lib as ael
print("post-import")
led = ael.Adafruit_Ease_Lib()
print("post-object")

sys.path.insert(0, "/home/pi/packages/Adafruit_Python_ADS1x15/examples")
# Import the ADS1x15 module.
##import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
##adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

led.change_frequency(2000)

pwms = [0, 1, 2]

##print(adc.read_adc(1, gain = GAIN))

print("set up pwm and direction channels")

def motor_setup():
     print("start motor setup")
     
##     #MOTOR 1 SETUP
##     motor_1 = stepper(port = 1, speed = 20, micro_steps = 128)
##     print("g")
##     motor_1.home(0)
##     print("homed motor 1")
##     sleep(.5)
##     home_pos_1 = 11.34
##     motor_1.go_to_position(home_pos_1)
##
##     print("set up motor 1")
     
     #MOTOR 2 SETUP
     motor_2 = stepper(port=0, speed=30, micro_steps=128)
     motor_2.home(0)
     print("homed motor 2")
     sleep(.5)
     home_pos_2 = 24.123
     motor_2.go_to_position(home_pos_2)

     print("set up motor 2")
     
##motor_2 = stepper(port=0, speed=30, micro_steps=128)
##motor_2.home(0)
##print("homed motor 2")
##sleep(.5)
##home_pos_2 = 24.123
##motor_2.go_to_position(home_pos_2)

print("set up motor 2")

print("setup motors")

def pwm_to_knob():
     print('there')
     prev_dc = 0
     while True:
         # print(int((adc.read_adc(0, gain=GAIN) - 2672)*(100/16400))) 
          dc_1 = int(((adc.read_adc(0, gain=GAIN)) - 2672)*(100/16400))
          if not dc_1 == prev_dc:
               led.change_percentage(pwms, dc_1)
          prev_dc = dc_1
         # print(int(((adc.read_adc(0, gain=GAIN)) - 2672)*(100/16400)))
          
import math
##motor_setup()
home_pos_1 = 11.34
#current_pos_y = home_pos_2
##current_pos_x = home_pos_1
increment = 5
clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
def move_to_joy():
     print('start moveA_to_joy')
     current_pos_x = home_pos_1
     while True:
          joy_val_x = abs(9500 - adc.read_adc(1, gain=GAIN))
          #joy_val_y = abs(9500 - adc.read_adc(2, gain=GAIN))
          print(joy_val_x)
          #print(joy_val_y)
          current_pos_x = current_pos_x + joy_val_x*increment
          #current_pos_x = current_pos_x + joy_val_x*increment
          current_pos_x = clamp(current_pos_x, home_pos_1 - 13, home_pos_1 + 13)
       #   current_pos_x = clamp(current_pos_x, home_pos_1 - 15.77, home_pos_ + 15.77)
          motor_2.start_go_to_position(current_pos_x)
          
motor_thread = Thread(target = move_to_joy)
led_thread = Thread(target = pwm_to_knob)
print('here')

##motor_thread.start()
##led_thread.start()
print("started threading")

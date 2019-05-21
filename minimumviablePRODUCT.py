import math
import sys
sys.path.insert(0, "/home/pi/packages")

import RPi.GPIO as GPIO

from RaspberryPiCommon.pidev import stepper, RPiMIB

import Slush
import spidev

import pygame
from time import sleep
sys.path.insert(0, "/home/pi/packages/Adafruit_16_Channel_PWM_Module_Easy_Library")
print("pre-import")
import Adafruit_Ease_Lib as ael
print("post-import")
led = ael.Adafruit_Ease_Lib()
print("post-object")

from threading import Thread
from multiprocessing import Process

sys.path.insert(0, "/home/pi/packages/Adafruit_Python_ADS1x15/examples")
# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc_red = Adafruit_ADS1x15.ADS1115(0x4A)
adc_blue = Adafruit_ADS1x15.ADS1115(0x48)
adc_green = Adafruit_ADS1x15.ADS1115(0x49)


clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)

##########################################
#############KNOB CONTROLS################
##########################################

GAIN = 1

led.change_frequency(2000)

pwms = [0, 1, 2]

#led.change_percentage(pwms, 30)

##print(adc_blue.read_adc(1, gain = GAIN))

def value_as_percent(color, value):
    if color == "red":
        return ((value-4360)*100)/(15504-4360)
    if color == "green":
        return ((value-3850)*100)/(14832-3850)
    if color == "blue":
        return ((value-100)*100)/(11280-100)
    
def knob_red():   
    while True:
        sleep(.00001)
##        print(clamp(value_as_percent("red", adc_red.read_adc(0, gain = GAIN)), 0, 100))
        led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain = GAIN)), 0, 100))

def knob_blue():
    while True:
        sleep(.00001)
        led.change_percentage(2, clamp(value_as_percent("blue", adc_blue.read_adc(0, gain = GAIN)), 0, 100))

def knob_green():
    while True:
        sleep(.00001)
        #print(clamp(value_as_percent("green", adc_green.read_adc(0, gain = GAIN)), 0, 100))
        led.change_percentage(1, clamp(value_as_percent("green", adc_green.read_adc(0, gain = GAIN)), 0, 100))




r = Thread(target = knob_red)
b = Thread(target = knob_blue)
g = Thread(target = knob_green)
r.start()
b.start()
g.start()
    
##########################################
###########JOYSTICK CONTROLS##############
##########################################



print("set up pwm and direction channels")
HORIZONTAL_AXIS = 0
VERTICAL_AXIS = 1

pygame.init()
pygame.joystick.init()

##MAKE JOYSTICKS
joystickR = pygame.joystick.Joystick(0)
joystickR.init()

joystickG = pygame.joystick.Joystick(1)
joystickG.init()

joystickB = pygame.joystick.Joystick(2)
joystickB.init()

print("made joysticks")

home_pos_x = -11.5
home_pos_y = 25

#MOTOR 0 SETUP
motor_0 = stepper(port = 0, speed = 20, micro_steps = 128)
##print("made motor 0")
##motor_0.home(0)
##print("homed motor 0")
##sleep(.5)
##motor_0.go_to_position(home_pos_y)
print("motor 0 set up")

#MOTOR 1 SETUP
motor_1 = stepper(port=1, speed=30, micro_steps=128)
##motor_1.home(1)
##print("homed motor 1")
##sleep(.5)
##motor_1.go_to_position(home_pos_x)
print("motor 1 set up")

###MOTOR 2 SETUP
motor_2 = stepper(port = 2, speed = 20, micro_steps = 128)
##motor_2.home(0)
##print("homed motor 2")
##sleep(.5)
##motor_2.go_to_position(home_pos_y)
print("motor 2 set up")

###MOTOR 3 SETUP
motor_3 = stepper(port=3, speed=30, micro_steps=128)
motor_3.home(1)
print("homed motor 3")
sleep(.5)
motor_3.go_to_position(home_pos_x)
print("motor 3 set up")

###MOTOR 4 SETUP
motor_4 = stepper(port = 4, speed = 20, micro_steps = 128)
motor_4.home(0) 
print("homed motor 4")
sleep(.5)
motor_4.go_to_position(home_pos_y)
print("motor 4 set up")

###MOTOR 5 SETUP
##motor_5 = stepper(port=5, speed=30, micro_steps=128)
##motor_5.home(0)``
##print("homed motor 5")
##sleep(.5)
##motor_5.go_to_position(home_pos_x)
print("motor 5 set up")

current_pos_yr = home_pos_y
current_pos_xr = home_pos_x

current_pos_yg = home_pos_y
current_pos_xg = home_pos_x

current_pos_yb = home_pos_y
current_pos_xb = home_pos_x

clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
increment = 5

##blue_joy_x = adc_blue.read_adc(2,gain = GAIN) #0-16400 --> 
##blue_joy_y = adc_blue.read_adc(3, gain = GAIN)

##while True:
##    sleep(.00001)
####    blue_joy_x = adc_blue.read_adc(2,gain = GAIN) #0-16400 --> 
####    blue_joy_y = adc_blue.read_adc(3, gain = GAIN)
##    print(adc_blue.read_adc(2, gain = GAIN))#(blue_joy_x - 8200)/16)

def gimblegimblegimble(gimble_color): #dear future spectator: look i know this is bad but we had sixty minutes to write this whole file and you shouldn't criticise 
    pygame.event.pump()
    print('gimblegimblegimble?')
    current_pos_yb = home_pos_y
    current_pos_xb = home_pos_x
    if gimble_color == "red":
        joy_val_xr = joystickR.get_axis(HORIZONTAL_AXIS)
        joy_val_yr = joystickR.get_axis(VERTICAL_AXIS)
        current_pos_yr = current_pos_yr + joy_val_yr*increment
        current_pos_xr = current_pos_xr + joy_val_xr*increment
        current_pos_yr = clamp(current_pos_yr, home_pos_y - 13, home_pos_y + 13)
        current_pos_xr = clamp(current_pos_xr, home_pos_x - 15.77, home_pos_x + 15.77)
        motor_1.start_go_to_position(current_pos_yr) 
        motor_2.start_go_to_position(current_pos_xr)
    if gimble_color == "green":
        joy_val_xg = joystickG.get_axis(HORIZONTAL_AXIS)
        joy_val_yg = joystickG.get_axis(VERTICAL_AXIS)
        current_pos_yg = current_pos_yg + joy_val_yg*increment
        current_pos_xg = current_pos_xg + joy_val_xg*increment
        current_pos_yg = clamp(current_pos_yg, home_pos_y - 13, home_pos_y + 13)
        current_pos_xg = clamp(current_pos_xg, home_pos_x - 15.77, home_pos_x + 15.77)
        motor_1.start_go_to_position(current_pos_yg) 
        motor_2.start_go_to_position(current_pos_xg)
    if gimble_color == "blue":
        print('bleu')
        joy_val_xb = joystickB.get_axis(HORIZONTAL_AXIS)
        joy_val_yb = joystickB.get_axis(VERTICAL_AXIS)
        current_pos_yb = current_pos_yb + joy_val_yb*increment
        current_pos_xb = current_pos_xb + joy_val_xb*increment
        current_pos_yb = clamp(current_pos_yb, home_pos_y - 13, home_pos_y + 13)
        current_pos_xb = clamp(current_pos_xb, home_pos_x - 15.77, home_pos_x + 15.77)
        motor_1.start_go_to_position(current_pos_yb) 
        motor_2.start_go_to_position(current_pos_xb)

##while True:
##    gimblegimblegimble("blue")



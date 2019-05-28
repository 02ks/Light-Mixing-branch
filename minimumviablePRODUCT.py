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

led.change_percentage(pwms, 100)

##print(adc_blue.read_adc(1, gain = GAIN))

def value_to_m(value):
    if value < 5:
        return 0
    if value > 95:
        return 100
    else:
        return value

def value_as_percent(color, value):
    if color == "red":
        return value_to_m(((value-4360)*100)/(15504-4360))
    if color == "green":
        return value_to_m(((value-3850)*100)/(14832-3850))
    if color == "blue":
        return value_to_m(((value-100)*100)/(11280-100))
    
def knob_red():   
    while True:
##        sleep(.00001)
        print(clamp(value_as_percent("red", adc_red.read_adc(0, gain = GAIN)), 0, 100))
        led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain = GAIN)), 0, 100))

def knob_blue():
    while True:
##        sleep(.00001)
##        print(clamp(value_as_percent("blue", adc_blue.read_adc(0, gain = GAIN)), 0, 100))        
        led.change_percentage(2, clamp(value_as_percent("blue", adc_blue.read_adc(0, gain = GAIN)), 0, 100))

def knob_green():
    while True:
##        sleep(.00001)
##        print(clamp(value_as_percent("green", adc_green.read_adc(0, gain = GAIN)), 0, 100))
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
from Slush.Devices import L6470Registers as LReg6470
from Slush.Devices import L6480Registers as LReg6480
from pidev.slush_manager import slush_board

home_pos_x = -11.5
home_pos_y = 25
board = 'D'
if board is 'D':
        current = 30
        
        motor_1 = stepper(port = 1, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        while motor_1.isBusy():
                continue
        motor_1.print_status()
        print("Stepper 1 Initial CONFIG Register: " + hex(motor_1.getParam(LReg6480.CONFIG)))
        print("Stepper 1 Intial GATECFG1 Register: " + hex(motor_1.getParam(LReg6480.GATECFG1)))
        motor_1.setParam(LReg6480.GATECFG1, 0x5F)
        while motor_1.isBusy():
                continue
        print("Stepper 1 Updated GATECFG1 Register: " + hex(motor_1.getParam(LReg6480.GATECFG1)))
        print("Stepper 1 Intial OCD_TH Register: " + hex(motor_1.getParam(LReg6480.OCD_TH)))
        motor_1.setParam(LReg6480.OCD_TH, 0x1F)
        while motor_1.isBusy():
                continue
        print("Stepper 1 Updated OCD_TH Register: " + hex(motor_1.getParam(LReg6480.OCD_TH)))
        motor_1.setParam(LReg6480.CONFIG, 0x3688)
        while motor_1.isBusy():
                continue
        print("Stepper 1 Updated CONFIG Register: " + hex(motor_1.getParam(LReg6480.CONFIG)))
        motor_1.print_status()
        
        motor_2 = stepper(port = 2, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        while motor_2.isBusy():
                continue
        motor_2.print_status()
        print("Stepper 2 Initial CONFIG Register: " + hex(motor_2.getParam(LReg6480.CONFIG)))
        print("Stepper 2 Intial GATECFG1 Register: " + hex(motor_2.getParam(LReg6480.GATECFG1)))
        motor_2.setParam(LReg6480.GATECFG1, 0x5F)
        while motor_2.isBusy():
                continue
        print("Stepper 2 Updated GATECFG1 Register: " + hex(motor_2.getParam(LReg6480.GATECFG1)))
        print("Stepper 2 Intial OCD_TH Register: " + hex(motor_2.getParam(LReg6480.OCD_TH)))
        motor_2.setParam(LReg6480.OCD_TH, 0x1F)
        while motor_2.isBusy():
                continue
        print("Stepper 2 Updated OCD_TH Register: " + hex(motor_2.getParam(LReg6480.OCD_TH)))
        motor_2.setParam(LReg6480.CONFIG, 0x3688)
        while motor_2.isBusy():
                continue
        print("Stepper 2 Updated CONFIG Register: " + hex(motor_2.getParam(LReg6480.CONFIG)))
        motor_2.print_status()
        
        motor_3 = stepper(port = 3, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        motor_3.print_status()
        print("Stepper 3 Initial CONFIG Register: " + hex(motor_3.getParam(LReg6470.CONFIG)))
        print("Stepper 3 Intial OCD_TH Register: " + hex(motor_3.getParam(LReg6470.OCD_TH)))
        motor_3.setParam(LReg6480.CONFIG, 0x3688)
        while motor_3.isBusy():
                continue
        print("Stepper 3 Updated CONFIG Register: " + hex(motor_3.getParam(LReg6470.CONFIG)))
        motor_3.print_status()

        motor_4 = stepper(port = 4, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        motor_4.print_status()
        print("Stepper 4 Initial CONFIG Register: " + hex(motor_4.getParam(LReg6470.CONFIG)))
        print("Stepper 4 Intial OCD_TH Register: " + hex(motor_4.getParam(LReg6470.OCD_TH)))
        motor_4.setParam(LReg6480.CONFIG, 0x3688)
        while motor_4.isBusy():
                continue
        print("Stepper 4 Updated CONFIG Register: " + hex(motor_4.getParam(LReg6470.CONFIG)))
        motor_4.print_status()

        motor_5 = stepper(port = 5, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        motor_5.print_status()
        print("Stepper 5 Initial CONFIG Register: " + hex(motor_5.getParam(LReg6470.CONFIG)))
        print("Stepper 5 Intial OCD_TH Register: " + hex(motor_5.getParam(LReg6470.OCD_TH)))
        motor_5.setParam(LReg6480.CONFIG, 0x3688)
        while motor_5.isBusy():
                continue
        print("Stepper 5 Updated CONFIG Register: " + hex(motor_5.getParam(LReg6470.CONFIG)))
        motor_5.print_status()

        motor_6 = stepper(port = 6, speed = 25, hold_current = current, run_current = current, accel_current = current, deaccel_current = current, micro_steps = 2)
        motor_6.print_status()
        print("Stepper 6 Initial CONFIG Register: " + hex(motor_6.getParam(LReg6470.CONFIG)))
        print("Stepper 6 Intial OCD_TH Register: " + hex(motor_6.getParam(LReg6470.OCD_TH)))
        motor_6.setParam(LReg6470.CONFIG, 0x3688)
        while motor_6.isBusy():
                continue
        print("Stepper 6 Updated CONFIG Register: " + hex(motor_6.getParam(LReg6470.CONFIG)))
        motor_6.print_status()

def setup_all_motors():
    #MOTOR 1 SETUP
    motor_1.home(0)
    print("homed motor 1")
    sleep(.5)
    motor_1.go_to_position(home_pos_y)
    print("motor 1 set up")

    #MOTOR 2 SETUP
    print('tryin to home')
    motor_2.home(0)
    print("homed motor 2")
    sleep(.5)
    motor_2.go_to_position(home_pos_y)
    print("motor 2 set up")

    #MOTOR 3 SETUP
    motor_3.home(0)
    print("homed motor 3")
    sleep(.5)
    motor_3.go_to_position(home_pos_y)
    print("motor 3 set up")
    
    #MOTOR 4 SETUP
    motor_4.home(1) 
    print("homed motor 4")
    sleep(.5)
    motor_4.go_to_position(home_pos_x)
    print("motor 4 set up")

    #MOTOR 5 SETUP
    motor_5.home(1)
    print("homed motor 5")
    sleep(.5)
    motor_5.go_to_position(home_pos_x)
    print("motor 5 set up")

    #MOTOR 6 SETUP
    motor_6.home(1)
    sleep(.5)
    motor_6.go_to_position(home_pos_x)
     
setup_all_motors()

current_pos_yr = home_pos_y
current_pos_xr = home_pos_x

current_pos_yg = home_pos_y
current_pos_xg = home_pos_x

current_pos_yb = home_pos_y
current_pos_xb = home_pos_x

clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
increment = 1

def joy_val_filter(value):
    if value < -0.9:
        return -1
    if value > 0.9:
        return 1
    if value > -0.1 and value < 0.1:
        return 0
    else:
        return value
    
def scale_joystick_value(value):
    return joy_val_filter((value - 6600)/6000)

def blue_joy_x(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
    global current_pos_xb
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_blue.read_adc(1, gain = GAIN))*increment)
        current_pos_xb += movement_amount
##        if current_pos_xb > home_pos_x - 15.77 and current_pos_xb < home_pos_x + 15.77:
##            motor_5.start_relative_move(movement_amount)
        current_pos_xb = clamp(current_pos_xb, home_pos_x - 15.77, home_pos_x + 15.77)
        #motor_5.start_go_to_position(current_pos_xb)
        if not movement_amount == 0:
            motor_5.start_relative_move(movement_amount)
        #print(current_pos_xb)
        
        #motor_3.start_go_to_position(current_pos_xb)
def blue_joy_y(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
##    global current_pos_yb
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_blue.read_adc(2, gain = GAIN))*increment)
##        if current_pos_yb > home_pos_y - 13 and current_pos_yb < home_pos_y + 13:
##            motor_3.start_relative_move(movement_amount)
##        current_pos_yb = current_pos_yb + movement_amount
        #current_pos_xg = clamp(current_pos_xg, home_pos_x - 15.77, home_pos_x + 15.77)
        #print(current_pos_yb)
        print(movement_amount)
        if not movement_amount == 0:
            motor_3.start_relative_move(movement_amount)

def green_joy_x(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_green.read_adc(1, gain = GAIN))*increment)
##        global current_pos_xg
##        if current_pos_xg > home_pos_x - 15.77 and current_pos_xg < home_pos_x + 15.77:
##            motor_6.start_relative_move(movement_amount)
##        current_pos_xg = current_pos_xg + movement_amount
        if not movement_amount == 0:
            motor_6.start_relative_move(movement_amount)
        #current_pos_xg = clamp(current_pos_xg, home_pos_x - 15.77, home_pos_x + 15.77)
        #print(current_pos_xg)
        
        #motor_3.start_go_to_position(current_pos_xb)
def green_joy_y(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_green.read_adc(2, gain = GAIN))*increment)
##        global current_pos_yg
##        if current_pos_yg > home_pos_y - 13 and current_pos_yg < home_pos_y + 13:
##            motor_2.start_relative_move(movement_amount)
##        current_pos_yg = current_pos_yg + movement_amount
        if not movement_amount == 0:            motor_2.start_relative_move(movement_amount)
        #current_pos_xg = clamp(current_pos_xg, home_pos_x - 15.77, home_pos_x + 15.77)
        #print(current_pos_yg)

def red_joy_x(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_red.read_adc(1, gain = GAIN))*increment)
##        global current_pos_xg
##        if current_pos_xg > home_pos_x - 15.77 and current_pos_xg < home_pos_x + 15.77:
##            motor_6.start_relative_move(movement_amount)
##        current_pos_xg = current_pos_xg + movement_amount
        if not movement_amount == 0:
            motor_4.start_relative_move(movement_amount)
        #current_pos_xg = clamp(current_pos_xg, home_pos_x - 15.77, home_pos_x + 15.77)

def red_joy_y(): ## WILL HAVE TO USE MOTORS 4 AND 5 IN THE FUTURE
    while True:
        movement_amount = joy_val_filter(scale_joystick_value(adc_red.read_adc(2, gain = GAIN))*increment)
##        global current_pos_xg
##        if current_pos_xg > home_pos_x - 15.77 and current_pos_xg < home_pos_x + 15.77:
##            motor_6.start_relative_move(movement_amount)
##        current_pos_xg = current_pos_xg + movement_amount
        if not movement_amount == 0:
            motor_1.start_relative_move(movement_amount)

      
blue_x = Thread(target = blue_joy_x)
blue_y = Thread(target = blue_joy_y)
green_x = Thread(target = green_joy_x)
green_y = Thread(target = green_joy_y)
red_x = Thread(target = red_joy_x)
red_y = Thread(target = red_joy_y)
##blue_x.start()
####blue_y.start()
green_x.start()
green_y.start()
##red_x.start()
####red_y.start()

while True:
    print("x : green %(green)s, blue %(blue)s, red %(red)s | y: green %(greeny)s blue %(bluey)s red %(redy)s"% {"green" : joy_val_filter(scale_joystick_value(adc_green.read_adc(1, 1))), "blue" : joy_val_filter(scale_joystick_value(adc_blue.read_adc(1, 1))), "red" : joy_val_filter(scale_joystick_value(adc_red.read_adc(1, 1))), "greeny":joy_val_filter(scale_joystick_value(adc_green.read_adc(2, 1))), "bluey":joy_val_filter(scale_joystick_value(adc_blue.read_adc(2, 1))), "redy":joy_val_filter(scale_joystick_value(adc_red.read_adc(2, 1)))})       



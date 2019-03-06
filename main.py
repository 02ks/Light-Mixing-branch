import math
import sys
sys.path.insert(0, "/home/pi/packages")

##from kivy.app import App
##from kivy.lang import Builder
##from kivy.core.window import Window
##from kivy.uix.screenmanager import ScreenManager, Screen
##from kivy.uix.button import Button
##from kivy.uix.floatlayout import FloatLayout
##from kivy.graphics import *
##from kivy.uix.popup import Popup
##from kivy.uix.label import Label
##from kivy.uix.widget import Widget
##from kivy.uix.slider import Slider
##from kivy.uix.image import Image
##from kivy.uix.behaviors import ButtonBehavior
##from kivy.clock import Clock
##from kivy.animation import Animation
##from functools import partial
##from kivy.config import Config
##from kivy.core.window import Window
from time import sleep

# config
##from kivy.config import Config
##
##Config.set('kivy', 'keyboard_mode', 'systemandmulti')
import RPi.GPIO as GPIO

from RaspberryPiCommon.pidev import stepper, RPiMIB

import Slush
import spidev

import pygame

HORIZONTAL_AXIS = 0
VERTICAL_AXIS = 1

pygame.init()
pygame.joystick.init()
joystick = pygame.joystick.Joystick(0)
joystick.init()

from threading import Thread
from multiprocessing import Process

#MOTOR 1 SETUP
motor_1 = stepper(port = 1, speed = 50, micro_steps = 128)
motor_1.home(0)
print("homed motor 1")
sleep(.5)
home_pos_1 = 11.34
motor_1.go_to_position(home_pos_1)

#MOTOR 2 SETUP
motor_2 = stepper(port=0, speed=50, micro_steps=128)
motor_2.home(0)
print("homed motor 2")
sleep(.5)
home_pos_2 = 24.123
motor_2.go_to_position(home_pos_2)

try:
    while True:
        pygame.event.pump()
        motor_1.start_go_to_position(home_pos_1-10*joystick.get_axis(HORIZONTAL_AXIS)) 
        motor_2.start_go_to_position(home_pos_2-15.77*joystick.get_axis(VERTICAL_AXIS))
##        print("x: " + str(45*joystick.get_axis(VERTICAL_AXIS)))
        print("y: "+ str(home_pos_1 - 10*joystick.get_axis(HORIZONTAL_AXIS)))
##    opposite ends are -36.702 and 35.051
except KeyboardInterrupt:
    sys.exit()

    

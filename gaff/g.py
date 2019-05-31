import board
import busio
import time
import sys
import RPi.GPIO as GPIO
sys.path.insert(0, "/home/pi/packages")
from RaspberryPiCommon.pidev import stepper, RPiMIB
sys.path.insert(0, "/home/pi/packages/Adafruit_16_Channel_PWM_Module_Easy_Library")
from Adafruit_Ease_Lib import Adafruit_Ease_Lib as ael
led = ael()

sys.path.insert(0, "/home/pi/packages/Adafruit_Python_ADS1x15/examples")
# Import the ADS1x15 module.
import Adafruit_ADS1x15

# Create an ADS1115 ADC (16-bit) instance.
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1
clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
import Slush
import spidev
increment = 5
motor_1 = stepper(port = 0, speed = 20, micro_steps = 128)
print("g")
motor_1.home(0)
home_pos_1 = 11.34
current_pos_x = home_pos_1
while True:
    joy_val_x = (adc.read_adc(1, gain=GAIN)-9408)/12000
    #joy_val_y = abs(9500 - adc.read_adc(2, gain=GAIN))
    print(joy_val_x)
    #print(joy_val_y)
    current_pos_x = current_pos_x + joy_val_x*increment
    #current_pos_x = current_pos_x + joy_val_x*increment
    current_pos_x = clamp(current_pos_x, home_pos_1 - 13, home_pos_1 + 13)
    #   current_pos_x = clamp(current_pos_x, home_pos_1 - 15.77, home_pos_ + 15.77)
    motor_1.start_go_to_position(current_pos_x)

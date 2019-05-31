# Simple demo of reading each analog input from the ADS1x15 and printing it to
# the screen.
# Author: Tony DiCola
# License: Public Domain
import time

# Import the ADS1x15 module.+3.2\[p-075t
import Adafruit_ADS1x15

#Make joystick value conversion functions and the required variables
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

increment = 1

# Create an ADS1115 ADC (16-bit) instance for each board.
adc_red = Adafruit_ADS1x15.ADS1115(0x4A)
adc_green = Adafruit_ADS1x15.ADS1115(0x49)
adc_blue = Adafruit_ADS1x15.ADS1115(0x48)

# Or create an ADS1015 ADC (12-bit) instance.
#adc = Adafruit_ADS1x15.ADS1015()

# Note you can change the I2C address from its default (0x48), and/or the I2C
# bus by passing in these optional parameters:
#adc = Adafruit_ADS1x15.ADS1015(address=0x49, busnum=1)

# Choose a gain of 1 for reading voltages from 0 to 4.09V.
# Or pick a different gain to change the range of voltages that are read:
#  - 2/3 = +/-6.144V
#  -   1 = +/-4.096V
#  -   2 = +/-2.048V
#  -   4 = +/-1.024V
#  -   8 = +/-0.512V
#  -  16 = +/-0.256V
# See table 3 in the ADS1015/ADS1115 datasheet for more info on gain.
GAIN = 1

print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Make and print nice channel column headers.
column_headers = ['Red Knob', 'Red X', 'Red Y', 'Red X Motor', 'Red Y Motor', \
                  'Green Knob', 'Green X', 'Green Y', 'Green X Motor', 'Green Y Motor', \
                  'Blue Knob', 'Blue X', 'Blue Y', 'Blue X Motor', 'Blue Y Motor']

print('| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} | {10} | {11} | {12} | {13} | {14} |'.format(*column_headers))
print('-' * 37)
# Main loop.
while True:
    ##############################
    #############RED##############
    ##############################
    
    # Read all the red ADC channel values in a list.
    values = [0]*15
    for i in range(15):
        # Read the specified ADC channels using the previously set gain value.
        ##RED
        if i < 3:
            values[i] = adc_red.read_adc(i, gain=GAIN)
        if i == 3:
            values[i] = joy_val_filter(scale_joystick_value(adc_red.read_adc(1, gain = GAIN))*increment)
        if i == 4:
            values[i] = joy_val_filter(scale_joystick_value(adc_red.read_adc(2, gain = GAIN))*increment)

        ##GREEN    
        if i > 4 and i < 8:
            values[i] = adc_green.read_adc(i - 5, gain=GAIN)
        if i == 8:
            values[i] = joy_val_filter(scale_joystick_value(adc_green.read_adc(1, gain = GAIN))*increment)
        if i == 9:
            values[i] = joy_val_filter(scale_joystick_value(adc_green.read_adc(2, gain = GAIN))*increment)
        ##BLUE
        if i > 9 and i < 13:
            values[i] = adc_blue.read_adc(i - 10, gain=GAIN)
        if i == 13:
            values[i] = joy_val_filter(scale_joystick_value(adc_blue.read_adc(1, gain = GAIN))*increment)
        if i == 14:
            values[i] = joy_val_filter(scale_joystick_value(adc_blue.read_adc(2, gain = GAIN))*increment) 
            
        
        # Note you can also pass in an optional data_rate parameter that controls
        # the ADC conversion time (in samples/second). Each chip has a different
        # set of allowed data rate values, see datasheet Table 9 config register
        # DR bit values.
        #values[i] = adc.read_adc(i, gain=GAIN, data_rate=128)
        # Each value will be a 12 or 16 bit signed integer value depending on the
        # ADC (ADS1015 = 12-bit, ADS1115 = 16-bit).
    # Print the ADC values.
    print('| {0} | {1} | {2} | {3} | {4} | {5} | {6} | {7} | {8} | {9} | {10} | {11} | {12} | {13} | {14} |'.format(*values))
    # Pause for half a second.
##    time.sleep(0.1)

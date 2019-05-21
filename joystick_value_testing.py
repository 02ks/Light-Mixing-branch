import time
import Adafruit_ADS1x15
adc = Adafruit_ADS1x15.ADS1115()

GAIN = 1

############################
######  Find joy_val  ######
############################



column_names = ["adc_val", "joy_val"]
print('Reading ADS1x15 values, press Ctrl-C to quit...')
# Print nice channel column headers.
print('| {0:>6} | {1:>6} |'.format(*column_names))
print('-' * 37)
# Main loop.
while True:
    values = [0]*4
    for i in range(4):
        values[i] = adc.read_adc(i, gain=GAIN)

    print('| {0:>6} | {1:>6} |'.format(*values))
    # Pause for half a second.
    time.sleep(0.5)

def test_joy_x1():
    pass

def test_joy_y1():
    pass

def test_joy_x2():
    pass

def test_joy_y2():
    pass

def test_joy_x3():
    pass

def test_joy_y3():
    pass

import sys
import Adafruit_ADS1x15
import os

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

from pidev.MixPanel import MixPanel
from pidev.kivy.PassCodeScreen import PassCodeScreen
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from pidev.kivy import ImageButton
from pidev.stepper import stepper
from time import sleep
from threading import Thread
from Slush.Devices import L6480Registers as LReg6480, L6470Registers as LReg6470

sys.path.insert(0, "/home/pi/packages/Adafruit_16_Channel_PWM_Module_Easy_Library")
import Adafruit_Ease_Lib as ael
led = ael.Adafruit_Ease_Lib()
led.change_frequency(2000)
pwms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 , 13, 14, 15]
led.change_percentage(pwms, 50)

AXIS_MOTOR_SETTINGS = {
    'hold_current': 20,
    'run_current': 20,
    'acc_current': 20,
    'dec_current': 20,
    'max_speed': 100,
    'min_speed': 0,
    'micro_steps': 1,
    'threshold_speed': 400,
    'over_current': 2000,
    'stall_current': 2031.25,
    'accel': 0xF00,
    'decel': 0xF00,
    'low_speed_opt': False,
    'homing_direction': 0
}
MIXPANEL_TOKEN = "x"
MIXPANEL = MixPanel("Project Name", MIXPANEL_TOKEN)

SCREEN_MANAGER = ScreenManager()
MAIN_SCREEN_NAME = 'main'
ADMIN_SCREEN_NAME = 'admin'
class ProjectNameGUI(App):
    """
    Class to handle running the GUI Application
    """

    def build(self):
        """
        Build the application
        :return: Kivy Screen Manager instance
        """
        return SCREEN_MANAGER
Window.clearcolor = (1, .6, .3, 1)  # White


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """

    def pressed(self):
        """
        Function called on button touch event for button with id: testButton
        :return: None
        """
        PauseScreen.pause(pause_scene_name='pauseScene', transition_back_scene='main', text="Test", pause_duration=5)

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'

# motor_1 = stepper(port=1, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_2 = stepper(port=2, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_3 = stepper(port=3, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_4 = stepper(port=4, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_5 = stepper(port=5, speed=AXIS_MOTOR_SETTINGS['max_speed'])
# motor_6 = stepper(port=6, speed=AXIS_MOTOR_SETTINGS['max_speed'])
#
# motors = [motor_1, motor_2, motor_3, motor_4, motor_5, motor_6]
# for motor in motors:
#     motor.setCurrent(hold=AXIS_MOTOR_SETTINGS['hold_current'], run=AXIS_MOTOR_SETTINGS['run_current'],
#                      acc=AXIS_MOTOR_SETTINGS['acc_current'], dec=AXIS_MOTOR_SETTINGS['dec_current'])
#     motor.setMaxSpeed(AXIS_MOTOR_SETTINGS['max_speed'])
#     motor.setMinSpeed(AXIS_MOTOR_SETTINGS['min_speed'])
#     motor.setMicroSteps(AXIS_MOTOR_SETTINGS['micro_steps'])
#     motor.setThresholdSpeed(AXIS_MOTOR_SETTINGS['threshold_speed'])
#     motor.setOverCurrent(AXIS_MOTOR_SETTINGS['over_current'])
#     motor.setStallCurrent(AXIS_MOTOR_SETTINGS['stall_current'])
#     motor.setAccel(AXIS_MOTOR_SETTINGS['accel'])
#     motor.setDecel(AXIS_MOTOR_SETTINGS['decel'])
#     motor.setLowSpeedOpt(AXIS_MOTOR_SETTINGS['low_speed_opt'])
#     motor.setParam(LReg.CONFIG, 0x3688)
#     motor.home(0)
#     while motor.isBusy():
#         continue


current = 30


motor_1 = stepper(port=1, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)

motor_2 = stepper(port=2, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)

motor_3 = stepper(port=3, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)

motor_4 = stepper(port=4, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)

motor_5 = stepper(port=5, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)

motor_6 = stepper(port=6, speed=100, hold_current=current, run_current=current, accel_current=current,
                  deaccel_current=current)
motors = [motor_1, motor_2, motor_3, motor_4, motor_5, motor_6]
microstepping = 32
for motor in motors:
    motor.setAccel(0xF00)
    motor.setDecel(0xF00)
    motor.set_micro_steps(microstepping)

motor_1.home(0)
motor_2.home(0)
motor_4.home(1)
motor_5.home(1)
motor_6.home(1)
sleep(.5)
motor_3.home(0)

motor_1.go_to(199 * microstepping)
motor_2.go_to(199 * microstepping)
motor_3.go_to(150 * microstepping)
motor_4.go_to(-76 * microstepping)
motor_5.go_to(-76 * microstepping)
motor_6.go_to(-76 * microstepping)
motor_1.set_speed(15)
motor_2.set_speed(15)
motor_3.set_speed(15)
motor_4.set_speed(15)
motor_5.set_speed(15)
motor_6.set_speed(15)
GAIN = 1
increment = 1
# Create an ADS1115 ADC (16-bit) instance.
adc_red = Adafruit_ADS1x15.ADS1115(0x4A)
adc_blue = Adafruit_ADS1x15.ADS1115(0x48)
adc_green = Adafruit_ADS1x15.ADS1115(0x49)
global gamer
gamer = True
clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)


class AdminScreen(Screen):
    """
    Class to handle the AdminScreen and its functionality
    """

    def __init__(self, **kwargs):
        """
        Load the AdminScreen.kv file. Set the necessary names of the screens for the PassCodeScreen to transition to.
        Lastly super Screen's __init__
        :param kwargs: Normal kivy.uix.screenmanager.Screen attributes
        """
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)  # Specify screen name to transition to after correct password
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)  # set screen name to transition to if "Back to Game is pressed"

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        """
        Shutdown the system. This should free all steppers and do any cleanup necessary
        :return: None
        """
        global gamer
        gamer = False
        motor_1.softFree()
        sleep(.05)
        motor_2.softFree()
        sleep(.05)
        motor_3.softFree()
        sleep(.05)
        motor_4.softFree()
        sleep(.05)
        motor_5.softFree()
        sleep(.05)
        motor_6.softFree()
        sleep(.05)
        led.change_percentage(0, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.05)
        led.change_percentage(1, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.05)
        led.change_percentage(2, clamp(value_as_percent("red", 0), 0, 100))
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        global gamer
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        gamer = False
        motor_1.softFree()
        sleep(.05)
        motor_2.softFree()
        sleep(.05)
        motor_3.softFree()
        sleep(.05)
        motor_4.softFree()
        sleep(.05)
        motor_5.softFree()
        sleep(.05)
        motor_6.softFree()
        sleep(.05)
        led.change_percentage(0, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.05)
        led.change_percentage(1, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.05)
        led.change_percentage(2, clamp(value_as_percent("red", 0), 0, 100))
        quit()
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

def scale_joystick_value(value):
    return (value - 6600)/6000

def joy_val_filter(value):
    if value < -0.9:
        return -1
    if value > 0.9:
        return 1
    if value > -0.1 and value < 0.1:
        return 0
    else:
        return value
motor_3.go_to(49 * microstepping)
sleep(3)

def threadman():
    while gamer ==True:
        led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain=GAIN)), 0, 100))
        led.change_percentage(1, clamp(value_as_percent("red", adc_green.read_adc(0, gain=GAIN)), 0, 100))
        led.change_percentage(2, clamp(value_as_percent("red", adc_blue.read_adc(0, gain=GAIN)), 0, 100))


        movement_amount = round(scale_joystick_value(adc_red.read_adc(1, gain=GAIN)) * increment)
        if (movement_amount == 0):
            motor_4.softStop()
        if movement_amount is not 0 and not motor_4.is_busy() or movement_amount is not 0 and motor_4.getPosition() >=7000 or motor_4.getPosition() <=-7000:
            #print(motor_4.getPosition())
            print(movement_amount)
            motor_4.softStop()
            if(motor_4.getPosition() >=7000 & movement_amount!=-1):
                print(motor_4.getPosition())
                motor_4.stop()
                print("yep")
            elif(motor_4.getPosition() <=-7000 & movement_amount<0):
                motor_4.stop()
                print("working")
            else:
                motor_4.start_relative_move(movement_amount*100)
            # print(motor_4.get_position())

        movement_amount = round(scale_joystick_value(adc_blue.read_adc(1, gain=GAIN)) * increment)
        if (movement_amount == 0):
            motor_5.softStop()
        if movement_amount is not 0 and not motor_5.is_busy() or movement_amount is not 0 and motor_5.getPosition() >=7000 or motor_5.getPosition() <=-7000:
            print(motor_5.getPosition())
            motor_5.softStop()
            if (motor_5.getPosition() >= 7000 & movement_amount != -1):
                print(motor_5.getPosition())
                motor_5.stop()
                print("yep")
            elif (motor_5.getPosition() <= -7000 & movement_amount < 0):
                motor_5.stop()
                print("working")
            else:
                motor_5.start_relative_move(movement_amount*100)

        movement_amount = round(scale_joystick_value(adc_green.read_adc(1, gain=GAIN)) * increment)
        if (movement_amount == 0):
            motor_6.softStop()
        if movement_amount is not 0 and not motor_6.is_busy() or movement_amount is not 0 and motor_6.getPosition() >=7000 or motor_6.getPosition() <=-7000:
            print(motor_6.getPosition())
            motor_6.softStop()
            if (motor_6.getPosition() >= 7000 & movement_amount != -1):
                print(motor_6.getPosition())
                motor_6.stop()
                print("yep")
            elif (motor_6.getPosition() <= -7000 & movement_amount < 0):
                motor_6.stop()
                print("working")
            else:
                motor_6.start_relative_move(movement_amount*100)

        movement_amount = round(scale_joystick_value(adc_red.read_adc(2, gain=GAIN)) * increment)
        if (movement_amount == 0):
            motor_1.softStop()
            print("stoppd")
        if movement_amount is not 0 and not motor_1.is_busy() or movement_amount is not 0 and motor_1.getPosition() >=14000 or motor_1.getPosition() <=-500:
            print(movement_amount)
            print(motor_1.getPosition())
            motor_1.softStop()
            if (motor_1.getPosition() >= 14000 & movement_amount > 0):
                print(motor_1.getPosition())
                print("yep")
                motor_1.softStop()
            elif (motor_1.getPosition() <= 2000 & movement_amount <= 1):
                print(motor_1.getPosition())
                print("working")
                motor_1.softStop()
            else:
                motor_1.start_relative_move(-movement_amount*100)
        movement_amount = round(scale_joystick_value(adc_green.read_adc(2, gain=GAIN)-6000) * increment)
        if (movement_amount == 0):
            motor_2.softStop()
        if movement_amount is not 0 and not motor_2.is_busy() or movement_amount is not 0 and motor_2.getPosition() >=14000 or motor_2.getPosition() <=-500:
            print(movement_amount)
            print(motor_2.getPosition())
            motor_2.softStop()
            if (motor_2.getPosition() >= 14000 & movement_amount > 0):
                print(motor_2.getPosition())
                print("yep")
                motor_2.softStop()
            elif (motor_2.getPosition() <= 2000 & movement_amount <= 1):
                print(motor_2.getPosition())
                print("working")
                motor_2.softStop()
            else:
                motor_2.start_relative_move(-movement_amount * 100)

        movement_amount = round(scale_joystick_value(adc_blue.read_adc(2, gain=GAIN)) * increment)
        if (movement_amount == 0):
            motor_3.softStop()
        if movement_amount is not 0 and not motor_3.is_busy() or movement_amount is not 0 and motor_3.getPosition() >=14000 or motor_3.getPosition() <=-500:
            print(movement_amount)
            print(motor_3.getPosition())
            if (motor_3.getPosition() >= 14000 & movement_amount > 0):
                print(motor_3.getPosition())
                motor_3.softStop()
                print("yep")
            elif (motor_3.getPosition() <= 2000 & movement_amount <= 1):
                print(motor_3.getPosition())
                print("working")
                motor_3.softStop()
            else:
                motor_3.start_relative_move(-movement_amount * 100)


        #print("red knob: " + str(adc_red.read_adc(0, gain = GAIN)) + "   red x: " + str(adc_red.read_adc(1, gain = GAIN)) + "  red y: " + str(adc_red.read_adc(2, gain = GAIN)),end = '        ')
        #print("blue knob: " + str(adc_blue.read_adc(0, gain = GAIN)) + "   blue x: " + str(adc_blue.read_adc(1, gain = GAIN)) + "  blue y: " + str(adc_blue.read_adc(2, gain = GAIN)),end = '      ')
        print("green knob: " + str(adc_green.read_adc(0, gain = GAIN)) + "   green x: " + str(adc_green.read_adc(1, gain = GAIN)) + "  green y: " + str(adc_green.read_adc(2, gain = GAIN)))
Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))

Thread(target=threadman).start()
Thread.daemon = True
print("happesns")
def send_event(event_name):
    """
    Send an event to MixPanel without properties
    :param event_name: Name of the event
    :return: None
    """
    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    # send_event("Project Initialized")
    # Window.fullscreen = 'auto'
    ProjectNameGUI().run()

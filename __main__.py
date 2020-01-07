import sys
import Adafruit_ADS1x15
import os

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import random
from pidev.MixPanel import MixPanel
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
pwms = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
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
CENTER_SCREEN_NAME = 'center'
PASSCODESCREEN_SCREEN_NAME = 'passCode'


class CustomImage(Image):
    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'


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


Window.clearcolor = (0, 0, 0, 1)


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

motor_1.set_speed(50)
motor_2.set_speed(50)
motor_3.set_speed(50)
motor_4.set_speed(50)
motor_5.set_speed(50)
motor_6.set_speed(50)
motor_1.home(0)
motor_2.home(0)
motor_4.home(1)
motor_5.home(1)
motor_6.home(1)
sleep(.5)
motor_3.home(0)
motor_1.go_to(199 * microstepping)
motor_2.go_to(199 * microstepping)
motor_4.go_to(-76 * microstepping)
motor_5.go_to(-76 * microstepping)
motor_6.go_to(-76 * microstepping)
motor_1.set_speed(13)
motor_2.set_speed(13)
motor_3.set_speed(13)
motor_4.set_speed(13)
motor_5.set_speed(13)
motor_6.set_speed(13)
motor_4.set_limit_hardstop(False)
motor_5.set_limit_hardstop(False)
motor_6.set_limit_hardstop(False)
motor_3.go_to(199 * microstepping)
sleep(3)
GAIN = 1
increment = 1

# Create an ADS1115 ADC (16-bit) instance.
adc_red = Adafruit_ADS1x15.ADS1115(0x4A)
adc_blue = Adafruit_ADS1x15.ADS1115(0x48)
adc_green = Adafruit_ADS1x15.ADS1115(0x49)

global gamer
global gamer2000
gamer = True
clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
global dsaf
global dsaf2
global dsaf3
global dsaf4
global dsaf5
global dsaf6
global dsaf7
global dsaf8
global dsaf9
dsaf = adc_red.read_adc(0, gain=GAIN)
dsaf2 = adc_blue.read_adc(0, gain=GAIN)
dsaf3 = adc_green.read_adc(0, gain=GAIN)
dsaf4 = adc_red.read_adc(1, gain=GAIN)
dsaf5 = adc_blue.read_adc(1, gain=GAIN)
dsaf6 = adc_green.read_adc(1, gain=GAIN)
dsaf7 = adc_red.read_adc(2, gain=GAIN)
dsaf8 = adc_blue.read_adc(2, gain=GAIN)
dsaf9 = adc_green.read_adc(2, gain=GAIN)

PASSWORD = '7266' # make different pw lead to different places?
USERPW = ''

passcode_screen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "PassCodeScreen.kv")

Builder.load_file(passcode_screen_path)

ADMIN_EVENTS_SCREEN = None
TRANSITION_BACK_SCREEN = 'main'

"""
Class to display a passcode on screen to advance to admin screen
"""


class PassCodeScreen(Screen):
    """
    Class used to enter the PassCodeScreen to enter the admin screen
    """

    def __init__(self, **kw):
        super(PassCodeScreen, self).__init__(**kw)

    def initialize(self):
        curr_app = App.get_running_app()
        print("wait")

    def add_num(self, num):
        """
        Add a number to the current password entry
        :param num: Number to add
        :return: None
        """
        global USERPW

        self.ids.pw.text += '* '
        USERPW += str(num)

    def remove_num(self):
        """
        Remove a number from the current password entry
        :return: None
        """
        global USERPW
        self.ids.pw.text = self.ids.pw.text[:len(self.ids.pw.text) - 2]
        USERPW = USERPW[:len(USERPW) - 1]

    def check_pass(self):
        """
        Check to see if the password was entered correctly
        :return: None
        """
        global USERPW
        if PASSWORD == USERPW:
            self.ids.pw.text = ' '
            USERPW = ''

            if ADMIN_EVENTS_SCREEN is None:
                print("Specify the admin screen name by calling PassCodeScreen.set_admin_events_screen")
                return

            self.parent.current = ADMIN_EVENTS_SCREEN

    def transition_back(self):
        """
        Transition back to given transition back scren
        :return: None
        """
        self.ids.pw.text = ""
        self.parent.current = TRANSITION_BACK_SCREEN

    @staticmethod
    def set_admin_events_screen(screen):
        """
        Set the name of the screen to transition to when the password is correct
        :param screen: Name of the screen to transition to
        :return: None
        """
        global ADMIN_EVENTS_SCREEN
        ADMIN_EVENTS_SCREEN = screen

    @staticmethod
    def set_transition_back_screen(screen):
        """
        Set the screen to transition back to when the "Back to Game" button is pressed
        :param screen: Name of the screen to transition back to
        :return: None
        """
        global TRANSITION_BACK_SCREEN
        TRANSITION_BACK_SCREEN = screen

    @staticmethod
    def set_password(pswd):
        """
        Change the default password
        :param pswd: New password
        :return: None
        """
        global PASSWORD
        PASSWORD = pswd

    @staticmethod
    def change_main_screen_name(name):
        """
        Change the name of the screen to add the hidden button to go to the admin screen

        NOTE: This only needs to be run ONCE, once it is called with the new name you can remove the call from your code
        :param name: Name of the main screen of the UI
        :return: None
        """
        if name == '':
            return

        with open(passcode_screen_path) as file:
            data = file.readlines()

        # This needs to be updated every time there are line changes in the PassCodeScreen.kv
        # TODO implement a better way to dynamically change the main screen name
        data[134] = '<' + name + '>\n'

        with open(passcode_screen_path, 'w') as file:
            file.writelines(data)


class CenterScreen(Screen):
    global gamer3000
    global game
    global gamer
    global gamer2000

    def __init__(self, **kw):
        Builder.load_file('center.kv')
        super(CenterScreen, self).__init__(**kw)
    def goBack(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
    #def whatsThis(self):
     #   gamer3000 = False
      #  self.ids.LMF.text = "Center"
       # game = True
        #gamer = True
        #gamer2000 = True
        #self.init()
        #self.test()


class MainScreen(Screen):
    """
    Class to handle the main screen and its associated touch events
    """
    global game
    global gamer
    global idlem
    global loopRun
    loopRun = False
    idlem = False
    global gamer2000
    global gamer3000
    gamer3000 = True
    gamer2000 = True
    game = True
    bruhmst = ObjectProperty(None)
    bruhmst2 = ObjectProperty(None)
    bruhmst3 = ObjectProperty(None)
    aaa = ObjectProperty(None)
    def whatsThis(self):
        global gamer
        global game
        global gamer3000
        global gamer2000
        gamer = False
        global idlem
        SCREEN_MANAGER.current = CENTER_SCREEN_NAME
        if idlem == True:
            game = False
            self.init()
            game = True
            gamer = True
            self.test()
        elif(gamer2000 == True):
            gamer3000 = True
            self.ids.LMF.text = "Uncenter"
            gamer2000 = False
            Thread(target=self.justColor).start()
            Thread.daemon = True
            self.init()
            print(motor_1.getPosition())
            print(motor_2.getPosition())
            print(motor_3.getPosition())
            print(motor_4.getPosition())
            print(motor_5.getPosition())
            print(motor_6.getPosition())
           # motor_1.go_to_position(5564)
           # motor_2.go_to_position(5468)
           # motor_3.go_to_position(5759)
          #  motor_4.go_to_position(-902)
           # motor_5.go_to_position(-2534)
          #  motor_6.go_to_position(-4783)
            motor_1.goToDir(1, 5564)
            motor_2.goToDir(1, 5468)
            motor_3.goToDir(1, 5759)
            motor_4.go_to(-902)
            motor_5.goToDir(1, -2834)
            motor_6.goToDir(1, -4783)
            sleep(2)
        else:
            gamer3000 = False
            self.ids.LMF.text = "Center"
            game = True
            gamer =True
            gamer2000 = True
            self.init()
            self.test()
    def justColor(self):
        while gamer3000 == True:
            led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain=GAIN)), 0, 100))
            led.change_percentage(1, clamp(value_as_percent("red", adc_green.read_adc(0, gain=GAIN)), 0, 100))
            led.change_percentage(2, clamp(value_as_percent("red", adc_blue.read_adc(0, gain=GAIN)), 0, 100))
            sd = ((adc_red.read_adc(0, gain=GAIN)-3968 * 1.0)/(15200-3968)) * 256
            fd = ((adc_blue.read_adc(0, gain= GAIN)-160*1.0)/(11200-160))*256
            ff = ((adc_green.read_adc(0, gain= GAIN)-3760*1.0)/(14620-3760)) * 256
            if(int(sd) > 256):
                sd = 256
            if(int(fd) > 256):
                fd = 256
            if(int(ff) > 256):
                ff = 256
            self.ids.bruhmst.text = "Red Light: %s" % int(sd)
            self.ids.bruhmst2.text = "Blue Light: %s" % int(fd)
            self.ids.bruhmst3.text = "Green Light: %s" % int(ff)
            print(adc_red.read_adc(0, gain=GAIN))
            print(adc_blue.read_adc(0, gain= GAIN))
            print(adc_green.read_adc(0, gain= GAIN))
            print("break")
    def setWhite(self):
        print('yo')
        global gamer
        global game
        global idlem
        if idlem == True:
            game = False
            self.init()
            game = True
            gamer = True
            self.test()
            return
        global gamer3000
        if gamer3000 == True:
            gamer3000 = False
            self.ids.WHITE.text = "To Knob Control"
            led.change_percentage(0, 10928)
            led.change_percentage(2, 8480)
            led.change_percentage(1, 14496)
        elif gamer == True:
            self.ids.WHITE.text = "To White"
            gamer3000 = True
        else:
            self.ids.WHITE.text = "To White"
            gamer3000 = True
            Thread(target=self.justColor).start()
            Thread.daemon = True
    def threadman(self):
        global stored_movement_amount1
        global stored_movement_amount2
        global stored_movement_amount3
        global stored_movement_amount4
        global stored_movement_amount5
        global stored_movement_amount6
        global loopRun
        loopRun = False
        stored_movement_amount1 = 0
        stored_movement_amount2 = 0
        stored_movement_amount3 = 0
        stored_movement_amount4 = 0
        stored_movement_amount5 = 0
        stored_movement_amount6 = 0
        global dsaf
        global dsaf2
        global dsaf3
        global dsaf4
        global dsaf5
        global dsaf6
        global dsaf7
        global dsaf8
        global dsaf9
        global bruhm
        bruhm = 0
        while gamer == True:
            loopRun = True
            if gamer3000 == True:
                bruhm = bruhm + 1
                print(bruhm)
                if (dsaf - adc_red.read_adc(0, gain=GAIN) >= 1000 or dsaf - adc_red.read_adc(0, gain=GAIN) <= -1000):
                    bruhm = 0

                elif (dsaf2 - adc_blue.read_adc(0, gain=GAIN) >= 1000 or dsaf2 - adc_blue.read_adc(0, gain=GAIN) <= -1000):
                    bruhm = 0

                elif (dsaf3 - adc_green.read_adc(0, gain=GAIN) >= 1000 or dsaf3 - adc_green.read_adc(0, gain=GAIN) <= -1000):
                    bruhm = 0
                dsaf = adc_red.read_adc(0, gain=GAIN)
                dsaf2 = adc_blue.read_adc(0, gain=GAIN)
                dsaf3 = adc_green.read_adc(0, gain=GAIN)
                led.change_percentage(0, clamp(value_as_percent("red", adc_red.read_adc(0, gain=GAIN)), 0, 100))
                led.change_percentage(1, clamp(value_as_percent("red", adc_green.read_adc(0, gain=GAIN)), 0, 100))
                led.change_percentage(2, clamp(value_as_percent("red", adc_blue.read_adc(0, gain=GAIN)), 0, 100))
                sd = ((adc_red.read_adc(0, gain=GAIN)-3968 * 1.0)/(15200-3968)) * 256
                fd = ((adc_blue.read_adc(0, gain= GAIN)-160*1.0)/(11200-160))*256
                ff = ((adc_green.read_adc(0, gain= GAIN)-3760*1.0)/(14620-3760)) * 256
                if(int(sd) > 256):
                    sd = 256
                if(int(fd) > 256):
                    fd = 256
                if(int(ff) > 256):
                    ff = 256
                self.ids.bruhmst.text = "Red Light: %s" % int(sd)
                self.ids.bruhmst2.text = "Blue Light: %s" % int(fd)
                self.ids.bruhmst3.text = "Green Light: %s" % int(ff)

            movement_amount = round(scale_joystick_value(adc_red.read_adc(1, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount4) - abs(movement_amount)) > 1:
                stored_movement_amount4 = movement_amount
                motor_4.stop()
            if movement_amount is not 0 and not motor_4.is_busy() or movement_amount is not 0 and motor_4.getPosition() >= 1000 or motor_4.getPosition() <= -7000:
                print(movement_amount)
                motor_4.set_speed(abs(movement_amount*2))
                bruhm = 0
                if motor_4.getPosition() >= 1000 and movement_amount > 0:
                    print(motor_4.getPosition())
                    motor_4.stop()
                    print("yep")
                elif motor_4.getPosition() <= -7000 & movement_amount < 0:
                    motor_4.stop()
                    print("working")
                else:
                    motor_4.start_relative_move(movement_amount * 100)

            movement_amount = round(scale_joystick_value(adc_blue.read_adc(1, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount5) - abs(movement_amount)) > 1:
                stored_movement_amount5 = movement_amount
                motor_5.stop()
            if movement_amount is not 0 and not motor_5.is_busy() or movement_amount is not 0 and motor_5.getPosition() >= 1000 or motor_5.getPosition() <= -7000:
                print(motor_5.getPosition())
                motor_5.set_speed(abs(movement_amount * 2))
                bruhm = 0
                if motor_5.getPosition() >= 1000 and movement_amount > 0:
                    print(motor_5.getPosition())
                    motor_5.stop()
                    print("yep")
                elif motor_5.getPosition() <= -7000 & movement_amount < 0:
                    motor_5.stop()
                    print("working")
                else:
                    motor_5.start_relative_move(movement_amount * 100)

            movement_amount = round(scale_joystick_value(adc_green.read_adc(1, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount6) - abs(movement_amount)) > 1:
                stored_movement_amount6 = movement_amount
                motor_6.stop()
            if movement_amount is not 0 and not motor_6.is_busy() or movement_amount is not 0 and motor_6.getPosition() >= 1000 or motor_6.getPosition() <= -7000:
                print(motor_6.getPosition())
                motor_6.set_speed(abs(movement_amount * 2))
                bruhm = 0
                if motor_6.getPosition() >= 1000 and movement_amount > 0:
                    print("This is yep movement_amount value: %d" % movement_amount)
                    print(motor_6.getPosition())
                    motor_6.stop()
                    print("yep")
                elif motor_6.getPosition() <= -7000 & movement_amount < 0:
                    motor_6.stop()
                    print("working")
                else:
                    motor_6.start_relative_move(movement_amount * 100)

            movement_amount = round(scale_joystick_value(adc_red.read_adc(2, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount1) - abs(movement_amount)) > 1:
                stored_movement_amount1 = movement_amount
                motor_1.stop()
                print("stoppd")
            if movement_amount is not 0 and not motor_1.is_busy() or movement_amount is not 0 and motor_1.getPosition() >= 14000 or motor_1.getPosition() <= -500:
                print(movement_amount)
                motor_1.set_speed(abs(movement_amount * 2))
                bruhm = 0
                print(motor_1.getPosition())
                if motor_1.getPosition() >= 14000 & movement_amount > 0:
                    print(motor_1.getPosition())
                    print("yep")
                    motor_1.softStop()
                elif motor_1.getPosition() <= 2000 & movement_amount <= 1:
                    print(motor_1.getPosition())
                    print("working")
                    motor_1.softStop()
                else:
                    motor_1.start_relative_move(-movement_amount * 100)
            movement_amount = round(scale_joystick_value(adc_green.read_adc(2, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount2) - abs(movement_amount)) > 1:
                stored_movement_amount2 = movement_amount
                motor_2.stop()
            if movement_amount is not 0 and not motor_2.is_busy() or movement_amount is not 0 and motor_2.getPosition() >= 14000 or motor_2.getPosition() <= -500:
                print(movement_amount)
                motor_2.set_speed(abs(movement_amount * 2))
                bruhm = 0
                print(motor_2.getPosition())
                if motor_2.getPosition() >= 14000 & movement_amount > 0:
                    print(motor_2.getPosition())
                    print("yep")
                    motor_2.softStop()
                elif motor_2.getPosition() <= 2000 & movement_amount <= 1:
                    print(motor_2.getPosition())
                    print("working")
                    motor_2.softStop()
                else:
                    motor_2.start_relative_move(-movement_amount * 100)

            movement_amount = round(scale_joystick_value(adc_blue.read_adc(2, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount3) - abs(movement_amount)) > 1:
                stored_movement_amount3 = movement_amount
                motor_3.stop()
            if movement_amount is not 0 and not motor_3.is_busy() or movement_amount is not 0 and motor_3.getPosition() >= 14000 or motor_3.getPosition() <= -500:
                print(movement_amount)
                motor_3.set_speed(abs(movement_amount * 2))
                bruhm = 0
                print(motor_3.getPosition())
                if motor_3.getPosition() >= 14000 & movement_amount > 0:
                    print(motor_3.getPosition())
                    motor_3.softStop()
                    print("yep")
                elif motor_3.getPosition() <= 2000 & movement_amount <= 1:
                    print(motor_3.getPosition())
                    print("working")
                    motor_3.softStop()
                else:
                    motor_3.start_relative_move(-movement_amount * 100)
            if (bruhm == 200):
                bruhm = 0
                idle()
        loopRun = False

           # print("red knob: " + str(adc_red.read_adc(0, gain = GAIN)) + "   red x: " + str(adc_red.read_adc(1, gain = GAIN)) + "  red y: " + str(adc_red.read_adc(2, gain = GAIN)),end = '        ')
          #  print("blue knob: " + str(adc_blue.read_adc(0, gain = GAIN)) + "   blue x: " + str(adc_blue.read_adc(1, gain = GAIN)) + "  blue y: " + str(adc_blue.read_adc(2, gain = GAIN)),end = '      ')
         #   print("green knob: " + str(adc_green.read_adc(0, gain = GAIN)) + "   green x: " + str(adc_green.read_adc(1, gain = GAIN)) + "  green y: " + str(adc_green.read_adc(2, gain = GAIN)))
           # print(motor_1.getPosition())
           # print(motor_2.getPosition())
          #  print(motor_3.getPosition())
          #  print(motor_4.getPosition())
          #  print(motor_5.getPosition())
           # print(motor_6.getPosition())
    def test(self):
        global loopRun
        if(loopRun == False):
            Thread(target=self.threadman).start()
            Thread.daemon = True
    def idleTrue(self):
        global game
        global gamer
        global idlem
        if(idlem == True):
            game = False
            self.init()
            game = True
            gamer = True
            self.test()
        elif(game == False):
            game = True
            self.ids.asd.text = "Idle On"
        else:
            game = False
            self.ids.asd.text = "Idle Off"

    def init(self):
        motor_1.free()
        sleep(.05)
        motor_2.free()
        sleep(.05)
        motor_3.free()
        sleep(.05)
        motor_4.free()
        sleep(.05)
        motor_5.free()
        sleep(.05)
        motor_6.free()
        sleep(2)
        motor_1.set_speed(50)
        motor_2.set_speed(50)
        motor_3.set_speed(50)
        motor_4.set_speed(50)
        motor_5.set_speed(50)
        motor_6.set_speed(50)
        motor_1.home(0)
        motor_2.home(0)
        motor_4.home(1)
        motor_5.home(1)
        motor_6.home(1)
        sleep(.5)
        motor_3.home(0)
        motor_1.go_to(199 * microstepping)
        motor_2.go_to(199 * microstepping)
        motor_4.go_to(-76 * microstepping)
        motor_5.go_to(-76 * microstepping)
        motor_6.go_to(-76 * microstepping)
        motor_1.set_speed(13)
        motor_2.set_speed(13)
        motor_3.set_speed(13)
        motor_4.set_speed(13)
        motor_5.set_speed(13)
        motor_6.set_speed(13)
        motor_4.set_limit_hardstop(False)
        motor_5.set_limit_hardstop(False)
        motor_6.set_limit_hardstop(False)
        motor_3.go_to(199 * microstepping)
        sleep(4)

    def idleThread(self):
        global a
        global b
        global c
        global d
        global gamer
        global e
        global idlem
        idlem = True
        global game
        global f
        global dsaf
        global dsaf2
        global dsaf3
        global change
        global change2
        global change3
        global change4
        global change5
        global change6
        motor_1.set_speed(13)
        motor_2.set_speed(13)
        motor_3.set_speed(13)
        motor_4.set_speed(13)
        motor_5.set_speed(13)
        motor_6.set_speed(13)
        change = random.random() * 999
        change2 = random.random() * 999
        change3 = random.random() * 999
        change3 = random.random() * 999
        change4 = random.random() * 999
        change5 = random.random() * 999
        change6 = random.random() * 999
        a = 100
        b = 100
        c = 100
        d = 100
        e = 100
        f = 100

        while game == True:
            change = change + 1
            change2 = change2 + 1
            change3 = change3 + 1
            change4 = change4 + 1
            change5 = change5 + 1
            change6 = change6 + 1

            if not motor_1.is_busy() or change == 1000:
                if change == 1000:
                    motor_1.stop()
                    a = a * -1
                    motor_1.start_relative_move(a)
                    change = random.random() * 999
                else:
                    motor_1.start_relative_move(a)
            if motor_1.getPosition() >= 9000 and a == 100 or motor_1.getPosition() <= 3000 and a == -100:
                motor_1.stop()
                a = a * -1
                motor_1.start_relative_move(a)

                print("stoppeders")
            if not motor_2.is_busy() or change2 ==1000:
                if change2 == 1000:
                    motor_2.stop()
                    b = b * -1
                    motor_2.start_relative_move(b)
                    change2 = random.random() * 999
                else:
                    motor_2.start_relative_move(b)
            if motor_2.getPosition() >= 9000 and b == 100 or motor_2.getPosition() <= 3000 and b == -100:
                motor_2.stop()
                b = b* -1
                print("stoppeders")
                motor_1.start_relative_move(b)
            if not motor_3.is_busy() or change3 == 1000:
                if change3 == 1000:
                    motor_3.stop()
                    c = c * -1
                    motor_3.start_relative_move(c)
                    change3 = random.random() * 999
                else:
                    motor_3.start_relative_move(c)
            if motor_3.getPosition() >= 9000 and c == 100 or motor_3.getPosition() <= 3000 and c == -100:
                motor_3.stop()
                c = c * -1
                print("stoppeders")
                motor_3.start_relative_move(c)
            if not motor_4.is_busy() or change4 == 1000:
                if change4 == 1000:
                    motor_4.stop()
                    d = d * -1
                    motor_4.start_relative_move(d)
                    change4 = random.random() * 999
                else:
                    motor_4.start_relative_move(d)
            if motor_4.getPosition() >= 1000 and d == 100 or motor_4.getPosition() <= -7000 and d == -100:
                motor_4.stop()
                d = d *-1
                print("stoppeders")
                motor_4.start_relative_move(d)

            if not motor_5.is_busy() or change5 ==1000:
                if change5 == 1000:
                    motor_5.stop()
                    e = e * -1
                    motor_5.start_relative_move(e)
                    change5 = random.random() * 999
                else:
                    motor_5.start_relative_move(e)
            if motor_5.getPosition() >= 1000 and e == 100 or motor_5.getPosition() <= -7000 and e == -100:
                motor_5.stop()
                e = e * -1
                print("stoppeders")
                motor_5.start_relative_move(e)
            if not motor_6.is_busy() or change6 == 1000:
                if change6 == 1000:
                    motor_6.stop()
                    f = f * -1
                    motor_6.start_relative_move(f)
                    change6 = random.random() * 999
                else:
                    motor_6.start_relative_move(f)
            if motor_6.getPosition() >= 1000 and f == 100 or motor_6.getPosition() <= -7000 and f == -100:
                motor_6.stop()
                f = f * -1
                print("stoppeders")
                motor_6.start_relative_move(f)
            if(dsaf - adc_red.read_adc(0, gain=GAIN) >= 1000 or dsaf - adc_red.read_adc(0, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False

               # Thread(target=threadman, daemon=True).start()
            elif (dsaf2 - adc_blue.read_adc(0, gain=GAIN) >= 1000 or dsaf2 - adc_blue.read_adc(0, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
               # Thread(target=threadman, daemon=True).start()
            elif (dsaf3 - adc_green.read_adc(0, gain=GAIN) >= 1000 or dsaf3 - adc_green.read_adc(0, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
               # Thread(target=threadman, daemon=True).start()
            elif (dsaf4 - adc_red.read_adc(1, gain=GAIN) >= 1000 or dsaf4 - adc_red.read_adc(1, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False

               # Thread(target=threadman, daemon=True).start()
            elif (dsaf5 - adc_blue.read_adc(1, gain=GAIN) >= 1000 or dsaf5 - adc_blue.read_adc(1, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
               # Thread(target=threadman, daemon=True).start()
            elif (dsaf6 - adc_green.read_adc(1, gain=GAIN) >= 1000 or dsaf6 - adc_green.read_adc(1, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
               # Thread(target=threadman, daemon=True).start()
            elif (dsaf7 - adc_red.read_adc(2, gain=GAIN) >= 1000 or dsaf7 - adc_red.read_adc(2, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False

               # Thread(target=threadman, daemon=True).start()
            elif (dsaf8 - adc_blue.read_adc(2, gain=GAIN) >= 1000 or dsaf8 - adc_blue.read_adc(2, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
                #Thread(target=threadman, daemon=True).start()
            elif (dsaf9 - adc_green.read_adc(2, gain=GAIN) >= 1000 or dsaf9 - adc_green.read_adc(2, gain=GAIN) <= -1000):
                self.init(self)
                gamer = True
                game = False
               # Thread(target=threadman, daemon=True).start()
        idlem = False

    def admin_action(self):
        """
        Hidden admin button touch event. Transitions to passCodeScreen.
        This method is called from pidev/kivy/PassCodeScreen.kv
        :return: None
        """
        SCREEN_MANAGER.current = 'passCode'


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
        global game
        gamer = False
        global gamer2000
        gamer2000 = True
        game = False
        motor_1.free()
        sleep(.3)
        motor_2.free()
        sleep(.3)
        motor_3.free()
        sleep(.3)
        motor_4.free()
        sleep(.3)
        motor_5.free()
        sleep(.3)
        motor_6.free()
        sleep(.3)
        led.change_percentage(0, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
        led.change_percentage(1, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
        led.change_percentage(2, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
        os.system("sudo shutdown now")

    @staticmethod
    def exit_program():
        global gamer
        global gamer2000
        global game
        game = False
        """
        Quit the program. This should free all steppers and do any cleanup necessary
        :return: None
        """
        gamer = False
        gamer2000 = True
        motor_1.free()
        sleep(.3)
        motor_2.free()
        sleep(.3)
        motor_3.free()
        sleep(.3)
        motor_4.free()
        sleep(.3)
        motor_5.free()
        sleep(.3)
        motor_6.free()
        sleep(.3)
        led.change_percentage(0, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
        led.change_percentage(1, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
        led.change_percentage(2, clamp(value_as_percent("red", 0), 0, 100))
        sleep(.3)
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
    abf = (value-6600)/2000
    #print("movement_amount: %d" % abf)
    return (value - 6600)/1000


def joy_val_filter(value):
    if value < -0.9:
        return -1
    if value > 0.9:
        return 1
    if value > -0.1 and value < 0.1:
        return 0
    else:
        return value
def idle():
    global game
    global gamer
    if(game == True):
        game = True
        gamer = False
        self = MainScreen
        Thread(target=MainScreen.idleThread(self), daemon=True).start()


Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(CenterScreen(name=CENTER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
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
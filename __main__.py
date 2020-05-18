import sys
import Adafruit_ADS1x15
import os
import random

from kivy.uix.colorpicker import ColorPicker
from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from pidev.MixPanel import MixPanel
from pidev.kivy.PauseScreen import PauseScreen
from pidev.kivy import DPEAButton
from kivy.uix.button import Button
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
# Variables are the solution to all problems, hence why I made and named almost all the variables. I take credit for
# work such as centeringVariable or colorControl, or idleToggle, or the knobStore line or brust line.
# Please and thank you. (by Alex)
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
COMMUNE_TIME_SCREEN = 'commune'
FAKE_SCREEN_NAME = 'fake'
PASSCODESCREEN_SCREEN_NAME = 'passCode'
COLOR_SCREEN_NAME = 'color'


class CustomImage(Image):
    def __init__(self, *args, **kwargs):
        Image.__init__(self, *args, **kwargs)
        self.bind(texture=self._update_texture_filters)

    def _update_texture_filters(self, image, texture):
        texture.mag_filter = 'nearest'


class ProjectNameGUI(App):
    def build(self):
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

global mainThreadToggle
global idleToggle
idleToggle = True
global centeringVariable
mainThreadToggle = True
clamp = lambda n, min_n, max_n: max(min(max_n, n), min_n)
global knobStore
global knobStore2
global knobStore3
global joyStore
global joyStore2
global joyStore3
global joyStore4
global joyStore8
global joyStore9
knobStore = adc_red.read_adc(0, gain=GAIN)
knobStore2 = adc_blue.read_adc(0, gain=GAIN)
knobStore3 = adc_green.read_adc(0, gain=GAIN)
joyStore = adc_red.read_adc(1, gain=GAIN)
joyStore2 = adc_blue.read_adc(1, gain=GAIN)
joyStore3 = adc_green.read_adc(1, gain=GAIN)
joyStore4 = adc_red.read_adc(2, gain=GAIN)
joyStore8 = adc_blue.read_adc(2, gain=GAIN)
joyStore9 = adc_green.read_adc(2, gain=GAIN)
global betweenThreadToggle
betweenThreadToggle = False
PASSWORD = '7266'
PASSWORD2 = '1922'
PASSWORD3 = '12345'
USERPW = ''

passcode_screen_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "", "PassCodeScreen.kv")

Builder.load_file(passcode_screen_path)

ADMIN_EVENTS_SCREEN = None
TRANSITION_BACK_SCREEN = 'main'


class PassCodeScreen(Screen):
    def __init__(self, **kw):
        super(PassCodeScreen, self).__init__(**kw)

    def initialize(self):
        curr_app = App.get_running_app()
        print("wait")

    def add_num(self, num):
        global USERPW

        self.ids.pw.text += '* '
        USERPW += str(num)

    def remove_num(self):
        global USERPW
        self.ids.pw.text = self.ids.pw.text[:len(self.ids.pw.text) - 2]
        USERPW = USERPW[:len(USERPW) - 1]

    def check_pass(self):
        global USERPW
        if PASSWORD3 == USERPW:
            self.ids.pw.text = ' '
            USERPW = ''

            if ADMIN_EVENTS_SCREEN is None:
                print("Specify the admin screen name by calling PassCodeScreen.set_admin_events_screen")
                return

            self.parent.current = FAKE_SCREEN_NAME
        if PASSWORD2 == USERPW:
            self.ids.pw.text = ' '
            USERPW = ''

            if ADMIN_EVENTS_SCREEN is None:
                print("Specify the admin screen name by calling PassCodeScreen.set_admin_events_screen")
                return

            self.parent.current = COMMUNE_TIME_SCREEN
        if PASSWORD == USERPW:
            self.ids.pw.text = ' '
            USERPW = ''

            if ADMIN_EVENTS_SCREEN is None:
                print("Specify the admin screen name by calling PassCodeScreen.set_admin_events_screen")
                return

            self.parent.current = ADMIN_EVENTS_SCREEN

    def transition_back(self):
        self.ids.pw.text = ""
        self.parent.current = TRANSITION_BACK_SCREEN

    @staticmethod
    def set_admin_events_screen(screen):
        global ADMIN_EVENTS_SCREEN
        ADMIN_EVENTS_SCREEN = screen

    @staticmethod
    def set_transition_back_screen(screen):
        global TRANSITION_BACK_SCREEN
        TRANSITION_BACK_SCREEN = screen

    @staticmethod
    def set_password(pswd):
        global PASSWORD
        PASSWORD = pswd

    @staticmethod
    def change_main_screen_name(name):
        if name == '':
            return

        with open(passcode_screen_path) as file:
            data = file.readlines()

        data[134] = '<' + name + '>\n'

        with open(passcode_screen_path, 'w') as file:
            file.writelines(data)


class CenterScreen(Screen):
    "Temporary screen that's entered while centering or uncentering to prevent issues where buttons can store up clicks "
    global colorControl
    global idleToggle
    global mainThreadToggle
    global centeringVariable

    def __init__(self, **kw):
        Builder.load_file('center.kv')
        super(CenterScreen, self).__init__(**kw)

    def goBack(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def LoadAnimation(self):
        "This currently doesn't function cause the screen is technically frozen at the time, however if the issue of freezing is solved"
        "this should work"
        while(SCREEN_MANAGER.current == MAIN_SCREEN_NAME):
            self.ids.owos.text = "Centering"
            sleep(.1)
            self.ids.owos.text = "Centering."
            sleep(.1)
            self.ids.owos.text = "Centering.."
            sleep(.1)
            self.ids.owos.text = "Centering..."
            sleep(.1)

    def oii(self):
        self.LoadAnimation()
        MainScreen.whatsThis(MainScreen)

    def transition_back(self):
        """
        Transition back to the main screen
        :return:
        """
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


class CommuneScreen(Screen):
    "Easter Egg Screen"
    def __init__(self, **kw):
        Builder.load_file('commune.kv')
        super(CommuneScreen, self).__init__(**kw)
    def goBack(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME


class FakeScreen(Screen):
    "Easter Egg Screen"
    def __init__(self, **kw):
        Builder.load_file('fake.kv')
        super(FakeScreen, self).__init__(**kw)

    def goBack(self):
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def bamBoozle(self):
        self.ids.bnr.text = " "
        sleep(10)
        self.ids.bnr.text = "Ha you thought, try something a little better then 12345 next time"


class ColorScreen(Screen):
    "Color Changing Screen"
    def __init__(self, **kw):
        Builder.load_file('color.kv')
        super(ColorScreen, self).__init__(**kw)

    def APLE(self):
        global colorControl
        colorControl = False

    def goBack(self):
        global betweenThreadToggle
        global colorControl
        colorControl= True
        print("activated")
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    def ColorLarge(self, red, blue, green, otherValue):
        print(self)
        print(otherValue)
        print(red)
        print("bruh")
        print(blue)
        print(green)
        led.change_percentage(0, red*200)
        led.change_percentage(2, green*200)
        led.change_percentage(1, blue*200)


class ColPckr(ColorPicker):
    pass


class MainScreen(Screen):
    global idleToggle
    global mainThreadToggle
    global idleTrueCheck
    global loopRun
    loopRun = False
    idleTrueCheck = False
    global centeringVariable
    global colorControl
    colorControl = True
    centeringVariable = True
    RBGtext = ObjectProperty(None)
    RBGtext2 = ObjectProperty(None)
    RBGtext3 = ObjectProperty(None)
    uselessLabel = ObjectProperty(None)

    def whatThis(self):
        "Toggles between centering and uncentering, take note of the importance of the variables changed"
        global colorControl
        global idleToggle
        if centeringVariable == True:
            colorControl = True
            Thread(target=self.justColor).start()
            Thread.daemon = True
            self.ids.LMF.text = "Uncenter"
        else:
            colorControl = True
            self.ids.LMF.text = "Center"
        SCREEN_MANAGER.current = CENTER_SCREEN_NAME

    def colorScreen(self):
        "Toggles between colorscreen and namescreen, also important variables."
        global idleToggle
        global mainThreadToggle
        if idleTrueCheck == True:
            idleToggle = False
            self.init()
            idleToggle = True
            mainThreadToggle = True
            self.test()
            return
        SCREEN_MANAGER.current = COLOR_SCREEN_NAME

    def whatsThis(self):
        ""
        global mainThreadToggle
        global idleToggle
        global colorControl
        global centeringVariable
        mainThreadToggle = False
        global idleTrueCheck
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME
        if idleTrueCheck == True:
            idleToggle = False
            self.init(self)
            idleToggle = True
            mainThreadToggle = True
            self.test(self)
        elif(centeringVariable == True):
            colorControl = True
            centeringVariable = False
            self.init(self)
            print(motor_1.getPosition())
            print(motor_2.getPosition())
            print(motor_3.getPosition())
            print(motor_4.getPosition())
            print(motor_5.getPosition())
            print(motor_6.getPosition())
            motor_1.goToDir(1, 5564)
            motor_2.goToDir(1, 5468)
            motor_3.goToDir(1, 5759)
            motor_4.go_to(-902)
            motor_5.goToDir(1, -2834)
            motor_6.goToDir(1, -4783)
            sleep(2)
        else:
            colorControl = False
            #idleToggle = True
            mainThreadToggle =True
            centeringVariable = True
            self.init(self)
            colorControl = True
            self.test(self)

    def justColor(self):
        "A variation of threadman which only uses color, used when the motors are centered and stopped from moving"
        global betweenThreadToggle
        while colorControl == True:
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
            self.ids.RBGtext.text = "Red Light: %s" % int(sd)
            self.ids.RBGtext2.text = "Blue Light: %s" % int(fd)
            self.ids.RBGtext3.text = "Green Light: %s" % int(ff)
            print(adc_red.read_adc(0, gain=GAIN))
            print(adc_blue.read_adc(0, gain= GAIN))
            print(adc_green.read_adc(0, gain= GAIN))
            print("break")
        betweenThreadToggle = True

    def setWhite(self):
        "A function to set colors to white instead of control them via the knobs, with some added if/elses to check"
        "the current state of the project"
        print('yo')
        global mainThreadToggle
        global idleToggle
        global idleTrueCheck
        if idleTrueCheck == True:
            idleToggle = False
            self.init()
            idleToggle = True
            mainThreadToggle = True
            self.test()
            return
        global colorControl
        if colorControl == True:
            colorControl = False
            self.ids.WHITE.text = "To Knob Control"
            led.change_percentage(0, 10928)
            led.change_percentage(2, 8480)
            led.change_percentage(1, 14496)
        elif mainThreadToggle == True:
            self.ids.WHITE.text = "To White"
            colorControl = True
        else:
            self.ids.WHITE.text = "To White"
            colorControl = True
            Thread(target=self.justColor).start()
            Thread.daemon = True

    def threadman(self):
        "Main Thread that runs everything, color and movement."
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
        global knobStore
        global knobStore2
        global knobStore3
        global joyStore
        global joyStore2
        global joyStore3
        global joyStore4
        global joyStore8
        global joyStore9
        global idleCounter
        idleCounter = 0
        while mainThreadToggle == True:
            loopRun = True
            if colorControl == True:
                idleCounter = idleCounter + 1
                print(idleCounter)
                if (knobStore - adc_red.read_adc(0, gain=GAIN) >= 1000 or knobStore - adc_red.read_adc(0, gain=GAIN) <= -1000):
                    idleCounter = 0

                elif (knobStore2 - adc_blue.read_adc(0, gain=GAIN) >= 1000 or knobStore2 - adc_blue.read_adc(0, gain=GAIN) <= -1000):
                    idleCounter = 0

                elif (knobStore3 - adc_green.read_adc(0, gain=GAIN) >= 1000 or knobStore3 - adc_green.read_adc(0, gain=GAIN) <= -1000):
                    idleCounter = 0
                knobStore = adc_red.read_adc(0, gain=GAIN)
                knobStore2 = adc_blue.read_adc(0, gain=GAIN)
                knobStore3 = adc_green.read_adc(0, gain=GAIN)
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
                self.ids.RBGtext.text = "Red Light: %s" % int(sd)
                self.ids.RBGtext2.text = "Blue Light: %s" % int(fd)
                self.ids.RBGtext3.text = "Green Light: %s" % int(ff)

            movement_amount = round(scale_joystick_value(adc_red.read_adc(1, gain=GAIN)) * increment)
            if movement_amount == 0 or abs(abs(stored_movement_amount4) - abs(movement_amount)) > 1:
                stored_movement_amount4 = movement_amount
                motor_4.stop()
            if movement_amount is not 0 and not motor_4.is_busy() or movement_amount is not 0 and motor_4.getPosition() >= 1000 or motor_4.getPosition() <= -7000:
                print(movement_amount)
                motor_4.set_speed(abs(movement_amount*2))
                idleCounter = 0
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
                idleCounter = 0
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
                idleCounter = 0
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
                idleCounter = 0
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
                idleCounter = 0
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
                idleCounter = 0
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
            if (idleCounter == 200):
                idleCounter = 0
                idle()
        loopRun = False

    def test(self):
        "Used to toggle between threads when going between centered and uncentered states"
        global loopRun
        global betweenThreadToggle
        if(betweenThreadToggle == True):
            betweenThreadToggle = False
            Thread(target=self.justColor).start()
            Thread.daemon = True
        if(loopRun == False):
            Thread(target=self.threadman).start()
            Thread.daemon = True

    def idleTrue(self):
        global idleToggle
        global mainThreadToggle
        global idleTrueCheck
        if(idleTrueCheck == True):
            idleToggle = False
            self.init()
            idleToggle = True
            mainThreadToggle = True
            self.test()
        elif(idleToggle == False):
            idleToggle = True
            self.ids.asd.text = "Idle On"
        else:
            idleToggle = False
            self.ids.asd.text = "Idle Off"

    def init(self):
        "The setup function, used to prevent things from breaking in various places"
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
        "The idle thread that controls what happens when iddling"
        global a
        global b
        global c
        global d
        global mainThreadToggle
        global e
        global idleTrueCheck
        idleTrueCheck = True
        global idleToggle
        global f
        global knobStore
        global knobStore2
        global knobStore3
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

        while idleToggle == True:
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
            if(knobStore - adc_red.read_adc(0, gain=GAIN) >= 1000 or knobStore - adc_red.read_adc(0, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (knobStore2 - adc_blue.read_adc(0, gain=GAIN) >= 1000 or knobStore2 - adc_blue.read_adc(0, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (knobStore3 - adc_green.read_adc(0, gain=GAIN) >= 1000 or knobStore3 - adc_green.read_adc(0, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore - adc_red.read_adc(1, gain=GAIN) >= 1000 or joyStore - adc_red.read_adc(1, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore2 - adc_blue.read_adc(1, gain=GAIN) >= 1000 or joyStore2 - adc_blue.read_adc(1, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore3 - adc_green.read_adc(1, gain=GAIN) >= 1000 or joyStore3 - adc_green.read_adc(1, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore4 - adc_red.read_adc(2, gain=GAIN) >= 1000 or joyStore4 - adc_red.read_adc(2, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore8 - adc_blue.read_adc(2, gain=GAIN) >= 1000 or joyStore8 - adc_blue.read_adc(2, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
            elif (joyStore9 - adc_green.read_adc(2, gain=GAIN) >= 1000 or joyStore9 - adc_green.read_adc(2, gain=GAIN) <= -1000):
                idleTrueCheck = False
                self.init(self)
                mainThreadToggle = True
                idleToggle = False
        idleTrueCheck = False

    def admin_action(self):
        SCREEN_MANAGER.current = 'passCode'


class AdminScreen(Screen):
    def __init__(self, **kwargs):
        Builder.load_file('AdminScreen.kv')

        PassCodeScreen.set_admin_events_screen(
            ADMIN_SCREEN_NAME)
        PassCodeScreen.set_transition_back_screen(
            MAIN_SCREEN_NAME)

        super(AdminScreen, self).__init__(**kwargs)

    @staticmethod
    def transition_back():
        SCREEN_MANAGER.current = MAIN_SCREEN_NAME

    @staticmethod
    def shutdown():
        global mainThreadToggle
        global idleToggle
        mainThreadToggle = False
        global centeringVariable
        global colorControl
        colorControl = False
        centeringVariable = True
        idleToggle = False
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
        global mainThreadToggle
        global centeringVariable
        global colorControl
        global idleToggle
        idleToggle = False
        colorControl = False
        mainThreadToggle = False
        centeringVariable = True
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
    "Runs the idle function when called. Must be outside of mainscreen"
    global idleToggle
    global mainThreadToggle
    if(idleToggle == True):
        idleToggle = True
        mainThreadToggle = False
        self = MainScreen
        Thread(target=MainScreen.idleThread(self), daemon=True).start()


Builder.load_file('main.kv')
SCREEN_MANAGER.add_widget(MainScreen(name=MAIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(CenterScreen(name=CENTER_SCREEN_NAME))
SCREEN_MANAGER.add_widget(CommuneScreen(name = COMMUNE_TIME_SCREEN))
SCREEN_MANAGER.add_widget(FakeScreen(name = FAKE_SCREEN_NAME))
SCREEN_MANAGER.add_widget(PassCodeScreen(name='passCode'))
SCREEN_MANAGER.add_widget(PauseScreen(name='pauseScene'))
SCREEN_MANAGER.add_widget(AdminScreen(name=ADMIN_SCREEN_NAME))
SCREEN_MANAGER.add_widget(ColorScreen(name = COLOR_SCREEN_NAME))
print("happens")


def send_event(event_name):

    global MIXPANEL

    MIXPANEL.set_event_name(event_name)
    MIXPANEL.send_event()


if __name__ == "__main__":
    ProjectNameGUI().run()

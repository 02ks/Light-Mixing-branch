from pidev.Cyprus_Commands import Cyprus_Commands_RPi as ccrpi

ccrpi.open_spi()

from pidev import stepper

##led = stepper(port = 1, speed = 50)

##for i in range(1, 255):
##    print("lup")
ccrpi.write_pwm(1, ccrpi.COMPARE_MODE, ccrpi.LESS_THAN)
ccrpi.write_pwm(1, ccrpi.PERIOD, .001)
ccrpi.write_pwm(1, ccrpi.COMPARE, .001)

ccrpi.write_pwm(2, ccrpi.COMPARE_MODE, ccrpi.LESS_THAN)
ccrpi.write_pwm(2, ccrpi.PERIOD, .001)
ccrpi.write_pwm(2, ccrpi.COMPARE, .001) 
##    ccrpi.set_servo_speed(1, -0.5)
    

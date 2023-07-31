from machine import Pin, PWM
from time import sleep
import time
import math

led = Pin("LED", Pin.IN)
pwm0 = PWM(Pin(0))
pwm0.freq(200)
fimfpwm0.duty_u16(0)


def set_motor_strength(strength):
    """Sets the motor to a certain strength.
       strength is between 0 and 1."""
    pwm0.duty_u16(int((2**15)*strength))

set_motor_strength(0)
sleep(1)

loop_duration = 0.001
t = 0
while True:
    strength = (math.sin(t*5)+1)/2
    print(strength)
    set_motor_strength(strength)
    sleep(loop_duration)
    t += loop_duration
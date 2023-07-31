from machine import Pin, PWM
from time import sleep
import time
import math

# Directions are multiples of Tau:
# 0 is forward, 0.25 is right.
motors = [
    {"pin": 0, "direction": 0.25},
    {"pin": 1, "direction": 0.75},
]

for motor in motors:
    motor["pin"] = PWM(Pin(motor["pin"], Pin.OUT))
    motor["pin"].freq(200)

def set_motor_strength(pin, strength):
    """Sets the motor to a certain strength.
       strength is between 0 and 1.
       Attention: Use set_only_motor_strength instead
       to ensure that only one motor is on at a time."""
    pin.duty_u16(int((2**16)*strength))

def set_only_motor_strength(pin, strength):
    """Disables all motors, then sets the motor to a certain strength."""
    print(f"Vibration at pin {pin}")
    disable_all_motors()
    set_motor_strength(pin, strength)

def disable_all_motors():
    for motor in motors:
        set_motor_strength(motor["pin"], 0)

disable_all_motors()
sleep(1)

loop_duration = 0.01
#t = 0
#while True:
#    strength = (math.sin(t*5)+1)/2
#    print(strength)
#    set_motor_strength(strength)
#    sleep(loop_duration)
#    t += loop_duration

def best_motor(direction):
    """Returns the index of the motor that is best for a given direction."""
    best_motor = motors[0]["pin"]
    best_distance = 1
    for i in range(len(motors)):
        motor_direction = motors[i]["direction"]
        distance = abs((motor_direction - direction + 0.5) % 1 - 0.5)
        if distance < best_distance:
            best_distance = distance
            best_motor = motors[i]["pin"]
    return best_motor

t = 0
while True:
    direction = t/2 # Also in multiples of Tau.
    best_motor_pin = best_motor(direction)
    set_only_motor_strength(best_motor_pin, 1)
    t += loop_duration
    sleep(loop_duration)
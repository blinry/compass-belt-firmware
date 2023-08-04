from machine import Pin, PWM

# Directions are multiples of Tau:
# 0 is forward, 0.25 is right.
motors = [
    {"pin": 7, "direction": 0/8},
    {"pin": 2, "direction": 2/8},
    {"pin": 3, "direction": 3/8},
    {"pin": 5, "direction": 4/8},
    {"pin": 0, "direction": 5/8},
    {"pin": 4, "direction": 6/8},
    {"pin": 6, "direction": 7/8},
]

for motor in motors:
    motor["pwm"] = PWM(Pin(motor["pin"], Pin.OUT))
    motor["pwm"].freq(200)

def set_motor_strength(motor, strength):
    """Sets the motor to a certain strength.
       strength is between 0 and 1.
       Attention: Use set_only_motor_strength instead
       to ensure that only one motor is on at a time."""
    motor["pwm"].duty_u16(int((2**16-1)*strength))

def set_only_motor_strength(motor, strength):
    """Disables all motors, then sets the motor to a certain strength."""
    print(f"Activating {motor['pin']}")
    disable_all_motors()
    set_motor_strength(motor, strength)

def disable_all_motors():
    for motor in motors:
        set_motor_strength(motor, 0)

disable_all_motors()

def find_best_motor(direction):
    """Returns the motor that is best for a given direction."""
    best_motor = motors[0]
    best_distance = 1
    for i in range(len(motors)):
        motor_direction = motors[i]["direction"]
        distance = abs((motor_direction - direction + 0.5) % 1 - 0.5)
        if distance < best_distance:
            best_distance = distance
            best_motor = motors[i]
    return best_motor

while True:
    command = input("Enter direction (0-1) or 'stop': ").strip()
    if command == "stop":
        disable_all_motors()
    else:
        try:
            direction = float(command)
        except ValueError:
            print("That wasn't a valid command.")
            continue
        print("Your direction is", direction)
        best_motor = find_best_motor(direction)
        set_only_motor_strength(best_motor, 1)

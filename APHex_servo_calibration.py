import pigpio
import time
from adafruit_servokit import ServoKit
s=ServoKit(channels=16, address=0x40)
pi=pigpio.pi()
current_positions = [90 for _ in range(18)]
def move_servo(servoPin, pos, speed, minpwm, maxpwm):
    assert servoPin in range(18), "servoPin parameter must be between 0 and 17 inclusive"
    pos = 180 if pos > 180 else pos
    pos = 0 if pos < 0 else pos
    if servoPin == 16:
        for i in range(current_positions[16], pos+1 if current_positions[16] < pos else pos-1, 1 if current_positions[16] < pos else -1):
            pi.set_servo_pulsewidth(17, int((i/180*(maxpwm-minpwm))+minpwm))
            time.sleep(speed/1000)
    elif servoPin == 17:
        for i in range(current_positions[17], pos+1 if current_positions[17] < pos else pos-1, 1 if current_positions[17] < pos else -1):
            pi.set_servo_pulsewidth(18, int((i/180*(maxpwm-minpwm))+minpwm))
            time.sleep(speed/1000)
    else:
        for i in range(current_positions[servoPin], pos+1 if current_positions[servoPin] < pos else pos-1, 1 if current_positions[servoPin] < pos else -1):
            s.servo[servoPin].set_pulse_width_range(minpwm, maxpwm)
            s.servo[servoPin].angle=i
            time.sleep(speed/1000)

if __name__ == "__main__":
    values = [[500, 2550] for i in range(18)]
    servoPin = 28
    while True:
        servoPin = input("Please enter servo number or q to quit: ")
        if servoPin == "q":
            break
        else:
            servoPin = int(servoPin)
        if servoPin in [1, 4, 7, 10, 13, 16]:
            print()

            value = 2550
            move_servo(servoPin, 180, 40, 500, 2550)
            print("This is the 180 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 180, 40, 500, new_value)
                    value = new_value
            values[servoPin][1] = value
            value = 500
            move_servo(servoPin, 0, 40, 500, values[servoPin][1])
            print("This is the 0 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 0, 40, new_value, values[servoPin][1])
                    value = new_value
            values[servoPin][0] = value
            value = 0
            if servoPin in [1, 7, 13]:
                move_servo(servoPin, 0, 40, values[servoPin][0], values[servoPin][1])
            else:
                move_servo(servoPin, 180, 40, values[servoPin][0], values[servoPin][1])
        elif servoPin in [0, 6, 12]:
            print()
            servoPin = int(servoPin)
            value = 2550
            move_servo(servoPin, 180, 40, 500, 2550)
            print("This is the 180 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 180, 40, 500, new_value)
                    value = new_value
            values[servoPin][1] = value
            value = 1500
            move_servo(servoPin, 90, 40, 500, values[servoPin][1])
            print("This is the 90 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 90, 40, new_value * 2 - values[servoPin][1], values[servoPin][1])
                    value = new_value
            values[servoPin][0] = value * 2 - values[servoPin][1]
            value = 0
            move_servo(servoPin, 180, 40, values[servoPin][0], values[servoPin][1])
        elif servoPin in [3, 9, 15]:
            print()
            servoPin = int(servoPin)
            value = 500
            move_servo(servoPin, 0, 40, 500, 2550)
            print("This is the 0 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 180, 40, new_value, new_value)
                    value = new_value
            values[servoPin][0] = value
            value = 1500
            move_servo(servoPin, 90, 40, values[servoPin][0], 2550)
            print("This is the 90 degree position")
            while True:
                print(f"Current value: {value}")
                new_value = int(input("Please enter new value: "))
                if value == new_value:
                    break
                else:
                    move_servo(servoPin, 0, 40, new_value, values[servoPin][1])
                    value = new_value
            values[servoPin][1] = value * 2 - values[servoPin][0]
            value = 0
            move_servo(servoPin, 0, 40, values[servoPin][0], values[servoPin][1])
    print("\n")
    print("Final Calibration Values".center(42, '-'))
    print("------------------------------------------")
    for i in range(len(values)):
        print(f"|Servo: {str(i).zfill(2)} || minpwm: {values[i][0]} || maxpwm: {values[i][1]}|")
    print("------------------------------------------")





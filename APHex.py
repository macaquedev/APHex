import time
import os
import pigpio
from statistics import mean, median
from adafruit_servokit import ServoKit
from multiprocessing import Process
from math import atan2, acos, asin, cos, sin, tan
import hex_ik
import timeit
MG996R = 0
SG90 = 1

radian_constant = 0.017453292519943
pi = 3.14159265358979323846
pi_over_two = 1.570796326794897
os.system('sudo pigpiod > /dev/null 2>&1')

class APHex:
    def __init__(self, servoType=SG90, I2C_ADDR=0x40, sixteenPin=17, seventeenPin=18): # initialises APHex object. servoType is the type of servo your APHex uses, (can be a tuple to set minPWM and maxPWM yourself). I2C_ADDR has to be in hexadecimal. sixteenPin and seventeenPin are only required if you are not using the default pins for the 2 servos NOT on the PCA9685 board. These should be in BCM numbering, not BOARD numbering!
        self.__current_positions = [180, 0, 90, 0, 180, 90, 180, 0, 90, 0, 180, 90, 180, 0, 90, 0, 180, 90]
        self.__s=ServoKit(channels=16, address=I2C_ADDR)
        self.__pi=pigpio.pi()
        self.__initial_positions = self.__current_positions[:]
        self.__neutral_positions = [90 for i in range(18)]
        self.current_cartesian_positions = [[82.5, 142.89, 0], [82.5, 142.89, 0], [165, 0, 0], [165, 0, 0], [82.5, 142.89, 0], [82.5, 142.89, 0]]
        self.sixteen_pin = sixteenPin
        self.seventeen_pin = seventeenPin

        self._folded = True
        if servoType == 0:
            self.hip_length = 50
            self.leg_length = 115
            self.foot_length = 160
            self.body_side_length = 80
            self.__minpwm = [660, 425, 500, 610, 550, 500, 700, 535, 500, 530, 640, 500, 600, 630, 500, 610, 530, 500]
            self.__maxpwm = [2635, 2455, 2550, 2390, 2555, 2550, 2590, 2535, 2550, 2550, 2600, 2550, 2550, 2635, 2550, 2590, 2390, 2550]
            for i in range(0, 16):
                self.__s.servo[i].set_pulse_width_range(self.__minpwm[i], self.__maxpwm[i])
        
        for servoPin, position in enumerate(self.__current_positions):
            self.move_servo(servoPin, position, 100)
    def squat(times):
        self.shift_lean(0, 0, 60, 0, 0, 0)
        time.sleep(0.3)
        for i in range(times):
            self.shift_lean(0, 0, -30, 0, 0, 0)
            time.sleep(0.2)
            self.shift_lean(0, 0, 60, 0, 0, 0)
            time.sleep(0.2)
        time.sleep(0.1)
        self.shift_lean(0, 0, 0, 0, 0, 0)

    def wave(self, foot, times, width):
        femur = foot * 3 + 1
        tibia = foot * 3
        original_femur_pos = self.__current_positions[femur]
        p = self.move_servo(femur, self.__initial_positions[femur], 85)
        p.join()
        time.sleep(0.3)
        if foot % 2 == 0:
            p = self.move_servo(tibia, self.__current_positions[tibia] + width // 2, 100)
            p.join()
            time.sleep(0.2)
            for i in range(times):
                p = self.move_servo(tibia, self.__current_positions[tibia] - width, 100)
                p.join()
                time.sleep(0.2)
                p = self.move_servo(tibia, self.__current_positions[tibia] + width, 100)
                p.join()
                time.sleep(0.2)
            p = self.move_servo(tibia, self.__current_positions[tibia] - width // 2, 100)
            p.join()
            time.sleep(0.2)
        else:
            p = self.move_servo(tibia, self.__current_positions[tibia] - width // 2, 100)
            p.join()
            time.sleep(0.2)
            for i in range(times):
                p = self.move_servo(tibia, self.__current_positions[tibia] + width, 100)
                p.join()
                time.sleep(0.2)
                p = self.move_servo(tibia, self.__current_positions[tibia] - width, 100)
                p.join()
                time.sleep(0.2)
            p = self.move_servo(tibia, self.__current_positions[tibia] + width // 2, 100)
            p.join()
            time.sleep(0.2)
        p = self.move_servo(femur, original_femur_pos, 85)
        p.join()
        time.sleep(0.3)

    def __move_servo(self, servoPin, pos, speed):
        assert servoPin in range(18), "servoPin parameter must be between 0 and 17 inclusive"
        pos = 180 if pos > 180 else pos
        pos = 0 if pos < 0 else pos
        speed = 100 if speed > 100 else speed
        speed = (7.5 - speed / 15) ** 2
        pos = round(pos)
        if servoPin == 16:
            for i in range(self.__current_positions[16], pos+1 if self.__current_positions[16] < pos else pos-1, 1 if self.__current_positions[16] < pos else -1):
                self.__pi.set_servo_pulsewidth(self.sixteen_pin, int((i/180*(self.__maxpwm[16]-self.__minpwm[16]))+self.__minpwm[16]))
                time.sleep(speed/1000)
        elif servoPin == 17:
            for i in range(self.__current_positions[17], pos+1 if self.__current_positions[17] < pos else pos-1, 1 if self.__current_positions[17] < pos else -1):
                self.__pi.set_servo_pulsewidth(self.seventeen_pin, int((i/180*(self.__maxpwm[17]-self.__minpwm[17]))+self.__minpwm[17]))
                time.sleep(speed/1000)
        else:
            for i in range(self.__current_positions[servoPin], pos+1 if self.__current_positions[servoPin] < pos else pos-1, 1 if self.__current_positions[servoPin] < pos else -1):
                self.__s.servo[servoPin].angle=i
                time.sleep(speed/1000)

    def move_servo(self, servoPin, pos, speed):
        p = Process(target=self.__move_servo, args=[servoPin, pos, speed])
        p.start()
        self.__current_positions[servoPin] = pos
        return p

    def shift_lean(self, posX, posY, posZ, rotX, rotY, rotZ, speed=100):
        coordinates = hex_ik.shift_lean(posX, posY, posZ, rotX, rotY, rotZ, self.body_side_length, self.foot_length, self.leg_length, self.hip_length)
        processes = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]]
        for (leg, coords), i in zip(enumerate(coordinates), range(6)):
            processes[i] = self.cartesian_to_servo(leg, coords[0], coords[1], coords[2], speed)
        for i in range(len(processes)):
            for j in range(len(processes[i])):
                processes[i][j].join()

    def __move_servo_delay_time(self, servoPin, pos, speed):
        assert servoPin in range(18), "servoPin parameter must be between 0 and 17 inclusive"
        pos = 180 if pos > 180 else pos
        pos = 0 if pos < 0 else pos
        if servoPin == 16:
            for i in range(self.__current_positions[16], pos+1 if self.__current_positions[16] < pos else pos-1, 1 if self.__current_positions[16] < pos else -1):
                self.__pi.set_servo_pulsewidth(self.sixteen_pin, int((i/180*(self.__maxpwm[16]-self.__minpwm[16]))+self.__minpwm[16]))
                time.sleep(speed/1000)
        elif servoPin == 17:
            for i in range(self.__current_positions[17], pos+1 if self.__current_positions[17] < pos else pos-1, 1 if self.__current_positions[17] < pos else -1):
                self.__pi.set_servo_pulsewidth(self.seventeen_pin, int((i/180*(self.__maxpwm[17]-self.__minpwm[17]))+self.__minpwm[17]))
                time.sleep(speed/1000)
        else:
            for i in range(self.__current_positions[servoPin], pos+1 if self.__current_positions[servoPin] < pos else pos-1, 1 if self.__current_positions[servoPin] < pos else -1):
                self.__s.servo[servoPin].angle=i
                time.sleep(speed/1000)

    def move_servo_delay_time(self, servoPin, pos, speed):
        p = Process(target=self.__move_servo_delay_time, args=[servoPin, pos, speed])
        p.start()
        self.__current_positions[servoPin] = pos
        return p

    def folded(self):
        return self._folded
    def fold(self, speed=15):
        processes = [0, 0, 0, 0, 0, 0]
        self.shift_lean(0, 0, -(self.foot_length-60), 0, 0, 0, speed)
        for i, j in zip(range(1, 18, 3), range(0, 6)):
            processes[j] = self.move_servo(i, self.__initial_positions[i], speed)
        self._folded = True
        for i in processes:
            i.join()
        for i, j in zip(range(0, 17, 3), range(0, 6)):
            processes[j] = self.move_servo(i, self.__initial_positions[i], speed)
        for i in processes:
            i.join()
    def unfold(self, speed=15):
        processes = [0, 0, 0, 0, 0, 0]
        for i, j in zip(range(0, 17, 3), range(0, 6)):
            processes[j] = self.move_servo(i, self.__neutral_positions[i], speed)
        self._folded = False
        for i in processes:
            i.join()
        self.shift_lean(0, 0, -(self.foot_length-60), 0, 0, 0, speed)
        self.shift_lean(0, 0, 0, 0, 0, 0, speed)
    def tripod_gait_swift_mode(self, number_of_steps, direction=0, speed=50, step_size=60, leg_pickup_height=60):
        assert step_size > 0
        assert direction in range(0, 360), 'Bearing must be between 0 and 359 inclusive'
        assert speed <= 100, 'Speed parameter must be less than 100'
        assert leg_pickup_height > 0, 'Leg pickup height must be a positive non-zero number'
        x_step_size, y_step_size = ik.polar_to_cartesian(step_size, direction)
        leg_0_fd_x = self.current_cartesian_positions[0][0] - x_step_size / 2
        leg_0_bk_x = self.current_cartesian_positions[0][0] + x_step_size / 2
        leg_0_nt_x = self.current_cartesian_positions[0][0]
        leg_0_fd_y = self.current_cartesian_positions[0][1] - y_step_size / 2
        leg_0_bk_y = self.current_cartesian_positions[0][1] + y_step_size / 2
        leg_0_nt_y = self.current_cartesian_positions[0][1]
        leg_0_up_z = self.current_cartesian_positions[0][2] + leg_pickup_height
        leg_0_down_z = self.current_cartesian_positions[0][2]

        leg_1_fd_x = self.current_cartesian_positions[1][0] + x_step_size / 2
        leg_1_bk_x = self.current_cartesian_positions[1][0] - x_step_size / 2
        leg_1_nt_x = self.current_cartesian_positions[1][0]
        leg_1_fd_y = self.current_cartesian_positions[1][1] - y_step_size / 2
        leg_1_bk_y = self.current_cartesian_positions[1][1] + y_step_size / 2
        leg_1_nt_y = self.current_cartesian_positions[1][1]
        leg_1_up_z = self.current_cartesian_positions[1][2] + leg_pickup_height
        leg_1_down_z = self.current_cartesian_positions[1][2]

        leg_2_fd_x = self.current_cartesian_positions[2][0] - x_step_size / 2
        leg_2_bk_x = self.current_cartesian_positions[2][0] + x_step_size / 2
        leg_2_nt_x = self.current_cartesian_positions[2][0]
        leg_2_fd_y = self.current_cartesian_positions[2][1] - y_step_size / 2
        leg_2_bk_y = self.current_cartesian_positions[2][1] + y_step_size / 2
        leg_2_nt_y = self.current_cartesian_positions[2][1]
        leg_2_up_z = self.current_cartesian_positions[2][2] + leg_pickup_height
        leg_2_down_z = self.current_cartesian_positions[2][2]

        leg_3_fd_x = self.current_cartesian_positions[3][0] + x_step_size / 2
        leg_3_bk_x = self.current_cartesian_positions[3][0] - x_step_size / 2
        leg_3_nt_x = self.current_cartesian_positions[3][0]
        leg_3_fd_y = self.current_cartesian_positions[3][1] - y_step_size / 2
        leg_3_bk_y = self.current_cartesian_positions[3][1] + y_step_size / 2
        leg_3_nt_y = self.current_cartesian_positions[3][1]
        leg_3_up_z = self.current_cartesian_positions[3][2] + leg_pickup_height
        leg_3_down_z = self.current_cartesian_positions[3][2]

        leg_4_fd_x = self.current_cartesian_positions[4][0] - x_step_size / 2
        leg_4_bk_x = self.current_cartesian_positions[4][0] + x_step_size / 2
        leg_4_nt_x = self.current_cartesian_positions[4][0]
        leg_4_fd_y = self.current_cartesian_positions[4][1] + y_step_size / 2
        leg_4_bk_y = self.current_cartesian_positions[4][1] - y_step_size / 2
        leg_4_nt_y = self.current_cartesian_positions[4][1]
        leg_4_up_z = self.current_cartesian_positions[4][2] + leg_pickup_height
        leg_4_down_z = self.current_cartesian_positions[4][2]

        leg_5_fd_x = self.current_cartesian_positions[5][0] + x_step_size / 2
        leg_5_bk_x = self.current_cartesian_positions[5][0] - x_step_size / 2
        leg_5_nt_x = self.current_cartesian_positions[5][0]
        leg_5_fd_y = self.current_cartesian_positions[5][1] + y_step_size / 2
        leg_5_bk_y = self.current_cartesian_positions[5][1] - y_step_size / 2
        leg_5_nt_y = self.current_cartesian_positions[5][1]
        leg_5_up_z = self.current_cartesian_positions[5][2] + leg_pickup_height
        leg_5_down_z = self.current_cartesian_positions[5][2]

        process1 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
        process2 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
        process3 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
        for i in range(3):
            process1[i].join()
            process2[i].join()
            process3[i].join()
        process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
        process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
        process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
        process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
        process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
        process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
        for i in range(3):
            process1[i].join()
            process2[i].join()
            process3[i].join()
            process4[i].join()
            process5[i].join()
            process6[i].join()

        process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
        process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
        process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
        for i in range(3):
            process1[i].join()
            process2[i].join()
            process3[i].join()

        for i in range(number_of_steps):
            process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed)
            process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed)
            process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed)
            process4 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed)
            process5 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed)
            process6 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
            process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
            process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
            process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

        process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
        process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
        process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
        for i in range(3):
           process1[i].join()
           process2[i].join()
           process3[i].join()

        process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed)
        process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed)
        process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed)
        process4 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed)
        process5 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed)
        process6 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed)
        for i in range(3):
            process1[i].join()
            process2[i].join()
            process3[i].join()
            process4[i].join()
            process5[i].join()
            process6[i].join()

        process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
        process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
        process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
        for i in range(3):
           process1[i].join()
           process2[i].join()
           process3[i].join()
    
    def cartesian_to_servo(self, leg, x, y, z, speed):
        processes = [0, 0, 0]
        servo_nums, servo_angles, servo_speeds = hex_ik.cartesian_to_servo(leg, x, y, z, speed, self.foot_length, self.leg_length, self.hip_length, self.__current_positions)        
        for servo_num, servo_angle, servo_speed, i in zip(servo_nums, servo_angles, servo_speeds, [0, 1, 2]):
            processes[i] = self.move_servo_delay_time(servo_num, servo_angle, servo_speed)
        self.current_cartesian_positions[leg] = [x, y, z]
        self.__current_positions[leg*3], self.__current_positions[leg*3+1], self.__current_positions[leg*3+2] = servo_angles[0], servo_angles[1], servo_angles[2]
        return processes

    def circle_bend(self, repeats):
        self.shift_lean(0, 0, 0, 15, 0, 0)
        for i in range(repeats):
            self.shift_lean(0, 0, 0, 12, 3, 0)
            self.shift_lean(0, 0, 0, 9, 6, 0)
            self.shift_lean(0, 0, 0, 6, 9, 0)
            self.shift_lean(0, 0, 0, 3, 12, 0)
            self.shift_lean(0, 0, 0, 0, 15, 0)
            self.shift_lean(0, 0, 0, -3, 12, 0)
            self.shift_lean(0, 0, 0, -6, 9, 0)
            self.shift_lean(0, 0, 0, -9, 6, 0)
            self.shift_lean(0, 0, 0, -12, 3, 0)
            self.shift_lean(0, 0, 0, -15, 0, 0)
            self.shift_lean(0, 0, 0, -12, -3, 0)
            self.shift_lean(0, 0, 0, -9, -6, 0)
            self.shift_lean(0, 0, 0, -6, -9, 0)
            self.shift_lean(0, 0, 0, -3, -12, 0)
            self.shift_lean(0, 0, 0, 0, -15, 0)
            self.shift_lean(0, 0, 0, 3, -12, 0)
            self.shift_lean(0, 0, 0, 6, -9, 0)
            self.shift_lean(0, 0, 0, 9, -6, 0)
            self.shift_lean(0, 0, 0, 12, -3, 0)
            self.shift_lean(0, 0, 0, 15, 0, 0)
        self.shift_lean(0, 0, 0, 0, 0, 0)
         
    def tripod_gait(self, number_of_steps, foot_selection=0, turn_value=1, speed=50, step_size=60, leg_pickup_height=60):
        assert step_size > 0
        assert foot_selection in range(0, 2), 'Foot selection is either 0 or 1'
        assert speed <= 100, 'Speed parameter must be less than 100'
        assert leg_pickup_height > 0, 'Leg pickup height must be a positive non-zero number'
        y_step_size = step_size
        x_step_size = 0
        if foot_selection == 1:
            leg_0_fd_x = self.current_cartesian_positions[0][0] - x_step_size / 2
            leg_0_bk_x = self.current_cartesian_positions[0][0] + x_step_size / 2
            leg_0_nt_x = self.current_cartesian_positions[0][0]
            leg_0_fd_y = self.current_cartesian_positions[0][1] - y_step_size / 2
            leg_0_bk_y = self.current_cartesian_positions[0][1] + y_step_size / 2
            leg_0_nt_y = self.current_cartesian_positions[0][1]
            leg_0_up_z = self.current_cartesian_positions[0][2] + leg_pickup_height
            leg_0_down_z = self.current_cartesian_positions[0][2]

            leg_1_fd_x = self.current_cartesian_positions[1][0] + x_step_size / 2
            leg_1_bk_x = self.current_cartesian_positions[1][0] - x_step_size / 2
            leg_1_nt_x = self.current_cartesian_positions[1][0]
            leg_1_fd_y = self.current_cartesian_positions[1][1] - (y_step_size*turn_value) / 2
            leg_1_bk_y = self.current_cartesian_positions[1][1] + (y_step_size*turn_value) / 2
            leg_1_nt_y = self.current_cartesian_positions[1][1]
            leg_1_up_z = self.current_cartesian_positions[1][2] + leg_pickup_height
            leg_1_down_z = self.current_cartesian_positions[1][2]

            leg_2_fd_x = self.current_cartesian_positions[2][0] - x_step_size / 2
            leg_2_bk_x = self.current_cartesian_positions[2][0] + x_step_size / 2
            leg_2_nt_x = self.current_cartesian_positions[2][0]
            leg_2_fd_y = self.current_cartesian_positions[2][1] - y_step_size / 2
            leg_2_bk_y = self.current_cartesian_positions[2][1] + y_step_size / 2
            leg_2_nt_y = self.current_cartesian_positions[2][1]
            leg_2_up_z = self.current_cartesian_positions[2][2] + leg_pickup_height
            leg_2_down_z = self.current_cartesian_positions[2][2]

            leg_3_fd_x = self.current_cartesian_positions[3][0] + x_step_size / 2
            leg_3_bk_x = self.current_cartesian_positions[3][0] - x_step_size / 2
            leg_3_nt_x = self.current_cartesian_positions[3][0]
            leg_3_fd_y = self.current_cartesian_positions[3][1] - (y_step_size*turn_value) / 2
            leg_3_bk_y = self.current_cartesian_positions[3][1] + (y_step_size*turn_value) / 2
            leg_3_nt_y = self.current_cartesian_positions[3][1]
            leg_3_up_z = self.current_cartesian_positions[3][2] + leg_pickup_height
            leg_3_down_z = self.current_cartesian_positions[3][2]

            leg_4_fd_x = self.current_cartesian_positions[4][0] - x_step_size / 2
            leg_4_bk_x = self.current_cartesian_positions[4][0] + x_step_size / 2
            leg_4_nt_x = self.current_cartesian_positions[4][0]
            leg_4_fd_y = self.current_cartesian_positions[4][1] + y_step_size / 2
            leg_4_bk_y = self.current_cartesian_positions[4][1] - y_step_size / 2
            leg_4_nt_y = self.current_cartesian_positions[4][1]
            leg_4_up_z = self.current_cartesian_positions[4][2] + leg_pickup_height
            leg_4_down_z = self.current_cartesian_positions[4][2]

            leg_5_fd_x = self.current_cartesian_positions[5][0] + x_step_size / 2
            leg_5_bk_x = self.current_cartesian_positions[5][0] - x_step_size / 2
            leg_5_nt_x = self.current_cartesian_positions[5][0]
            leg_5_fd_y = self.current_cartesian_positions[5][1] + (y_step_size*turn_value) / 2
            leg_5_bk_y = self.current_cartesian_positions[5][1] - (y_step_size*turn_value) / 2
            leg_5_nt_y = self.current_cartesian_positions[5][1]
            leg_5_up_z = self.current_cartesian_positions[5][2] + leg_pickup_height
            leg_5_down_z = self.current_cartesian_positions[5][2]
        elif foot_selection == 0:
            leg_0_fd_x = self.current_cartesian_positions[0][0] - x_step_size / 2
            leg_0_bk_x = self.current_cartesian_positions[0][0] + x_step_size / 2
            leg_0_nt_x = self.current_cartesian_positions[0][0]
            leg_0_fd_y = self.current_cartesian_positions[0][1] - (y_step_size*turn_value) / 2
            leg_0_bk_y = self.current_cartesian_positions[0][1] + (y_step_size*turn_value)/ 2
            leg_0_nt_y = self.current_cartesian_positions[0][1]
            leg_0_up_z = self.current_cartesian_positions[0][2] + leg_pickup_height
            leg_0_down_z = self.current_cartesian_positions[0][2]

            leg_1_fd_x = self.current_cartesian_positions[1][0] + x_step_size / 2
            leg_1_bk_x = self.current_cartesian_positions[1][0] - x_step_size / 2
            leg_1_nt_x = self.current_cartesian_positions[1][0]
            leg_1_fd_y = self.current_cartesian_positions[1][1] - y_step_size / 2
            leg_1_bk_y = self.current_cartesian_positions[1][1] + y_step_size / 2
            leg_1_nt_y = self.current_cartesian_positions[1][1]
            leg_1_up_z = self.current_cartesian_positions[1][2] + leg_pickup_height
            leg_1_down_z = self.current_cartesian_positions[1][2]

            leg_2_fd_x = self.current_cartesian_positions[2][0] - x_step_size / 2
            leg_2_bk_x = self.current_cartesian_positions[2][0] + x_step_size / 2
            leg_2_nt_x = self.current_cartesian_positions[2][0]
            leg_2_fd_y = self.current_cartesian_positions[2][1] - (y_step_size*turn_value) / 2
            leg_2_bk_y = self.current_cartesian_positions[2][1] + (y_step_size*turn_value) / 2
            leg_2_nt_y = self.current_cartesian_positions[2][1]
            leg_2_up_z = self.current_cartesian_positions[2][2] + leg_pickup_height
            leg_2_down_z = self.current_cartesian_positions[2][2]

            leg_3_fd_x = self.current_cartesian_positions[3][0] + x_step_size / 2
            leg_3_bk_x = self.current_cartesian_positions[3][0] - x_step_size / 2
            leg_3_nt_x = self.current_cartesian_positions[3][0]
            leg_3_fd_y = self.current_cartesian_positions[3][1] - y_step_size / 2
            leg_3_bk_y = self.current_cartesian_positions[3][1] + y_step_size / 2
            leg_3_nt_y = self.current_cartesian_positions[3][1]
            leg_3_up_z = self.current_cartesian_positions[3][2] + leg_pickup_height
            leg_3_down_z = self.current_cartesian_positions[3][2]

            leg_4_fd_x = self.current_cartesian_positions[4][0] - x_step_size / 2
            leg_4_bk_x = self.current_cartesian_positions[4][0] + x_step_size / 2
            leg_4_nt_x = self.current_cartesian_positions[4][0]
            leg_4_fd_y = self.current_cartesian_positions[4][1] + (y_step_size*turn_value) / 2
            leg_4_bk_y = self.current_cartesian_positions[4][1] - (y_step_size*turn_value) / 2
            leg_4_nt_y = self.current_cartesian_positions[4][1]
            leg_4_up_z = self.current_cartesian_positions[4][2] + leg_pickup_height
            leg_4_down_z = self.current_cartesian_positions[4][2]

            leg_5_fd_x = self.current_cartesian_positions[5][0] + x_step_size / 2
            leg_5_bk_x = self.current_cartesian_positions[5][0] - x_step_size / 2
            leg_5_nt_x = self.current_cartesian_positions[5][0]
            leg_5_fd_y = self.current_cartesian_positions[5][1] + y_step_size / 2
            leg_5_bk_y = self.current_cartesian_positions[5][1] - y_step_size / 2
            leg_5_nt_y = self.current_cartesian_positions[5][1]
            leg_5_up_z = self.current_cartesian_positions[5][2] + leg_pickup_height
            leg_5_down_z = self.current_cartesian_positions[5][2]

        #MOVEMENT
        if foot_selection == 1:
            process1 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()


            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed*turn_value)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed*turn_value)
            process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
            process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed*turn_value)
            process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            for i in range(number_of_steps):
                process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed)
                process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed*turn_value)
                process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed)
                process4 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed*turn_value)
                process5 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed)
                process6 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed*turn_value)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()
                    process4[i].join()
                    process5[i].join()
                    process6[i].join()

                process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
                process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
                process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
                process2 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
                process3 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed*turn_value)
                process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
                process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed*turn_value)
                process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
                process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed*turn_value)
                process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()
                    process4[i].join()
                    process5[i].join()
                    process6[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed)
            process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed*turn_value)
            process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed)
            process4 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed*turn_value)
            process5 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed)
            process6 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed*turn_value)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

        elif foot_selection == 0:
            process1 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed*turn_value)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
            process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed*turn_value)
            process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
            process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed*turn_value)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
            process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
            process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            for i in range(number_of_steps):
                process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed*turn_value)
                process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed)
                process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed*turn_value)
                process4 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed)
                process5 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed*turn_value)
                process6 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()
                    process4[i].join()
                    process5[i].join()
                    process6[i].join()

                process1 = self.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
                process2 = self.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
                process3 = self.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
                process2 = self.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
                process3 = self.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
                process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed*turn_value)
                process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
                process4 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed*turn_value)
                process5 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
                process6 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed*turn_value)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()
                    process4[i].join()
                    process5[i].join()
                    process6[i].join()

                process1 = self.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                process2 = self.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                process3 = self.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                for i in range(3):
                    process1[i].join()
                    process2[i].join()
                    process3[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed*turn_value)
            process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed)
            process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed*turn_value)
            process4 = self.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed)
            process5 = self.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed*turn_value)
            process6 = self.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
                process4[i].join()
                process5[i].join()
                process6[i].join()

            process1 = self.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
            process2 = self.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
            process3 = self.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
            for i in range(3):
                process1[i].join()
                process2[i].join()
                process3[i].join()
    def turn_on_spot(self, number_of_steps, turn_angle, speed=50, step_size=60, leg_pickup_height=60):
        turn_angle = round(self.__calculate_turn_angle(turn_angle)/4 if turn_angle >= 0 else self.__calculate_turn_angle(abs(turn_angle))*-0.25)
        process1 = self.scara_to_servo(0, 165, leg_pickup_height, 100)
        process2 = self.scara_to_servo(3, 165, leg_pickup_height, 100)
        process3 = self.scara_to_servo(4, 165, leg_pickup_height, 100)
        for i in range(2):
            process1[i].join()
            process2[i].join()
            process3[i].join()

        process1 = self.move_servo(2, 90-turn_angle, speed)
        process2 = self.move_servo(5, 90+turn_angle, speed)
        process3 = self.move_servo(8, 90+turn_angle, speed)
        process4 = self.move_servo(11, 90-turn_angle, speed)
        process5 = self.move_servo(14, 90-turn_angle, speed)
        process6 = self.move_servo(17, 90+turn_angle, speed)

        process1.join()
        process2.join()
        process3.join()
        process4.join()
        process5.join()
        process6.join()

        process1 = self.scara_to_servo(0, 165, 0, 100)
        process2 = self.scara_to_servo(3, 165, 0, 100)
        process3 = self.scara_to_servo(4, 165, 0, 100)
        for i in range(2):
            process1[i].join()
            process2[i].join()
            process3[i].join()
        for i in range(0, number_of_steps-1 if number_of_steps != 0 else 0):
            process1 = self.scara_to_servo(1, 165, leg_pickup_height, 100)
            process2 = self.scara_to_servo(2, 165, leg_pickup_height, 100)
            process3 = self.scara_to_servo(5, 165, leg_pickup_height, 100)
            for i in range(2):
                process1[i].join()
                process2[i].join()
                process3[i].join()
            process1 = self.move_servo(2, 90+turn_angle, speed)
            process2 = self.move_servo(5, 90-turn_angle, speed)
            process3 = self.move_servo(8, 90-turn_angle, speed)
            process4 = self.move_servo(11, 90+turn_angle, speed)
            process5 = self.move_servo(14, 90+turn_angle, speed)
            process6 = self.move_servo(17, 90-turn_angle, speed)

            process1.join()
            process2.join()
            process3.join()
            process4.join()
            process5.join()
            process6.join()

            process1 = self.scara_to_servo(1, 165, 0, 100)
            process2 = self.scara_to_servo(2, 165, 0, 100)
            process3 = self.scara_to_servo(5, 165, 0, 100)
            for i in range(2):
                process1[i].join()
                process2[i].join()
                process3[i].join()
            process1 = self.scara_to_servo(0, 165, leg_pickup_height, 100)
            process2 = self.scara_to_servo(3, 165, leg_pickup_height, 100)
            process3 = self.scara_to_servo(4, 165, leg_pickup_height, 100)
            for i in range(2):
                process1[i].join()
                process2[i].join()
                process3[i].join()
            process1 = self.move_servo(2, 90-turn_angle, speed)
            process2 = self.move_servo(5, 90+turn_angle, speed)
            process3 = self.move_servo(8, 90+turn_angle, speed)
            process4 = self.move_servo(11, 90-turn_angle, speed)
            process5 = self.move_servo(14, 90-turn_angle, speed)
            process6 = self.move_servo(17, 90+turn_angle, speed)

            process1.join()
            process2.join()
            process3.join()
            process4.join()
            process5.join()
            process6.join()

            process1 = self.scara_to_servo(0, 165, 0, 100)
            process2 = self.scara_to_servo(3, 165, 0, 100)
            process3 = self.scara_to_servo(4, 165, 0, 100)
            for i in range(2):
                process1[i].join()
                process2[i].join()
                process3[i].join()
        process1 = self.scara_to_servo(1, 165, leg_pickup_height, 100)
        process2 = self.scara_to_servo(2, 165, leg_pickup_height, 100)
        process3 = self.scara_to_servo(5, 165, leg_pickup_height, 100)
        for i in range(2):
            process1[i].join()
            process2[i].join()
            process3[i].join()
        process1 = self.move_servo(2, 90, speed)
        process2 = self.move_servo(5, 90, speed)
        process3 = self.move_servo(8, 90, speed)
        process4 = self.move_servo(11, 90, speed)
        process5 = self.move_servo(14, 90, speed)
        process6 = self.move_servo(17, 90, speed)

        process1.join()
        process2.join()
        process3.join()
        process4.join()
        process5.join()
        process6.join()

        process1 = self.scara_to_servo(1, 165, 0, 100)
        process2 = self.scara_to_servo(2, 165, 0, 100)
        process3 = self.scara_to_servo(5, 165, 0, 100)
        for i in range(2):
            process1[i].join()
            process2[i].join()
            process3[i].join()
    def __calculate_turn_angle(self, alpha):
        x, y, z = self.current_cartesian_positions[0]
        extension, _ = ik.cartesian_to_polar(x, y)
        return alpha + asin((self.body_side_length/extension)*sin(alpha*radian_constant)) / radian_constant
    def __scara_to_servo_calculation(self, leg, e, z):
        z -= (self.foot_length - 90)
        w = (1 if e >= 0 else -1) * e
        v = w - self.hip_length
        alpha = atan2(z, v) + acos((self.leg_length**2 - self.foot_length**2 + v**2 + z**2) / 2 / self.leg_length / (v**2 + z**2)**0.5)
        beta = acos((self.leg_length**2 + self.foot_length**2 - v**2 - z**2 ) / 2 / self.leg_length / self.foot_length)

        alpha = alpha / radian_constant
        beta = beta / radian_constant

        if leg == 0:
            alpha = 135 - alpha
            beta += 25
        elif leg == 1:
            alpha += 45
            beta = 155 - beta
        elif leg == 2:
            alpha = 135 - alpha
            beta += 25
        elif leg == 3:
            alpha += 45
            beta = 155 - beta
        elif leg == 4:
            alpha = 135 - alpha
            beta += 25
        elif leg == 5:
            alpha += 45
            beta = 155 - beta
        alpha = round(alpha)
        beta = round(beta)
        return (beta, alpha)
    def scara_to_servo(self, leg, e, z, speed):
        speed = (7.5 - (speed / 15)) ** 2
        tibia, femur = self.__scara_to_servo_calculation(leg, e, z)
        c_tibia, c_femur = self.__current_positions[leg*3], self.__current_positions[leg*3+1]
        tibia_diff, femur_diff = tibia-c_tibia, femur-c_femur
        differences = [tibia_diff, femur_diff]
        max_diff = max([abs(i) for i in differences])
        try:
            femur_speed = abs(1 / (femur_diff / max_diff / speed))
        except:
            femur_speed = 0
        try:
            tibia_speed = abs(1 / (tibia_diff / max_diff / speed))
        except:
            tibia_speed = 0
        servo_nums = [leg*3, leg*3+1]
        servo_angles = [tibia, femur]
        servo_speeds = [tibia_speed, femur_speed]
        processes = [0, 0]
        for servo_num, servo_angle, servo_speed, i in zip(servo_nums, servo_angles, servo_speeds, range(2)):
            processes[i] = self.move_servo_delay_time(servo_num, servo_angle, servo_speed)
        return processes

if __name__ == "__main__":
    h = APHex(MG996R)
    h.unfold(15)
    h.fold(15)
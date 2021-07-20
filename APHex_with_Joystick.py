import APHex
import xbox
import time
joy = xbox.Joystick()

if __name__ == '__main__':
    h = APHex.APHex(APHex.MG996R)
    time.sleep(2)
    p = h.move_servo(0, 90, 100)
    p.join()
    time.sleep(0.2)
    p = h.move_servo(0, 180, 100)
    p.join()
    time.sleep(0.2)
    leaning_shifting_mode = False
    swift_mode = False
    x0 = h.current_cartesian_positions[0][0]
    y0 = h.current_cartesian_positions[0][1]
    z0 = h.current_cartesian_positions[0][2]
    x1 = h.current_cartesian_positions[1][0]
    y1 = h.current_cartesian_positions[1][1]
    z1 = h.current_cartesian_positions[1][2]
    x2 = h.current_cartesian_positions[2][0]
    y2 = h.current_cartesian_positions[2][1]
    z2 = h.current_cartesian_positions[2][2]
    x3 = h.current_cartesian_positions[3][0]
    y3 = h.current_cartesian_positions[3][1]
    z3 = h.current_cartesian_positions[3][2]
    x4 = h.current_cartesian_positions[4][0]
    y4 = h.current_cartesian_positions[4][1]
    z4 = h.current_cartesian_positions[4][2]
    x5 = h.current_cartesian_positions[5][0]
    y5 = h.current_cartesian_positions[5][1]
    z5 = h.current_cartesian_positions[5][2]
    while 1:
        try:
            while 1:
                if joy.Start():
                    if h.folded():
                        h.unfold(15)
                    else:
                        h.fold(15)
                    x0 = h.current_cartesian_positions[0][0]
                    y0 = h.current_cartesian_positions[0][1]
                    z0 = h.current_cartesian_positions[0][2]
                    x1 = h.current_cartesian_positions[1][0]
                    y1 = h.current_cartesian_positions[1][1]
                    z1 = h.current_cartesian_positions[1][2]
                    x2 = h.current_cartesian_positions[2][0]
                    y2 = h.current_cartesian_positions[2][1]
                    z2 = h.current_cartesian_positions[2][2]
                    x3 = h.current_cartesian_positions[3][0]
                    y3 = h.current_cartesian_positions[3][1]
                    z3 = h.current_cartesian_positions[3][2]
                    x4 = h.current_cartesian_positions[4][0]
                    y4 = h.current_cartesian_positions[4][1]
                    z4 = h.current_cartesian_positions[4][2]
                    x5 = h.current_cartesian_positions[5][0]
                    y5 = h.current_cartesian_positions[5][1]
                    z5 = h.current_cartesian_positions[5][2]
                if joy.X():
                    h.shift_lean(0, 0, 60, 0, 0, 0)
                    time.sleep(0.3)
                    while joy.X():
                        h.shift_lean(0, 0, -30, 0, 0, 0)
                        time.sleep(0.2)
                        h.shift_lean(0, 0, 60, 0, 0, 0)
                        time.sleep(0.2)
                    time.sleep(0.1)
                    h.shift_lean(0, 0, 0, 0, 0, 0)
                if joy.dpadUp():
                    femur = 1
                    tibia = 0
                    width = 30
                    p = h.move_servo(femur, 180 if femur in [4, 10, 16] else 0, 85)
                    p.join()
                    time.sleep(0.3)
                    if tibia % 2 == 0:
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadUp():
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    else:
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadUp():
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    p = h.move_servo(femur, 90, 85)
                    p.join()
                    time.sleep(0.3)
                if joy.dpadDown():
                    femur = 16
                    tibia = 15
                    width = 30
                    p = h.move_servo(femur, 180 if femur in [4, 10, 16] else 0, 85)
                    p.join()
                    time.sleep(0.3)
                    if tibia % 2 == 0:
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadUp():
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    else:
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadDown():
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    p = h.move_servo(femur, 90, 85)
                    p.join()
                    time.sleep(0.3)
                if joy.dpadLeft():
                    femur = 7
                    tibia = 6
                    width = 30
                    p = h.move_servo(femur, 180 if femur in [4, 10, 16] else 0, 85)
                    p.join()
                    time.sleep(0.3)
                    if tibia % 2 == 0:
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadUp():
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    else:
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadLeft():
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    p = h.move_servo(femur, 90, 85)
                    p.join()
                    time.sleep(0.3)
                if joy.dpadRight():
                    femur = 10
                    tibia = 9
                    width = 30
                    p = h.move_servo(femur, 180 if femur in [4, 10, 16] else 0, 85)
                    p.join()
                    time.sleep(0.3)
                    if tibia % 2 == 0:
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadUp():
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    else:
                        p = h.move_servo(tibia, 90 - width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                        while joy.dpadRight():
                            p = h.move_servo(tibia, 90 + width, 100)
                            p.join()
                            time.sleep(0.2)
                            p = h.move_servo(tibia, 90 - width, 100)
                            p.join()
                            time.sleep(0.2)
                        p = h.move_servo(tibia, 90 + width // 2, 100)
                        p.join()
                        time.sleep(0.2)
                    p = h.move_servo(femur, 90, 85)
                    p.join()
                    time.sleep(0.3)
                if joy.rightBumper():
                    if not h.folded():
                        turn_angle = 12
                        leg_pickup_height = joy.rightTrigger() * 80 + 50
                        speed = joy.leftTrigger() * 80+20
                        process1 = h.scara_to_servo(0, 165, leg_pickup_height, 100)
                        process2 = h.scara_to_servo(3, 165, leg_pickup_height, 100)
                        process3 = h.scara_to_servo(4, 165, leg_pickup_height, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.move_servo(2, 90-turn_angle, speed)
                        process2 = h.move_servo(5, 90+turn_angle, speed)
                        process3 = h.move_servo(8, 90+turn_angle, speed)
                        process4 = h.move_servo(11, 90-turn_angle, speed)
                        process5 = h.move_servo(14, 90-turn_angle, speed)
                        process6 = h.move_servo(17, 90+turn_angle, speed)

                        process1.join()
                        process2.join()
                        process3.join()
                        process4.join()
                        process5.join()
                        process6.join()

                        process1 = h.scara_to_servo(0, 165, 0, 100)
                        process2 = h.scara_to_servo(3, 165, 0, 100)
                        process3 = h.scara_to_servo(4, 165, 0, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                        while joy.rightBumper():
                            speed = joy.leftTrigger()*80+20
                            speed = 10 if speed < 10 else speed

                            process1 = h.scara_to_servo(1, 165, leg_pickup_height, 100)
                            process2 = h.scara_to_servo(2, 165, leg_pickup_height, 100)
                            process3 = h.scara_to_servo(5, 165, leg_pickup_height, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            process1 = h.move_servo(2, 90+turn_angle, speed)
                            process2 = h.move_servo(5, 90-turn_angle, speed)
                            process3 = h.move_servo(8, 90-turn_angle, speed)
                            process4 = h.move_servo(11, 90+turn_angle, speed)
                            process5 = h.move_servo(14, 90+turn_angle, speed)
                            process6 = h.move_servo(17, 90-turn_angle, speed)

                            process1.join()
                            process2.join()
                            process3.join()
                            process4.join()
                            process5.join()
                            process6.join()

                            process1 = h.scara_to_servo(1, 165, 0, 100)
                            process2 = h.scara_to_servo(2, 165, 0, 100)
                            process3 = h.scara_to_servo(5, 165, 0, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            if not joy.rightBumper():
                                break
                            speed = joy.leftTrigger()*80+20
                            leg_pickup_height = joy.rightTrigger() * 80 + 50

                            process1 = h.scara_to_servo(0, 165, leg_pickup_height, 100)
                            process2 = h.scara_to_servo(3, 165, leg_pickup_height, 100)
                            process3 = h.scara_to_servo(4, 165, leg_pickup_height, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            process1 = h.move_servo(2, 90-turn_angle, speed)
                            process2 = h.move_servo(5, 90+turn_angle, speed)
                            process3 = h.move_servo(8, 90+turn_angle, speed)
                            process4 = h.move_servo(11, 90-turn_angle, speed)
                            process5 = h.move_servo(14, 90-turn_angle, speed)
                            process6 = h.move_servo(17, 90+turn_angle, speed)

                            process1.join()
                            process2.join()
                            process3.join()
                            process4.join()
                            process5.join()
                            process6.join()

                            process1 = h.scara_to_servo(0, 165, 0, 100)
                            process2 = h.scara_to_servo(3, 165, 0, 100)
                            process3 = h.scara_to_servo(4, 165, 0, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                        speed = joy.leftTrigger()*80+20
                        leg_pickup_height = joy.rightTrigger() * 80 + 50

                        process1 = h.scara_to_servo(1, 165, leg_pickup_height, 100)
                        process2 = h.scara_to_servo(2, 165, leg_pickup_height, 100)
                        process3 = h.scara_to_servo(5, 165, leg_pickup_height, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                        process1 = h.move_servo(2, 90, speed)
                        process2 = h.move_servo(5, 90, speed)
                        process3 = h.move_servo(8, 90, speed)
                        process4 = h.move_servo(11, 90, speed)
                        process5 = h.move_servo(14, 90, speed)
                        process6 = h.move_servo(17, 90, speed)

                        process1.join()
                        process2.join()
                        process3.join()
                        process4.join()
                        process5.join()
                        process6.join()

                        process1 = h.scara_to_servo(1, 165, 0, 100)
                        process2 = h.scara_to_servo(2, 165, 0, 100)
                        process3 = h.scara_to_servo(5, 165, 0, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                if joy.leftBumper():
                    if not h.folded():
                        turn_angle = -12
                        leg_pickup_height = joy.rightTrigger() * 80 + 50
                        speed = joy.leftTrigger() * 80+20
                        process1 = h.scara_to_servo(0, 165, leg_pickup_height, 100)
                        process2 = h.scara_to_servo(3, 165, leg_pickup_height, 100)
                        process3 = h.scara_to_servo(4, 165, leg_pickup_height, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.move_servo(2, 90-turn_angle, speed)
                        process2 = h.move_servo(5, 90+turn_angle, speed)
                        process3 = h.move_servo(8, 90+turn_angle, speed)
                        process4 = h.move_servo(11, 90-turn_angle, speed)
                        process5 = h.move_servo(14, 90-turn_angle, speed)
                        process6 = h.move_servo(17, 90+turn_angle, speed)

                        process1.join()
                        process2.join()
                        process3.join()
                        process4.join()
                        process5.join()
                        process6.join()

                        process1 = h.scara_to_servo(0, 165, 0, 100)
                        process2 = h.scara_to_servo(3, 165, 0, 100)
                        process3 = h.scara_to_servo(4, 165, 0, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                        while joy.leftBumper():
                            speed = joy.leftTrigger()*80+20
                            speed = 10 if speed < 10 else speed

                            process1 = h.scara_to_servo(1, 165, leg_pickup_height, 100)
                            process2 = h.scara_to_servo(2, 165, leg_pickup_height, 100)
                            process3 = h.scara_to_servo(5, 165, leg_pickup_height, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            process1 = h.move_servo(2, 90+turn_angle, speed)
                            process2 = h.move_servo(5, 90-turn_angle, speed)
                            process3 = h.move_servo(8, 90-turn_angle, speed)
                            process4 = h.move_servo(11, 90+turn_angle, speed)
                            process5 = h.move_servo(14, 90+turn_angle, speed)
                            process6 = h.move_servo(17, 90-turn_angle, speed)

                            process1.join()
                            process2.join()
                            process3.join()
                            process4.join()
                            process5.join()
                            process6.join()

                            process1 = h.scara_to_servo(1, 165, 0, 100)
                            process2 = h.scara_to_servo(2, 165, 0, 100)
                            process3 = h.scara_to_servo(5, 165, 0, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            if not joy.leftBumper():
                                break
                            speed = joy.leftTrigger()*80+20
                            leg_pickup_height = joy.rightTrigger() * 80 + 50

                            process1 = h.scara_to_servo(0, 165, leg_pickup_height, 100)
                            process2 = h.scara_to_servo(3, 165, leg_pickup_height, 100)
                            process3 = h.scara_to_servo(4, 165, leg_pickup_height, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                            process1 = h.move_servo(2, 90-turn_angle, speed)
                            process2 = h.move_servo(5, 90+turn_angle, speed)
                            process3 = h.move_servo(8, 90+turn_angle, speed)
                            process4 = h.move_servo(11, 90-turn_angle, speed)
                            process5 = h.move_servo(14, 90-turn_angle, speed)
                            process6 = h.move_servo(17, 90+turn_angle, speed)

                            process1.join()
                            process2.join()
                            process3.join()
                            process4.join()
                            process5.join()
                            process6.join()

                            process1 = h.scara_to_servo(0, 165, 0, 100)
                            process2 = h.scara_to_servo(3, 165, 0, 100)
                            process3 = h.scara_to_servo(4, 165, 0, 100)
                            for i in range(2):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                        speed = joy.leftTrigger()*80+20
                        leg_pickup_height = joy.rightTrigger() * 80 + 50

                        process1 = h.scara_to_servo(1, 165, leg_pickup_height, 100)
                        process2 = h.scara_to_servo(2, 165, leg_pickup_height, 100)
                        process3 = h.scara_to_servo(5, 165, leg_pickup_height, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                        process1 = h.move_servo(2, 90, speed)
                        process2 = h.move_servo(5, 90, speed)
                        process3 = h.move_servo(8, 90, speed)
                        process4 = h.move_servo(11, 90, speed)
                        process5 = h.move_servo(14, 90, speed)
                        process6 = h.move_servo(17, 90, speed)

                        process1.join()
                        process2.join()
                        process3.join()
                        process4.join()
                        process5.join()
                        process6.join()

                        process1 = h.scara_to_servo(1, 165, 0, 100)
                        process2 = h.scara_to_servo(2, 165, 0, 100)
                        process3 = h.scara_to_servo(5, 165, 0, 100)
                        for i in range(2):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                if joy.B():
                    leaning_shifting_mode = not leaning_shifting_mode
                    time.sleep(0.2)
                if joy.A() and not leaning_shifting_mode and not h.folded():
                    swift_mode = not swift_mode
                    time.sleep(0.2)

                if leaning_shifting_mode and not h.folded():
                    h.shift_lean(joy.leftX(0)*20, joy.leftY(0)*20, joy.leftTrigger()*75, joy.rightY(0)*10, joy.rightX(0)*10, 10*(joy.Y()-joy.A()))
                if not leaning_shifting_mode and not h.folded() and swift_mode and (joy.leftX() != 0 or joy.leftY() != 0):
                    x_step_size, y_step_size = joy.leftX()*70, joy.leftY()*-70
                    leg_pickup_height = joy.rightTrigger()*80+50
                    speed = joy.leftTrigger()*80+20

                    leg_0_fd_x = x0 - x_step_size / 2
                    leg_0_bk_x = x0 + x_step_size / 2
                    leg_0_nt_x = x0
                    leg_0_fd_y = y0 - y_step_size / 2
                    leg_0_bk_y = y0 + y_step_size / 2
                    leg_0_nt_y = y0
                    leg_0_up_z = z0 + leg_pickup_height
                    leg_0_down_z = z0
                    leg_1_fd_x = x1 + x_step_size / 2
                    leg_1_bk_x = x1 - x_step_size / 2
                    leg_1_nt_x = x1
                    leg_1_fd_y = y1 - y_step_size / 2
                    leg_1_bk_y = y1 + y_step_size / 2
                    leg_1_nt_y = y1
                    leg_1_up_z = z1 + leg_pickup_height
                    leg_1_down_z = z1
                    leg_2_fd_x = x2 - x_step_size / 2
                    leg_2_bk_x = x2 + x_step_size / 2
                    leg_2_nt_x = x2
                    leg_2_fd_y = y2 - y_step_size / 2
                    leg_2_bk_y = y2 + y_step_size / 2
                    leg_2_nt_y = y2
                    leg_2_up_z = z2 + leg_pickup_height
                    leg_2_down_z = z2
                    leg_3_fd_x = x3 + x_step_size / 2
                    leg_3_bk_x = x3 - x_step_size / 2
                    leg_3_nt_x = x3
                    leg_3_fd_y = y3 - y_step_size / 2
                    leg_3_bk_y = y3 + y_step_size / 2
                    leg_3_nt_y = y3
                    leg_3_up_z = z3 + leg_pickup_height
                    leg_3_down_z = z3
                    leg_4_fd_x = x4 - x_step_size / 2
                    leg_4_bk_x = x4 + x_step_size / 2
                    leg_4_nt_x = x4
                    leg_4_fd_y = y4 + y_step_size / 2
                    leg_4_bk_y = y4 - y_step_size / 2
                    leg_4_nt_y = y4
                    leg_4_up_z = z4 + leg_pickup_height
                    leg_4_down_z = z4
                    leg_5_fd_x = x5 + x_step_size / 2
                    leg_5_bk_x = x5 - x_step_size / 2
                    leg_5_nt_x = x5
                    leg_5_fd_y = y5 + y_step_size / 2
                    leg_5_bk_y = y5 - y_step_size / 2
                    leg_5_nt_y = x5
                    leg_5_up_z = z5 + leg_pickup_height
                    leg_5_down_z = z5

                    process1 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
                    process2 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
                    process3 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
                    for i in range(3):
                        process1[i].join()
                        process2[i].join()
                        process3[i].join()
                    process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
                    process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
                    process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
                    process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
                    process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
                    process6 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
                    for i in range(3):
                        process1[i].join()
                        process2[i].join()
                        process3[i].join()
                        process4[i].join()
                        process5[i].join()
                        process6[i].join()

                    process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                    process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                    process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                    for i in range(3):
                        process1[i].join()
                        process2[i].join()
                        process3[i].join()
                    while x_step_size != 0 or y_step_size != 0:
                        x_step_size, y_step_size = joy.leftX()*70, joy.leftY()*-70
                        leg_pickup_height = joy.rightTrigger()*80+50
                        speed = joy.leftTrigger()*80+20

                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - y_step_size / 2
                        leg_0_bk_y = y0 + y_step_size / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - y_step_size / 2
                        leg_1_bk_y = y1 + y_step_size / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - y_step_size / 2
                        leg_2_bk_y = y2 + y_step_size / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - y_step_size / 2
                        leg_3_bk_y = y3 + y_step_size / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + y_step_size / 2
                        leg_4_bk_y = y4 - y_step_size / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + y_step_size / 2
                        leg_5_bk_y = y5 - y_step_size / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5

                        process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed)
                        process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed)
                        process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed)
                        process4 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed)
                        process5 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed)
                        process6 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                        x_step_size, y_step_size = joy.leftX()*70, joy.leftY()*-70
                        leg_pickup_height = joy.rightTrigger()*80+50
                        speed = joy.leftTrigger()*80+20
                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - y_step_size / 2
                        leg_0_bk_y = y0 + y_step_size / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - y_step_size / 2
                        leg_1_bk_y = y1 + y_step_size / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - y_step_size / 2
                        leg_2_bk_y = y2 + y_step_size / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - y_step_size / 2
                        leg_3_bk_y = y3 + y_step_size / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + y_step_size / 2
                        leg_4_bk_y = y4 - y_step_size / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + y_step_size / 2
                        leg_5_bk_y = y5 - y_step_size / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5

                        process1 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
                        process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
                        process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                    x_step_size, y_step_size = joy.leftX()*70, joy.leftY()*-70
                    leg_pickup_height = joy.rightTrigger()*80+50
                    speed = joy.leftTrigger()*80+20
                    leg_0_fd_x = x0 - x_step_size / 2
                    leg_0_bk_x = x0 + x_step_size / 2
                    leg_0_nt_x = x0
                    leg_0_fd_y = y0 - y_step_size / 2
                    leg_0_bk_y = y0 + y_step_size / 2
                    leg_0_nt_y = y0
                    leg_0_up_z = z0 + leg_pickup_height
                    leg_0_down_z = z0
                    leg_1_fd_x = x1 + x_step_size / 2
                    leg_1_bk_x = x1 - x_step_size / 2
                    leg_1_nt_x = x1
                    leg_1_fd_y = y1 - y_step_size / 2
                    leg_1_bk_y = y1 + y_step_size / 2
                    leg_1_nt_y = y1
                    leg_1_up_z = z1 + leg_pickup_height
                    leg_1_down_z = z1
                    leg_2_fd_x = x2 - x_step_size / 2
                    leg_2_bk_x = x2 + x_step_size / 2
                    leg_2_nt_x = x2
                    leg_2_fd_y = y2 - y_step_size / 2
                    leg_2_bk_y = y2 + y_step_size / 2
                    leg_2_nt_y = y2
                    leg_2_up_z = z2 + leg_pickup_height
                    leg_2_down_z = z2
                    leg_3_fd_x = x3 + x_step_size / 2
                    leg_3_bk_x = x3 - x_step_size / 2
                    leg_3_nt_x = x3
                    leg_3_fd_y = y3 - y_step_size / 2
                    leg_3_bk_y = y3 + y_step_size / 2
                    leg_3_nt_y = y3
                    leg_3_up_z = z3 + leg_pickup_height
                    leg_3_down_z = z3
                    leg_4_fd_x = x4 - x_step_size / 2
                    leg_4_bk_x = x4 + x_step_size / 2
                    leg_4_nt_x = x4
                    leg_4_fd_y = y4 + y_step_size / 2
                    leg_4_bk_y = y4 - y_step_size / 2
                    leg_4_nt_y = y4
                    leg_4_up_z = z4 + leg_pickup_height
                    leg_4_down_z = z4
                    leg_5_fd_x = x5 + x_step_size / 2
                    leg_5_bk_x = x5 - x_step_size / 2
                    leg_5_nt_x = x5
                    leg_5_fd_y = y5 + y_step_size / 2
                    leg_5_bk_y = y5 - y_step_size / 2
                    leg_5_nt_y = x5
                    leg_5_up_z = z5 + leg_pickup_height
                    leg_5_down_z = z5

                    process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                    process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                    process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                    for i in range(3):
                       process1[i].join()
                       process2[i].join()
                       process3[i].join()

                    process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed)
                    process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed)
                    process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed)
                    process4 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed)
                    process5 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed)
                    process6 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed)
                    for i in range(3):
                        process1[i].join()
                        process2[i].join()
                        process3[i].join()
                        process4[i].join()
                        process5[i].join()
                        process6[i].join()

                    process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
                    process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
                    process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
                    for i in range(3):
                       process1[i].join()
                       process2[i].join()
                       process3[i].join()

                if not leaning_shifting_mode and not h.folded() and not swift_mode and joy.leftY() != 0:
                    x_step_size, y_step_size = 0, joy.leftY()*-70
                    leg_pickup_height = joy.rightTrigger()*80+50
                    speed = joy.leftTrigger()*80+20
                    foot_selection = 0 if joy.leftX() <= 0 else 1
                    turn_value = 1 - abs(joy.leftX()/2.5)

                    if foot_selection == 1:
                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - y_step_size / 2
                        leg_0_bk_y = y0 + y_step_size / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - (y_step_size*turn_value) / 2
                        leg_1_bk_y = y1 + (y_step_size*turn_value) / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - y_step_size / 2
                        leg_2_bk_y = y2 + y_step_size / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - (y_step_size*turn_value) / 2
                        leg_3_bk_y = y3 + (y_step_size*turn_value) / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + y_step_size / 2
                        leg_4_bk_y = y4 - y_step_size / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + (y_step_size*turn_value) / 2
                        leg_5_bk_y = y5 - (y_step_size*turn_value) / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5
                    elif foot_selection == 0:
                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - (y_step_size*turn_value) / 2
                        leg_0_bk_y = y0 + (y_step_size*turn_value) / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - y_step_size / 2
                        leg_1_bk_y = y1 + y_step_size / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - (y_step_size*turn_value) / 2
                        leg_2_bk_y = y2 + (y_step_size*turn_value) / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - y_step_size / 2
                        leg_3_bk_y = y3 + y_step_size / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + (y_step_size*turn_value) / 2
                        leg_4_bk_y = y4 - (y_step_size*turn_value) / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + y_step_size / 2
                        leg_5_bk_y = y5 - y_step_size / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5

                    #MOVEMENT
                    if foot_selection == 1:
                        process1 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()


                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed*turn_value)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed*turn_value)
                        process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
                        process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed*turn_value)
                        process6 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                    elif foot_selection == 0:
                        process1 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_up_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_up_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed*turn_value)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
                        process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed*turn_value)
                        process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
                        process6 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed*turn_value)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                        process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                        process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                    while not joy.leftY() == 0:
                        x_step_size, y_step_size = 0, joy.leftY()*-70
                        leg_pickup_height = joy.rightTrigger()*80+50
                        speed = joy.leftTrigger()*80+20
                        foot_selection = 0 if joy.leftX() <= 0 else 1
                        turn_value = 1 - abs(joy.leftX()/2.5)
                        if foot_selection == 1:
                            leg_0_fd_x = x0 - x_step_size / 2
                            leg_0_bk_x = x0 + x_step_size / 2
                            leg_0_nt_x = x0
                            leg_0_fd_y = y0 - y_step_size / 2
                            leg_0_bk_y = y0 + y_step_size / 2
                            leg_0_nt_y = y0
                            leg_0_up_z = z0 + leg_pickup_height
                            leg_0_down_z = z0
                            leg_1_fd_x = x1 + x_step_size / 2
                            leg_1_bk_x = x1 - x_step_size / 2
                            leg_1_nt_x = x1
                            leg_1_fd_y = y1 - (y_step_size*turn_value) / 2
                            leg_1_bk_y = y1 + (y_step_size*turn_value) / 2
                            leg_1_nt_y = y1
                            leg_1_up_z = z1 + leg_pickup_height
                            leg_1_down_z = z1
                            leg_2_fd_x = x2 - x_step_size / 2
                            leg_2_bk_x = x2 + x_step_size / 2
                            leg_2_nt_x = x2
                            leg_2_fd_y = y2 - y_step_size / 2
                            leg_2_bk_y = y2 + y_step_size / 2
                            leg_2_nt_y = y2
                            leg_2_up_z = z2 + leg_pickup_height
                            leg_2_down_z = z2
                            leg_3_fd_x = x3 + x_step_size / 2
                            leg_3_bk_x = x3 - x_step_size / 2
                            leg_3_nt_x = x3
                            leg_3_fd_y = y3 - (y_step_size*turn_value) / 2
                            leg_3_bk_y = y3 + (y_step_size*turn_value) / 2
                            leg_3_nt_y = y3
                            leg_3_up_z = z3 + leg_pickup_height
                            leg_3_down_z = z3
                            leg_4_fd_x = x4 - x_step_size / 2
                            leg_4_bk_x = x4 + x_step_size / 2
                            leg_4_nt_x = x4
                            leg_4_fd_y = y4 + y_step_size / 2
                            leg_4_bk_y = y4 - y_step_size / 2
                            leg_4_nt_y = y4
                            leg_4_up_z = z4 + leg_pickup_height
                            leg_4_down_z = z4
                            leg_5_fd_x = x5 + x_step_size / 2
                            leg_5_bk_x = x5 - x_step_size / 2
                            leg_5_nt_x = x5
                            leg_5_fd_y = y5 + (y_step_size*turn_value) / 2
                            leg_5_bk_y = y5 - (y_step_size*turn_value) / 2
                            leg_5_nt_y = x5
                            leg_5_up_z = z5 + leg_pickup_height
                            leg_5_down_z = z5
                        elif foot_selection == 0:
                            leg_0_fd_x = x0 - x_step_size / 2
                            leg_0_bk_x = x0 + x_step_size / 2
                            leg_0_nt_x = x0
                            leg_0_fd_y = y0 - (y_step_size*turn_value) / 2
                            leg_0_bk_y = y0 + (y_step_size*turn_value) / 2
                            leg_0_nt_y = y0
                            leg_0_up_z = z0 + leg_pickup_height
                            leg_0_down_z = z0
                            leg_1_fd_x = x1 + x_step_size / 2
                            leg_1_bk_x = x1 - x_step_size / 2
                            leg_1_nt_x = x1
                            leg_1_fd_y = y1 - y_step_size / 2
                            leg_1_bk_y = y1 + y_step_size / 2
                            leg_1_nt_y = y1
                            leg_1_up_z = z1 + leg_pickup_height
                            leg_1_down_z = z1
                            leg_2_fd_x = x2 - x_step_size / 2
                            leg_2_bk_x = x2 + x_step_size / 2
                            leg_2_nt_x = x2
                            leg_2_fd_y = y2 - (y_step_size*turn_value) / 2
                            leg_2_bk_y = y2 + (y_step_size*turn_value) / 2
                            leg_2_nt_y = y2
                            leg_2_up_z = z2 + leg_pickup_height
                            leg_2_down_z = z2
                            leg_3_fd_x = x3 + x_step_size / 2
                            leg_3_bk_x = x3 - x_step_size / 2
                            leg_3_nt_x = x3
                            leg_3_fd_y = y3 - y_step_size / 2
                            leg_3_bk_y = y3 + y_step_size / 2
                            leg_3_nt_y = y3
                            leg_3_up_z = z3 + leg_pickup_height
                            leg_3_down_z = z3
                            leg_4_fd_x = x4 - x_step_size / 2
                            leg_4_bk_x = x4 + x_step_size / 2
                            leg_4_nt_x = x4
                            leg_4_fd_y = y4 + (y_step_size*turn_value) / 2
                            leg_4_bk_y = y4 - (y_step_size*turn_value) / 2
                            leg_4_nt_y = y4
                            leg_4_up_z = z4 + leg_pickup_height
                            leg_4_down_z = z4
                            leg_5_fd_x = x5 + x_step_size / 2
                            leg_5_bk_x = x5 - x_step_size / 2
                            leg_5_nt_x = x5
                            leg_5_fd_y = y5 + y_step_size / 2
                            leg_5_bk_y = y5 - y_step_size / 2
                            leg_5_nt_y = x5
                            leg_5_up_z = z5 + leg_pickup_height
                            leg_5_down_z = z5
                        if foot_selection == 0:
                            process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                            process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                            process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                            process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed*turn_value)
                            process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed)
                            process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed*turn_value)
                            process4 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed)
                            process5 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed*turn_value)
                            process6 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                                process4[i].join()
                                process5[i].join()
                                process6[i].join()

                            process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
                            process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
                            process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                        elif foot_selection == 1:
                            process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                            process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                            process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                            process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_up_z, speed)
                            process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_up_z, speed*turn_value)
                            process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_up_z, speed)
                            process4 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_down_z, speed*turn_value)
                            process5 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_down_z, speed)
                            process6 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_down_z, speed*turn_value)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                                process4[i].join()
                                process5[i].join()
                                process6[i].join()

                            process1 = h.cartesian_to_servo(0, leg_0_fd_x, leg_0_fd_y, leg_0_down_z, 100)
                            process2 = h.cartesian_to_servo(3, leg_3_fd_x, leg_3_fd_y, leg_3_down_z, 100)
                            process3 = h.cartesian_to_servo(4, leg_4_fd_x, leg_4_fd_y, leg_4_down_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                        x_step_size, y_step_size = 0, joy.leftY()*-70
                        leg_pickup_height = joy.rightTrigger()*80+50
                        speed = joy.leftTrigger()*80+20
                        foot_selection = 0 if joy.leftX() <= 0 else 1
                        turn_value = 1 - abs(joy.leftX()/2.5)
                        if foot_selection == 1:
                            leg_0_fd_x = x0 - x_step_size / 2
                            leg_0_bk_x = x0 + x_step_size / 2
                            leg_0_nt_x = x0
                            leg_0_fd_y = y0 - y_step_size / 2
                            leg_0_bk_y = y0 + y_step_size / 2
                            leg_0_nt_y = y0
                            leg_0_up_z = z0 + leg_pickup_height
                            leg_0_down_z = z0
                            leg_1_fd_x = x1 + x_step_size / 2
                            leg_1_bk_x = x1 - x_step_size / 2
                            leg_1_nt_x = x1
                            leg_1_fd_y = y1 - (y_step_size*turn_value) / 2
                            leg_1_bk_y = y1 + (y_step_size*turn_value) / 2
                            leg_1_nt_y = y1
                            leg_1_up_z = z1 + leg_pickup_height
                            leg_1_down_z = z1
                            leg_2_fd_x = x2 - x_step_size / 2
                            leg_2_bk_x = x2 + x_step_size / 2
                            leg_2_nt_x = x2
                            leg_2_fd_y = y2 - y_step_size / 2
                            leg_2_bk_y = y2 + y_step_size / 2
                            leg_2_nt_y = y2
                            leg_2_up_z = z2 + leg_pickup_height
                            leg_2_down_z = z2
                            leg_3_fd_x = x3 + x_step_size / 2
                            leg_3_bk_x = x3 - x_step_size / 2
                            leg_3_nt_x = x3
                            leg_3_fd_y = y3 - (y_step_size*turn_value) / 2
                            leg_3_bk_y = y3 + (y_step_size*turn_value) / 2
                            leg_3_nt_y = y3
                            leg_3_up_z = z3 + leg_pickup_height
                            leg_3_down_z = z3
                            leg_4_fd_x = x4 - x_step_size / 2
                            leg_4_bk_x = x4 + x_step_size / 2
                            leg_4_nt_x = x4
                            leg_4_fd_y = y4 + y_step_size / 2
                            leg_4_bk_y = y4 - y_step_size / 2
                            leg_4_nt_y = y4
                            leg_4_up_z = z4 + leg_pickup_height
                            leg_4_down_z = z4
                            leg_5_fd_x = x5 + x_step_size / 2
                            leg_5_bk_x = x5 - x_step_size / 2
                            leg_5_nt_x = x5
                            leg_5_fd_y = y5 + (y_step_size*turn_value) / 2
                            leg_5_bk_y = y5 - (y_step_size*turn_value) / 2
                            leg_5_nt_y = x5
                            leg_5_up_z = z5 + leg_pickup_height
                            leg_5_down_z = z5
                        elif foot_selection == 0:
                            leg_0_fd_x = x0 - x_step_size / 2
                            leg_0_bk_x = x0 + x_step_size / 2
                            leg_0_nt_x = x0
                            leg_0_fd_y = y0 - (y_step_size*turn_value) / 2
                            leg_0_bk_y = y0 + (y_step_size*turn_value) / 2
                            leg_0_nt_y = y0
                            leg_0_up_z = z0 + leg_pickup_height
                            leg_0_down_z = z0
                            leg_1_fd_x = x1 + x_step_size / 2
                            leg_1_bk_x = x1 - x_step_size / 2
                            leg_1_nt_x = x1
                            leg_1_fd_y = y1 - y_step_size / 2
                            leg_1_bk_y = y1 + y_step_size / 2
                            leg_1_nt_y = y1
                            leg_1_up_z = z1 + leg_pickup_height
                            leg_1_down_z = z1
                            leg_2_fd_x = x2 - x_step_size / 2
                            leg_2_bk_x = x2 + x_step_size / 2
                            leg_2_nt_x = x2
                            leg_2_fd_y = y2 - (y_step_size*turn_value) / 2
                            leg_2_bk_y = y2 + (y_step_size*turn_value) / 2
                            leg_2_nt_y = y2
                            leg_2_up_z = z2 + leg_pickup_height
                            leg_2_down_z = z2
                            leg_3_fd_x = x3 + x_step_size / 2
                            leg_3_bk_x = x3 - x_step_size / 2
                            leg_3_nt_x = x3
                            leg_3_fd_y = y3 - y_step_size / 2
                            leg_3_bk_y = y3 + y_step_size / 2
                            leg_3_nt_y = y3
                            leg_3_up_z = z3 + leg_pickup_height
                            leg_3_down_z = z3
                            leg_4_fd_x = x4 - x_step_size / 2
                            leg_4_bk_x = x4 + x_step_size / 2
                            leg_4_nt_x = x4
                            leg_4_fd_y = y4 + (y_step_size*turn_value) / 2
                            leg_4_bk_y = y4 - (y_step_size*turn_value) / 2
                            leg_4_nt_y = y4
                            leg_4_up_z = z4 + leg_pickup_height
                            leg_4_down_z = z4
                            leg_5_fd_x = x5 + x_step_size / 2
                            leg_5_bk_x = x5 - x_step_size / 2
                            leg_5_nt_x = x5
                            leg_5_fd_y = y5 + y_step_size / 2
                            leg_5_bk_y = y5 - y_step_size / 2
                            leg_5_nt_y = x5
                            leg_5_up_z = z5 + leg_pickup_height
                            leg_5_down_z = z5
                        if foot_selection == 1:
                            process1 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
                            process2 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
                            process3 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                            process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed*turn_value)
                            process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed)
                            process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed*turn_value)
                            process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed)
                            process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed*turn_value)
                            process6 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                                process4[i].join()
                                process5[i].join()
                                process6[i].join()

                            process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                            process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                            process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                        elif foot_selection == 0:
                            process1 = h.cartesian_to_servo(1, leg_1_bk_x, leg_1_bk_y, leg_1_up_z, 100)
                            process2 = h.cartesian_to_servo(2, leg_2_bk_x, leg_2_bk_y, leg_2_up_z, 100)
                            process3 = h.cartesian_to_servo(5, leg_5_bk_x, leg_5_bk_y, leg_5_up_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()

                            process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_up_z, speed)
                            process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_up_z, speed*turn_value)
                            process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_up_z, speed)
                            process4 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_down_z, speed*turn_value)
                            process5 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_down_z, speed)
                            process6 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_down_z, speed*turn_value)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                                process4[i].join()
                                process5[i].join()
                                process6[i].join()

                            process1 = h.cartesian_to_servo(1, leg_1_fd_x, leg_1_fd_y, leg_1_down_z, 100)
                            process2 = h.cartesian_to_servo(2, leg_2_fd_x, leg_2_fd_y, leg_2_down_z, 100)
                            process3 = h.cartesian_to_servo(5, leg_5_fd_x, leg_5_fd_y, leg_5_down_z, 100)
                            for i in range(3):
                                process1[i].join()
                                process2[i].join()
                                process3[i].join()
                    x_step_size, y_step_size = 0, joy.leftY()*-70
                    leg_pickup_height = joy.rightTrigger()*80+50
                    speed = joy.leftTrigger()*80+20
                    foot_selection = 0 if joy.leftX() <= 0 else 1
                    turn_value = 1 - abs(joy.leftX()/2.5)
                    if foot_selection == 1:
                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - y_step_size / 2
                        leg_0_bk_y = y0 + y_step_size / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - (y_step_size*turn_value) / 2
                        leg_1_bk_y = y1 + (y_step_size*turn_value) / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - y_step_size / 2
                        leg_2_bk_y = y2 + y_step_size / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - (y_step_size*turn_value) / 2
                        leg_3_bk_y = y3 + (y_step_size*turn_value) / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + y_step_size / 2
                        leg_4_bk_y = y4 - y_step_size / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + (y_step_size*turn_value) / 2
                        leg_5_bk_y = y5 - (y_step_size*turn_value) / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5
                    elif foot_selection == 0:
                        leg_0_fd_x = x0 - x_step_size / 2
                        leg_0_bk_x = x0 + x_step_size / 2
                        leg_0_nt_x = x0
                        leg_0_fd_y = y0 - (y_step_size*turn_value) / 2
                        leg_0_bk_y = y0 + (y_step_size*turn_value) / 2
                        leg_0_nt_y = y0
                        leg_0_up_z = z0 + leg_pickup_height
                        leg_0_down_z = z0
                        leg_1_fd_x = x1 + x_step_size / 2
                        leg_1_bk_x = x1 - x_step_size / 2
                        leg_1_nt_x = x1
                        leg_1_fd_y = y1 - y_step_size / 2
                        leg_1_bk_y = y1 + y_step_size / 2
                        leg_1_nt_y = y1
                        leg_1_up_z = z1 + leg_pickup_height
                        leg_1_down_z = z1
                        leg_2_fd_x = x2 - x_step_size / 2
                        leg_2_bk_x = x2 + x_step_size / 2
                        leg_2_nt_x = x2
                        leg_2_fd_y = y2 - (y_step_size*turn_value) / 2
                        leg_2_bk_y = y2 + (y_step_size*turn_value) / 2
                        leg_2_nt_y = y2
                        leg_2_up_z = z2 + leg_pickup_height
                        leg_2_down_z = z2
                        leg_3_fd_x = x3 + x_step_size / 2
                        leg_3_bk_x = x3 - x_step_size / 2
                        leg_3_nt_x = x3
                        leg_3_fd_y = y3 - y_step_size / 2
                        leg_3_bk_y = y3 + y_step_size / 2
                        leg_3_nt_y = y3
                        leg_3_up_z = z3 + leg_pickup_height
                        leg_3_down_z = z3
                        leg_4_fd_x = x4 - x_step_size / 2
                        leg_4_bk_x = x4 + x_step_size / 2
                        leg_4_nt_x = x4
                        leg_4_fd_y = y4 + (y_step_size*turn_value) / 2
                        leg_4_bk_y = y4 - (y_step_size*turn_value) / 2
                        leg_4_nt_y = y4
                        leg_4_up_z = z4 + leg_pickup_height
                        leg_4_down_z = z4
                        leg_5_fd_x = x5 + x_step_size / 2
                        leg_5_bk_x = x5 - x_step_size / 2
                        leg_5_nt_x = x5
                        leg_5_fd_y = y5 + y_step_size / 2
                        leg_5_bk_y = y5 - y_step_size / 2
                        leg_5_nt_y = x5
                        leg_5_up_z = z5 + leg_pickup_height
                        leg_5_down_z = z5
                    if foot_selection == 1:
                        process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed)
                        process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed*turn_value)
                        process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed)
                        process4 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed*turn_value)
                        process5 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed)
                        process6 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed*turn_value)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                    elif foot_selection == 0:
                        process1 = h.cartesian_to_servo(0, leg_0_bk_x, leg_0_bk_y, leg_0_up_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_bk_x, leg_3_bk_y, leg_3_up_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_bk_x, leg_4_bk_y, leg_4_up_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_up_z, speed*turn_value)
                        process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_up_z, speed)
                        process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_up_z, speed*turn_value)
                        process4 = h.cartesian_to_servo(1, leg_1_nt_x, leg_1_nt_y, leg_1_down_z, speed)
                        process5 = h.cartesian_to_servo(2, leg_2_nt_x, leg_2_nt_y, leg_2_down_z, speed*turn_value)
                        process6 = h.cartesian_to_servo(5, leg_5_nt_x, leg_5_nt_y, leg_5_down_z, speed)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
                            process4[i].join()
                            process5[i].join()
                            process6[i].join()

                        process1 = h.cartesian_to_servo(0, leg_0_nt_x, leg_0_nt_y, leg_0_down_z, 100)
                        process2 = h.cartesian_to_servo(3, leg_3_nt_x, leg_3_nt_y, leg_3_down_z, 100)
                        process3 = h.cartesian_to_servo(4, leg_4_nt_x, leg_4_nt_y, leg_4_down_z, 100)
                        for i in range(3):
                            process1[i].join()
                            process2[i].join()
                            process3[i].join()
        except Exception:
            h.shift_lean(0, 0, 0, 0, 0, 0)


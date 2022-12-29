import time
import tmotorCAN
import numpy as np
import trajectory

motor1 = tmotorCAN.tmotor(2, 'ak80-64')

start_time = time.time()

lis = []

motor1.attain(0, 0, 0, 20, 1)

w = 6.28/5

pos = 0
vel = 0

try:
    for i in range(int(100 * 60)):
        time.sleep(0.01)
        t = time.time() - start_time

        print(t)
        
        desired_pos = trajectory.theta_6(w, t, 0)
        desired_vel = trajectory.omega_6(w, t, 0)

        desired_tor = 0
        pos, vel, tau = motor1.attain(desired_pos, desired_vel, desired_tor, 50, 3)
        
        lis.append([t, desired_pos, desired_vel, desired_tor, pos, vel, tau])

except KeyboardInterrupt as e:
    pass

finally:
    np.savetxt("trajectory_knee_5s.csv", lis, delimiter=",")

motor1.exit_motor_mode()
import time
import tmotorCAN
import numpy as np
import trajectory

# motor1 = tmotorCAN.tmotor(1, 'ak80-64')
motor2 = tmotorCAN.tmotor(2, 'ak80-64')
# motor3 = tmotorCAN.tmotor(3, 'ak80-64')
motor4 = tmotorCAN.tmotor(5, 'ak10-9')

motor2.attain(0, 0, 0, 20, 1)

# motor = tmotorCAN.tmotor(2, 'ak10-9')

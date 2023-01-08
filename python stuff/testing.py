import tmotorCAN

# motor1 = tmotorCAN.tmotor(1, 'AK80-64')
# motor2 = tmotorCAN.tmotor(2, 'AK80-64')
# motor = tmotorCAN.tmotor(3, 'AK80-64')
# motor = tmotorCAN.tmotor(4, 'AK80-64')
# motor = tmotorCAN.tmotor(5, 'AK10-9')
motor = tmotorCAN.tmotor(6, 'AK10-9')

motor.start_motor()

motor.attain(3.14, 0, 0, 10, 1)

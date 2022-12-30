import time
import tmotorCAN
import numpy as np
import channel_config
from matplotlib import pyplot as plt

ch0 = channel_config.start_channel()

id_1 = 1
id_2 = 2

# Delta is how much the vertical is offset from the actual zero of the motor
delta_1 = 0
delta_2 = 0

#Makes motor come to centre position

t_in = 0
p_in = 0

init_time = time.time()

motor = tmotorCAN.tmotor(1, 'ak80-64')

while True:

    current_time = time.time() - init_time
    p_out, v_out, t_out = motor.attain(delta_1 + p_in, 0, t_in, 50, 5)
        
    #Note: without load: A = 10, with load: A = 18
    A = 10
    
    t_in = A * np.sin(p_in)
    p_in = p_out    

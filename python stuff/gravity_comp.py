import time
import canlib
import canlib.canlib as clb
import tmotorCAN
import numpy as np
import channel_config
import trajectory
from matplotlib import pyplot as plt

ch0 = channel_config.start_channel()

id_1 = 1
id_2 = 2

# Delta is how much the vertical is offset from the actual zero of the motor
delta_1 = 0
delta_2 = -3.14 - 0.5

#Makes motor come to centre position

t_in = 0
p_in = 0

file = open("output_data.txt", "w")
file.close()

init_time = time.time()

#if p_in - p_out > 10, switch off motor

frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + p_in, 0, t_in), flags=clb.MessageFlag.STD)
ch0.write(frame)
time.sleep(0.01)


while True:
    current_time = time.time() - init_time
    frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + p_in, 0, t_in), flags=clb.MessageFlag.STD)
    ch0.write(frame)
    time.sleep(0.01)

    output_msg = ch0.read().data
    p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)

    t_in = + 10 * np.sin(p_out)
    p_in = p_out
    
    file = open("output_data.txt", "a")
    file.writelines([str(current_time),"  ", str(t_in),"  ", str(t_out), "\n"])
    file.close()

import channel_config
import canlib
import canlib.canlib as clb
import tmotorCAN
import time

delta_1 = -3.14
delta_2 = -3.14 - 0.5

kp =  10.0
kd = 1.0

ch0 = channel_config.start_channel()

frame = canlib.Frame(id_= 1, data=tmotorCAN.enter_motor_mode(), flags=clb.MessageFlag.STD)
ch0.write(frame)

time.sleep(0.001)

frame = canlib.Frame(id_= 2, data=tmotorCAN.enter_motor_mode(), flags=clb.MessageFlag.STD)
ch0.write(frame)

frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(delta_1, 0, 30, kp, kd), flags=clb.MessageFlag.STD)        
ch0.write(frame)
time.sleep(0.001)
frame = canlib.Frame(id_= 2, data=tmotorCAN.pack_cmd(delta_2, 0, 30, kp, kd), flags=clb.MessageFlag.STD)        
ch0.write(frame)
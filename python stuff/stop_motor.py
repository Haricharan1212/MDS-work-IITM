import channel_config
import canlib
import canlib.canlib as clb
import tmotorCAN
import time

ch0 = channel_config.start_channel()

frame = canlib.Frame(id_= 1, data=tmotorCAN.exit_motor_mode(), flags=clb.MessageFlag.STD)
ch0.write(frame)
time.sleep(0)
frame = canlib.Frame(id_= 2, data=tmotorCAN.exit_motor_mode(), flags=clb.MessageFlag.STD)
ch0.write(frame)

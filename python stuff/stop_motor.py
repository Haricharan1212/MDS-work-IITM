import channel_config
import canlib
import canlib.canlib as clb
import tmotorCAN

ch0 = channel_config.start_channel()

frame = canlib.Frame(id_= 1, data=tmotorCAN.exit_motor_mode(), flags=clb.MessageFlag.STD)
ch0.write(frame)

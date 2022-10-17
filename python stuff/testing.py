import time
import canlib
import canlib.canlib as clb
import tmotorCAN
import numpy as np
import channel_config

ch0 = channel_config.start_channel()
# Sending messages

theta = np.genfromtxt('theta.csv', delimiter = ",")
omega = np.genfromtxt('omega.csv', delimiter = ",")

shape = np.shape(theta)

#We need theta 5
n = 4

frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(3.14, 0, 30, 7.26, -0.31), flags=clb.MessageFlag.STD)
ch0.write(frame)
time.sleep(3)

start_time = time.time()
for i in range(1000000):    

    # frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(3.14 + theta[n][i], omega[n][i], 30, 7.26, 0.31), flags=clb.MessageFlag.EXT)
    frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(3.14, 0, 30, 100, 5), flags=clb.MessageFlag.STD)

    ch0.write(frame)

    while True:
        try:        
            # print(input_frame.data)
            break
        except clb.canNoMsg:
            pass
        except clb.canError as ex:
            print(ex)
    time.sleep(0.01)

end_time = time.time()
print(end_time - start_time)

channel_config.tearDownChannel(ch0)
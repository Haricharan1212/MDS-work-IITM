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

#126 values, not 24
# theta = np.genfromtxt('theta.csv', delimiter = ",")
# omega = np.genfromtxt('omega.csv', delimiter = ",")
# shape = np.shape(theta)

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

while True:
    current_time = time.time() - init_time
    frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + trajectory.theta_5(1.7, current_time), trajectory.omega_5(1.7, current_time), t_in), flags=clb.MessageFlag.STD)
    ch0.write(frame)
    time.sleep(0.01)

    output_msg = ch0.read().data
    p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
    t_in = 18 * np.sin(p_in)

    file = open("output_data.txt", "a")
    file.writelines([str(current_time),"  ", str(t_in),"  ", str(t_out), "\n"])
    file.close()

# frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
# ch0.write(frame)


"""

# Clearing current file to be empty
file = open("output_data.txt", "w")
file.close()

start_time = time.time()

for f in range(1000):    
    # Sending required trajectory position and velocity
    current_time = time.time()
    t = current_time - start_time
    
    # w = 3
    # theta_5 = trajectory.theta_5(w, t)
    # omega_5 = trajectory.omega_5(w, t)
    
    # w = 3
    # theta_6 = trajectory.theta_6(w, t)
    # omega_6 = trajectory.omega_6(w, t)

    w = 1
    theta_5 = np.sin(w * t)
    omega_5 = w * np.cos(w * t)
    theta_6 = 0
    omega_6 = 0

    frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + theta_5, omega_5, torque, kp, kd), flags=clb.MessageFlag.STD)        
    ch0.write(frame)
    time.sleep(0.001)
    # frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2 + theta_6, omega_6 - omega_5, torque, kp, kd), flags=clb.MessageFlag.STD)        
    # ch0.write(frame)

    try:                                
        # Writing required output data to a file
        output_msg = ch0.read().data
        p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
        file = open("output_data.txt", "a")
        file.writelines([str(t),"," , str(theta_5), "," , str(p_out), ",", str(omega_5), "," , str(v_out),"," , str(torque), "," , str(t_out), ";"])
        file.close()
        # output_msg = ch0.read().data
        # p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
        # file.writelines([str(t),"," , str(theta_6), "," , str(p_out), ",", str(omega_6 - omega_5), "," , str(v_out),"," , str(torque), "," , str(t_out), "\n"])
        # file.close()
    except clb.canNoMsg:
        pass
    except clb.canError as ex:
        print(ex)
    
    # Time for each step
    time.sleep(0.01)

    # Time between end of one trajectory and start of another trajectory

# Logging the amount of time
end_time = time.time()
print(end_time - start_time)

#Makes motor come to centre position
frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)
# frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
# ch0.write(frame)

channel_config.tearDownChannel(ch0)
"""
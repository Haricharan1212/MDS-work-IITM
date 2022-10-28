import time
import canlib
import canlib.canlib as clb
import tmotorCAN
import numpy as np
import channel_config
import trajectory

ch0 = channel_config.start_channel()

id_1 = 1
id_2 = 2

#126 values, not 24
# theta = np.genfromtxt('theta.csv', delimiter = ",")
# omega = np.genfromtxt('omega.csv', delimiter = ",")
# shape = np.shape(theta)

# Delta is how much the vertical is offset from the actual zero of the motor
delta_1 = -6.14 + 3.0
delta_2 = -3.14

torque = 30 # Why
kp =  10
kd = 1

#Makes motor come to centre position
frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)
time.sleep(0.001)
frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)

time.sleep(1)

# Clearing current file to be empty
file = open("output_data.txt", "w")
file.close()

start_time = time.time()

for t in range(650):    
    # Sending required trajectory position and velocity
    current_time = time.time()
    t = current_time - start_time
    
    w = 1
    theta_5 = trajectory.theta_5(w, t)
    omega_5 = trajectory.omega_5(w, t)
    
    w = 1
    theta_6 = trajectory.theta_6(w, t)
    omega_6 = trajectory.omega_6(w, t)

    frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + theta_5, omega_5, torque, kp, kd), flags=clb.MessageFlag.STD)        
    ch0.write(frame)
    time.sleep(0.001)
    frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2 + theta_6 - theta_5, omega_6 - omega_5, torque, kp, kd), flags=clb.MessageFlag.STD)        
    ch0.write(frame)

    try:                                
        # Writing required output data to a file
        # output_msg = ch0.read().data
        # p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
        # file = open("output_data.txt", "a")
        # file.writelines([str(t),"," , str(theta), "," , str(p_out), ",", str(omega), "," , str(v_out),"," , str(torque), "," , str(t_out), "\n"])
        # file.close()
       ...                     
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
frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2, 0, torque, 500, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)

channel_config.tearDownChannel(ch0)

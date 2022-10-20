import time
import canlib
import canlib.canlib as clb
import tmotorCAN
import numpy as np
import channel_config
import trajectory

ch0 = channel_config.start_channel()

#126 values, not 24
# theta = np.genfromtxt('theta.csv', delimiter = ",")
# omega = np.genfromtxt('omega.csv', delimiter = ",")
# shape = np.shape(theta)

#We need theta 5
n = 4

# Delta is how much the vertical is offset from the actual zero of the motor
delta = -6.14 + 3.0

torque = 30 # Why
kp = 50
kd = 3

#Makes motor come to centre position
frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(delta, 0, torque, kp, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)
time.sleep(1)

# Clearing current file to be empty
file = open("output_data.txt", "w")
file.close()

start_time = time.time()

w = 3

# Number of trajectories
for t in range(5000):    
    # Sending required trajectory position and velocity
    current_time = time.time()
    t = current_time - start_time
    theta = trajectory.theta_5(w, t)
    omega = trajectory.omega_5(w, t)
    frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(delta + theta, omega, torque, kp, kd), flags=clb.MessageFlag.STD)        
    ch0.write(frame)

    try:                                
        # Writing required output data to a file
        output_msg = ch0.read().data
        p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
        file = open("output_data.txt", "a")
        file.writelines([str(t),"," , str(theta), "," , str(p_out), ",", str(omega), "," , str(v_out),"," , str(t_out), "\n"])
        file.close()
                            
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
frame = canlib.Frame(id_= 1, data=tmotorCAN.pack_cmd(delta, 0, torque, kp, kd), flags=clb.MessageFlag.STD)
ch0.write(frame)

channel_config.tearDownChannel(ch0)
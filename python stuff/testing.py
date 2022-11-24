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

# Delta is how much the vertical is offset from the actual zero of the motor
delta_1 = 0
delta_2 = 0

#Makes motor come to centre position

t_in = 0
p_in = 0
v_in = 0

# Clearing current file to be empty
file = open("output_data.txt", "w")
file.close()

start_time = time.time()

for f in range(1000):    
    # Sending required trajectory position and velocity
    current_time = time.time()
    t = current_time - start_time
    
    w1 = 1.2
    theta_5 = trajectory.theta_5(w1, t)
    omega_5 = trajectory.omega_5(w1, t)
    
    w2 = 1.2
    theta_6 = trajectory.theta_6(w2, t)
    omega_6 = trajectory.omega_6(w2, t)

    torque_5 = 0
    torque_6 = 0

    frame = canlib.Frame(id_= id_1, data=tmotorCAN.pack_cmd(delta_1 + theta_5, omega_5, torque_5), flags=clb.MessageFlag.STD)        
    ch0.write(frame)
    time.sleep(0.001)

    frame = canlib.Frame(id_= id_2, data=tmotorCAN.pack_cmd(delta_2 + theta_6 - theta_5, omega_6 - omega_5, torque_6), flags=clb.MessageFlag.STD)        
    ch0.write(frame)

    try:                                
        output_msg = ch0.read().data
        p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)

        if (abs(t_out) > 20):
            frame = canlib.Frame(id_= id_2, data=tmotorCAN.exit_motor_mode(), flags=clb.MessageFlag.STD)        
            ch0.write(frame)

            tmotorCAN.exit_motor_mode()
            raise Exception("Your torque value is too high!!")

        file = open("output_data.txt", "a")
        file.writelines(f"{t} {theta_5} {p_out} {omega_5} {v_out} {torque_5} {t_out}\n")
        file.close()

        # output_msg = ch0.read().data
        # p_out, v_out, t_out = tmotorCAN.unpack_reply(output_msg)
        # file.writelines([str(t),"," , str(theta_6), "," , str(p_out), ",", str(omega_6 - omega_5), "," , str(v_out),"," , str(torque), "," , str(t_out), "\n"])
        # file.close()

    except clb.canNoMsg:
        pass
    except clb.canError as ex:
        print(ex)
    
    time.sleep(0.01)

channel_config.tearDownChannel(ch0)

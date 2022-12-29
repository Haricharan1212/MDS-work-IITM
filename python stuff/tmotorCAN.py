import time
import canlib
import canlib.canlib as clb
import tmotorCAN
import numpy as np
import channel_config
import trajectory

class tmotor():

    def __init__(self, id, type):
        self.channel = channel_config.start_channel()
        self.id = id
        
        frame = canlib.Frame(id_= self.id, data=self.enter_motor_mode(), flags=clb.MessageFlag.STD)
        self.channel.write(frame)
        time.sleep(0.001)
                
        if (type == "ak80-64"):
            self.P_MIN = -12.5
            self.P_MAX = 12.5
            self.V_MIN = -8.0
            self.V_MAX = 8.0
            self.KP_MIN = 0.0
            self.KP_MAX = 500.0
            self.KD_MIN = 0.0
            self.KD_MAX = 5.0
            self.T_MIN = -144.0
            self.T_MAX = 144.0

        elif (type == "ak10-9"):
            self.P_MIN = -12.5
            self.P_MAX = 12.5
            self.V_MIN = -50.0
            self.V_MAX = +50.0
            self.KP_MIN = 0.0
            self.KP_MAX = 500.0
            self.KD_MIN = 0.0
            self.KD_MAX = 5.0
            self.T_MIN = -65.0
            self.T_MAX = 65.0

        else:
            raise (ValueError)

    def attain(self, p_in, v_in, t_in, kp, kd):

        frame = canlib.Frame(id_= self.id, data=self.pack_cmd(p_in, v_in, t_in, kp, kd), flags=clb.MessageFlag.STD)
        self.channel.write(frame)

        try:
            time.sleep(0.00001)
            output_msg = self.channel.read().data
            p_out, v_out, t_out = self.unpack_reply(output_msg)
            return p_out, v_out, t_out
        except ZeroDivisionError:
            return None, None, None

#Helper functions
    def constrain(self, value, min_value, max_value):
        """Function which constrains the given value between min value and max value"""
        if (value < min_value):
            return min_value
        if (value > max_value):
            return max_value
        return value

    def float_to_uint(self, x, x_min, x_max, bits):
        """Function to convert float x into it's unsigned integer equivalent"""
        span = x_max - x_min
        offset = x_min
        pgg = 0
        if (bits == 12):
            pgg = (x - offset) * 4095.0/ span
        elif (bits == 16):
            pgg = (x - offset) * 65535.0/ span
            
        return int(pgg)
        
    def uint_to_float(self, x_int, x_min, x_max, bits):
        """Function to convert unsigned integer x_int into it's float x equivalent"""
        span = x_max - x_min
        offset = x_min
        pgg = 0
        if (bits == 12):
            pgg = x_int * span / 4095.0 + offset
        elif (bits == 16):
            pgg = x_int * span / 65535.0 + offset
        return pgg

    #Data creation functions
    def enter_motor_mode(self):
        """Function which creates array to turn the motor ON in MIT motor mode"""
        
        buf = [0 for i in range(8)]
        buf[0] = 0xFF
        buf[1] = 0xFF
        buf[2] = 0xFF
        buf[3] = 0xFF
        buf[4] = 0xFF
        buf[5] = 0xFF
        buf[6] = 0xFF
        buf[7] = 0xFC

        return buf

    def exit_motor_mode(self):
        """Function which creates array to turn the motor OFF in MIT motor mode"""

        buf = [0 for i in range(8)]
        
        buf[0] = 0xFF
        buf[1] = 0xFF
        buf[2] = 0xFF
        buf[3] = 0xFF
        buf[4] = 0xFF
        buf[5] = 0xFF
        buf[6] = 0xFF
        buf[7] = 0xFD
        
        return buf

    def zero(self):
        
        """Function which creates array to make the motor come to ZERO position"""

        buf = [0 for i in range(8)]
        buf[0] = 0x00
        buf[1] = 0xFF
        buf[2] = 0xFF
        buf[3] = 0xFF
        buf[4] = 0x02
        buf[5] = 0x01
        buf[6] = 0xFF
        buf[7] = 0xFE
        
        return buf
        
    def pack_cmd(self, p_in, v_in, t_in, kp_in, kd_in):
        """Function which creates required array given p_in, v_in, t_in, k_p, k_d"""

        p_des = self.constrain(p_in,self.P_MIN,self.P_MAX)
        v_des = self.constrain(v_in,self.V_MIN,self.V_MAX)
        kp = self.constrain(kp_in, self.KP_MIN, self.KP_MAX)
        kd = self.constrain(kd_in, self.KD_MIN, self.KD_MAX)
        t_ff = self.constrain(t_in,self.T_MIN,self.T_MAX)
    
        p_int = self.float_to_uint(p_des,self.P_MIN,self.P_MAX, 16)
        v_int = self.float_to_uint(v_des,self.V_MIN,self.V_MAX, 12)
        kp_int = self.float_to_uint(kp, self.KP_MIN, self.KP_MAX, 12)
        kd_int = self.float_to_uint(kd, self.KD_MIN, self.KD_MAX, 12)
        t_int = self.float_to_uint(t_ff,self.T_MIN,self.T_MAX, 12)
        
        buf = [0 for i in range(8)]
        
        buf[0] = p_int >> 8
        buf[1] = p_int & 0xFF
        buf[2] = v_int >> 4
        buf[3] = ((v_int & 0xF) << 4) | (kp_int >> 8)
        buf[4] = kp_int & 0xFF
        buf[5] = kd_int >> 4
        buf[6] = ((kd_int & 0xF) << 4) | (t_int >> 8)
        buf[7] = t_int & 0xFF

        return buf

    def unpack_reply(self, buf):
        """Function which converts given array data into float format"""
        
        id = buf[0]
        p_int = (buf[1] << 8) | buf[2]
        v_int = (buf[3] << 4) | (buf[4] >> 4)
        i_int = ((buf[4] & 0xF) << 8) | buf[5]

        p_out = self.uint_to_float(p_int,self.P_MIN,self.P_MAX, 16)
        v_out = self.uint_to_float(v_int,self.V_MIN,self.V_MAX, 12)
        t_out = self.uint_to_float(i_int, -self.T_MAX,self.T_MAX, 12)

        return p_out, v_out, t_out

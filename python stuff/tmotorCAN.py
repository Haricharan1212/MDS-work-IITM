P_MIN = -12.5
P_MAX = 12.5
V_MIN = -8.0
V_MAX = 8.0
KP_MIN = 0.0
KP_MAX = 500.0
KD_MIN = 0.0
KD_MAX = 5.0
T_MIN = -144.0
T_MAX = 144.0

p_in = 0.0
v_in = 0.0
kp_in = 10.0
kd_in = 1.0
t_in = 30.0

p_out = 0.0
v_out = 0.0
t_out = 0.0

motor_ID = 0x01

#Helper functions
def constrain(value, min_value, max_value):
    """Function which constrains the given value between min value and max value"""
    if (value < min_value):
        return min_value
    if (value > max_value):
        return max_value
    return value

def float_to_uint(x, x_min, x_max, bits):
    """Function to convert float x into it's unsigned integer equivalent"""
    span = x_max - x_min
    offset = x_min
    pgg = 0
    if (bits == 12):
        pgg = (x - offset) * 4095.0/ span
    elif (bits == 16):
        pgg = (x - offset) * 65535.0/ span
        
    return int(pgg)
    
def uint_to_float(x_int, x_min, x_max, bits):
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
def enter_motor_mode():
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

def exit_motor_mode():
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

def zero():
    
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
    
def pack_cmd(p_in, v_in, t_in, kp_, kd_):
    """Function which creates required array given p_in, v_in, t_in, k_p, k_d"""

    p_des = constrain(p_in, P_MIN, P_MAX)
    v_des = constrain(v_in, V_MIN, V_MAX)
    kp = constrain(kp_in, KP_MIN, KP_MAX)
    kd = constrain(kd_in, KD_MIN, KD_MAX)
    t_ff = constrain(t_in, T_MIN, T_MAX)
  
    p_int = float_to_uint(p_des, P_MIN, P_MAX, 16)
    v_int = float_to_uint(v_des, V_MIN, V_MAX, 12)
    kp_int = float_to_uint(kp, KP_MIN, KP_MAX, 12)
    kd_int = float_to_uint(kd, KD_MIN, KD_MAX, 12)
    t_int = float_to_uint(t_ff, T_MIN, T_MAX, 12)
    
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

def unpack_reply(buf):
    """Function which converts given array data into float format"""
    
    id = buf[0]
    p_int = (buf[1] << 8) | buf[2]
    v_int = (buf[3] << 4) | (buf[4] >> 4)
    i_int = ((buf[4] & 0xF) << 8) | buf[5]
    
    p_out = uint_to_float(p_int, P_MIN, P_MAX, 16);
    v_out = uint_to_float(v_int, V_MIN, V_MAX, 12);
    t_out = uint_to_float(i_int, -T_MAX, T_MAX, 12);

    return p_out, v_out, t_out


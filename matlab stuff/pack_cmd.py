
# Defining some constants
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

# Kp, Kd values, change here

kp_in = 50.0
kd_in = 5.0

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
    
def pack_cmd(p_in, v_in, t_in):
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



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


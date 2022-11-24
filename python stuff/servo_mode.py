from enum import Enum
import channel_config
import canlib
import canlib.canlib as clb

CAN_PACKET_SET_DUTY = 0
CAN_PACKET_SET_CURRENT = 1
CAN_PACKET_SET_CURRENT_BRAKE = 2
CAN_PACKET_SET_RPM = 3
CAN_PACKET_SET_POS = 4
CAN_PACKET_SET_ORIGIN_HERE = 5
CAN_PACKET_SET_POS_SPD = 6
    
ch0 = channel_config.start_channel()    
    
# void comm_can_transmit_eid(uint32_t id, const uint8_t *data, uint8_t len) {
# uint8_t i=0;
# if (len > 8) {
# len = 8;
# }
# CanTxMsg TxMessage;
# TxMessage.StdId = 0;
# TxMessage.IDE = CAN_ID_EXT;
# TxMessage.ExtId = id;
# TxMessage.RTR = CAN_RTR_DATA;
# TxMessage.DLC = len;

# for(i=0;i<len;i++)
# TxMessage.Data[i]=data[i];
# CAN_Transmit(CHASSIS_CAN, &TxMessage);
# }

def comm_can_transmit_eid(id, data, length):
    i = 0
    if (length > 8):
        length = 8
    frame = canlib.Frame(id_= id, data = data, dlc = 4, flags=clb.MessageFlag.EXT)
    ch0.write(frame)

# Note: we don't need buffer_append_int32, 16 functions because of python to_bytes function, so it is commented out

#     void buffer_append_int32(uint8_t* buffer, int32_t number, int32_t *index) {
# buffer[(*index)++] = number >> 24;
# buffer[(*index)++] = number >> 16;
# buffer[(*index)++] = number >> 8;
# buffer[(*index)++] = number;
# }

def buffer_append_int32(buffer, number, index):
    number = int(number)

    buffer[index + 0] = number >> 24
    buffer[index + 1] = number >> 16
    buffer[index + 2] = number >> 8
    buffer[index + 3] = number >> 0

    buffer = [i % 256 for i in buffer]

    return buffer
    
# # void buffer_append_int16(uint8_t* buffer, int16_t number, int16_t *index) {
# # buffer[(*index)++] = number >> 8;
# # buffer[(*index)++] = number;

# def buffer_append_int16(buffer, number, index):
#     number = int(number)
#     buffer[index + 0] = number >> 8
#     buffer[index + 1] = number >> 0
    
#     buffer = [i % 256 for i in buffer]

#     return buffer
    
    
# void comm_can_set_duty(uint8_t controller_id, float duty) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(duty * 100000.0), &send_index);
# comm_can_transmit_eid(controller_id |((uint32_t)CAN_PACKET_SET_DUTY << 8), buffer,
# send_index);
# }

def comm_can_set_duty(controller_id, duty):
    send_index = 4

    arr = (int(duty * 100000) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid(controller_id |(CAN_PACKET_SET_DUTY << 8), arr, send_index)

# void comm_can_set_current(uint8_t controller_id, float current) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(current * 1000.0), &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_CURRENT << 8), buffer, send_index);
# }

def comm_can_set_current(controller_id, current):
    send_index = 4
    arr = (int(current * 1000.0) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid(controller_id |(CAN_PACKET_SET_CURRENT << 8), arr, send_index)

# void comm_can_set_cb(uint8_t controller_id, float current) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(current * 1000.0), &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_CURRENT_BRAKE << 8), buffer, send_index);
# }

def comm_can_set_cb(controller_id, current):
    send_index = 0
    arr = (int(current * 1000.0) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid(controller_id |(CAN_PACKET_SET_CURRENT_BRAKE << 8), arr, send_index)

# void comm_can_set_rpm(uint8_t controller_id, float rpm) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)rpm, &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_RPM << 8), buffer, send_index);
# }

def comm_can_set_rpm(controller_id, rpm):
    send_index = 4
    arr = (int(rpm) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid(controller_id |(CAN_PACKET_SET_RPM << 8), arr, send_index)

    
# void comm_can_set_pos(uint8_t controller_id, float pos) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(pos * 1000000.0), &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_POS << 8), buffer, send_index);
# }

def comm_can_set_pos(controller_id, pos):
    send_index = 4

    arr = (int(pos * 1000000) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid((controller_id | (CAN_PACKET_SET_POS << 8)), arr, send_index)
 
# void comm_can_set_origin(uint8_t controller_id, uint8_t set_origin_mode) {
# comm_can_transmit_eid(controller_id |
# ((uint32_t) CAN_PACKET_SET_ORIGIN_HERE << 8), buffer, send_index);
# }

# Some error in the above code, as buffer is undefined actually
def comm_can_set_origin(controler_id, set_origin_mode):
    ...

# void comm_can_set_pos_spd(uint8_t controller_id, float pos,int16_t spd, int16_t RPA ) {
# int32_t send_index = 0;
# Int16_t send_index1 = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(pos * 10000.0), &send_index);
# buffer_append_int16(buffer,spd, & send_index1);
# https://www.cubemars.com/
# 39 / 52
# buffer_append_int16(buffer,RPA, & send_index1);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_POS_SPD << 8), buffer, send_index);
# }

def comm_can_set_pos_spd(controller_id, pos, spd, RPA):
    send_index = 8
    
    arr = (int(pos * 1000000) & 0xFFFFFFFF).to_bytes(4, 'big') + (int(spd) & 0xFFFF).to_bytes(2, 'big') + (int(RPA) & 0xFFFF).to_bytes(2, 'big')
    comm_can_transmit_eid((controller_id | (CAN_PACKET_SET_POS_SPD << 8)), arr[::-1], send_index)
    return arr

comm_can_set_rpm(0x00, 2000000)
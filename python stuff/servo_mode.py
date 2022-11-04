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
    
# void buffer_append_int16(uint8_t* buffer, int16_t number, int16_t *index) {
# buffer[(*index)++] = number >> 8;
# buffer[(*index)++] = number;

def buffer_append_int16(buffer, number, index):
    number = int(number)
    buffer[index + 0] = number >> 8
    buffer[index + 1] = number >> 0
    
    buffer = [i % 256 for i in buffer]

    return buffer
    
    
# void comm_can_set_pos(uint8_t controller_id, float pos) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(pos * 1000000.0), &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_POS << 8), buffer, send_index);
# }

def comm_can_set_pos(controller_id, pos):
    send_index = 0
    buffer = [0, 0, 0, 0]
    buffer = buffer_append_int32(buffer, pos * 1000000, send_index)

    arr = (int(pos * 1000000) & 0xFFFFFFFF).to_bytes(4, 'big')
    comm_can_transmit_eid((controller_id | (4 << 8)), arr[::-1], send_index)
 

comm_can_set_pos(0x00, 0)

# void comm_can_set_current(uint8_t controller_id, float current) {
# int32_t send_index = 0;
# uint8_t buffer[4];
# buffer_append_int32(buffer, (int32_t)(current * 1000.0), &send_index);
# comm_can_transmit_eid(controller_id |
# ((uint32_t)CAN_PACKET_SET_CURRENT << 8), buffer, send_index);
# }

def comm_can_set_current(controller_id, current):
    send_index = 0
    arr = (int(current * 1000.0) & 0xFFFFFFFF).to_bytes(4, 'little')
    comm_can_transmit_eid(controller_id |(CAN_PACKET_SET_CURRENT << 8), arr, 4)

# comm_can_set_current(0x00, 0.00001)
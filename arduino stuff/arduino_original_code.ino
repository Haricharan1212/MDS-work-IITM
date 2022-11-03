#include <mcp_can.h>
#include <SPI.h>

//Define LED Pins
#define LED2 8
#define LED3 7

//value limits

#define P_MIN -12.5f
#define P_MAX 12.5f
#define V_MIN -8.0f
#define V_MAX 8.0f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define T_MIN -144.0f
#define T_MAX 144.0f

// 0x02 0x7F 0xFF 0x80 0x18 0x1C
//Set Values
float p_in = 0.0f;
float v_in = 0.0f;
float kp_in = 10.0f;
float kd_in = 1.0f;
float t_in = 30.0f;

//measured values
float p_out = 0.0f;
float v_out = 0.0f;
float t_out = 0.0f;

//array 3 = number of sep
float V1_in_array[60] = {0.021672534, 0.042954273, 0.064761234, 0.086177871, 0.107370717, 0.128667996, 0.149874541, 0.170868316, 0.191698782, 0.212232866, 0.232279549, 0.251619863, 0.269933322, 0.286829249, 0.301845472, 0.31447779, 0.324227394, 0.330646393, 0.333416955, 0.332406736, 0.327991137, 0.319859558, 0.308749682, 0.295229261, 0.279893434, 0.263285997, 0.245870952, 0.228010767, 0.209966164, 0.191912575, 0.173925676, 0.156045832, 0.138264386, 0.120448097, 0.102612252, 0.084850635, 0.066881647, 0.048524847, 0.030441767, 0, -0.098612093, -0.188659873, -0.271301852, -0.347052155, -0.415811644, -0.476915592, -0.52921793, -0.571225031, -0.6012819, -0.617794826, -0.619467312, -0.605504173, -0.575737194, -0.530632179, -0.471164012, -0.398586019, -0.314159703, -0.218943443, -0.113783994, 0.000212431};
float P1_in_array[60] = {0.0002, 0.042954273, 0.064761234, 0.086177871, 0.107370717, 0.128667996, 0.149874541, 0.170868316, 0.191698782, 0.212232866, 0.232279549, 0.251619863, 0.269933322, 0.286829249, 0.301845472, 0.31447779, 0.324227394, 0.330646393, 0.333416955, 0.332406736, 0.327991137, 0.319859558, 0.308749682, 0.295229261, 0.279893434, 0.263285997, 0.245870952, 0.228010767, 0.209966164, 0.191912575, 0.173925676, 0.156045832, 0.138264386, 0.120448097, 0.102612252, 0.084850635, 0.066881647, 0.048524847, 0.030441767, 0, -0.098612093, -0.188659873, -0.271301852, -0.347052155, -0.415811644, -0.476915592, -0.52921793, -0.571225031, -0.6012819, -0.617794826, -0.619467312, -0.605504173, -0.575737194, -0.530632179, -0.471164012, -0.398586019, -0.314159703, -0.218943443, -0.113783994, 0.000212431};


int motor_id[1] = {0x01};
int motor_ID = 0x01;
//MCP_CAN CAN(SPI_CS_PIN);
#define CAN0_INT 2                              // Set INT to pin 2
MCP_CAN CAN0(10);                               // Set CS to pin 10 mega 53

void setup()
{
  Serial.begin(9600);
  delay(1000);
  if (CAN0.begin(MCP_ANY, CAN_1000KBPS, MCP_8MHZ) == CAN_OK)
    Serial.println("MCP2515 Initialized Successfully!");
  else
    Serial.println("Error Initializing MCP2515...");
  Serial.println("CAN BUS Shield init ok!");
  CAN0.setMode(MCP_NORMAL);                     // Set operation mode to normal so the MCP2515 sends acks to received data.

  pinMode(CAN0_INT, INPUT);                            // Configuring pin for /INT input

  //  pinMode(CLICK, INPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);

  //Write LED pins low to turn them off by default
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);

}

void loop()
{
  while (Serial.available() > 0)
  {
    //p_in = 0;

    String data_rec = Serial.readString();
    data_rec.trim();
    Serial.println(data_rec);
    float p_step = 1.57f;
   
  if (data_rec.indexOf("P=") >= 0)
    {
      String abc = data_rec.substring(data_rec.indexOf("=") + 1, data_rec.indexOf(";"));

      float z = abc.toFloat();
      //        v_in = z/100;
      p_in = z;
      Serial.print("moving to: ");
      Serial.println(p_in);
      //         Serial.print("p_in = ");
      //        Serial.println(p_in);
      pack_cmd();
    }

    if (data_rec == "POSARRAY"){
      float arr[] = {0, 1.57, 3.14, 6.28, 1.57};

      for (int i = 0; i < 5; i++) {
        p_in = arr[i];
        Serial.println(arr[i]);
        pack_cmd();
        delay(2000);
        }
    }

    v_in = constrain(v_in, V_MIN, V_MAX);
    p_in = constrain(p_in, P_MIN, P_MAX);
    if (data_rec == "ON")
    {
      //Enable
      Serial.println("Turning On");
      EnterMotorMode();
      digitalWrite(LED2, HIGH);
      unpack_reply();
    }
    if (data_rec == "OFF")
    {
      //Disable 
      Serial.println("Turning off!!");

      ExitMotorMode();
      digitalWrite(LED2, HIGH);
      unpack_reply();
    }
    if (data_rec == "ZERO")
    {
      //Zero position
            Serial.println("Zeroing!!");

      Zero();
      digitalWrite(LED2, HIGH);
      unpack_reply();
      p_in = 0;
      v_in = 0;
    }
  }

}

void EnterMotorMode() {
  //Enter Motor Mode (enable)
  byte buf[8];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0xFF;
  buf[5] = 0xFF;
  buf[6] = 0xFF;
  buf[7] = 0xFC;
  //  CAN0.sendMsgBuf(0x02, 0, 8, buf);
  byte sndStat = CAN0.sendMsgBuf(motor_id[0], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[1], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[2], 0, 8, buf);
  if (sndStat == CAN_OK) {
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
}

void ExitMotorMode() {
  //Exit Motor Mode (enable)
  byte buf[8];
  buf[0] = 0xFF;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0xFF;
  buf[5] = 0xFF;
  buf[6] = 0xFF;
  buf[7] = 0xFD;
  //  CAN0.sendMsgBuf(0x02, 0, 8, buf);
  byte sndStat = CAN0.sendMsgBuf(motor_id[0], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[1], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[2], 0, 8, buf);
  if (sndStat == CAN_OK) {
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
}

void Zero() {
  //Exit Motor Mode (enable)
  byte buf[8];
  buf[0] = 0x00;
  buf[1] = 0xFF;
  buf[2] = 0xFF;
  buf[3] = 0xFF;
  buf[4] = 0x02;
  buf[5] = 0x01;
  buf[6] = 0xFF;
  buf[7] = 0xFE;
  //  CAN0.sendMsgBuf(0x02, 0, 8, buf);// 0x02 id
  byte sndStat = CAN0.sendMsgBuf(motor_id[0], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[1], 0, 8, buf);
  sndStat = CAN0.sendMsgBuf(motor_id[2], 0, 8, buf);
  if (sndStat == CAN_OK) {
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
}

void pack_cmd() {
  byte buf[8];

  /// CAN Command Packet Structure///
  /// 16 bit position command, between -4*pi and 4*pi
  /// 12 bit velocity command, between -30 and +30 rad/s
  /// 12 bit kp, between 0 and 500 N-m/rad
  /// 12 bit kd, between 0 and 1500 N-m*s/rad
  /// 12 bit feed forward torque, between -18 and 18 N-m
  /// CAN Packet is 8 8-bit words
  /// Formatted as follows. For each quantity, bit 0 is LSB
  /// 0: [position[15-8]]
  /// 1: [position[7-0]]
  /// 2: [velocity[11-4]]
  /// 3: [velocity[3-0], kp[11-8]]
  /// 4: [kp[7-0]]
  /// 5: [kd[11-4]]
  /// 6: [kd[3-0], torque[11-8]]
  /// 7: [torque[7-0]]

  /// limit data to be within bounds ///
  float p_des = constrain(p_in, P_MIN, P_MAX);
  float v_des = constrain(v_in, V_MIN, V_MAX);
  float kp = constrain(kp_in, KP_MIN, KP_MAX);
  float kd = constrain(kd_in, KD_MIN, KD_MAX);
  float t_ff = constrain(t_in, T_MIN, T_MAX);
  // Convert floats to unsigned ints ///

  Serial.println(p_des);

  unsigned int p_int = float_to_unit(p_des, P_MIN, P_MAX, 16);
  unsigned int v_int = float_to_unit(v_des, V_MIN, V_MAX, 12);
  unsigned int kp_int = float_to_unit(kp, KP_MIN, KP_MAX, 12);
  unsigned int kd_int = float_to_unit(kd, KD_MIN, KD_MAX, 12);
  unsigned int t_int = float_to_unit(t_ff, T_MIN, T_MAX, 12);
  // pack ints into the can buffer ///
  Serial.print("p_int = ");
  Serial.print(p_int);
  Serial.print(" v_int = ");
  Serial.print(v_int);
  Serial.print(" kp_int = ");
  Serial.print(kp_int);
  Serial.print(" kd_int = ");
  Serial.print(kd_int);
  Serial.print(" t_int =");
  Serial.println(t_int);
  buf[0] = p_int >> 8;
  buf[1] = p_int & 0xFF;
  buf[2] = v_int >> 4;
  buf[3] = ((v_int & 0xF) << 4) | (kp_int >> 8);
  buf[4] = kp_int & 0xFF;
  buf[5] = kd_int >> 4;
  buf[6] = ((kd_int & 0xF) << 4) | (t_int >> 8);
  buf[7] = t_int & 0xFF;
  //  CAN0.sendMsgBuf(0x02, 0, 8, buf);
  byte sndStat = CAN0.sendMsgBuf(motor_ID, 0, 8, buf);
  
  if (sndStat == CAN_OK) {
    Serial.println("Message Sent Successfully!");
  } else {
    Serial.println("Error Sending Message...");
  }
}

void unpack_reply() {

  /// CAN Reply Packet Structure///
  /// 16 bit position, between -4*pi and 4*pi
  /// 12 bit velocity, between -30 and +30 rad/s
  /// 12 bit current, between -40 and 40
  /// CAN Packet is 5 8-bit words
  /// Formatted as follows. For each quantity, bit 0 is LSB
  /// 0: [position[15-8]]
  /// 1: [position[7-0]]
  /// 2: [velocity[11-4]]
  /// 3: [velocity[3-0], current[11-8]]
  /// 4: [current[7-0]]

  byte len = 0;
  byte buf[8];
  //  CAN0.readMsgBuf(&len, buf);
  long unsigned int rxId;
  CAN0.readMsgBuf(&rxId, &len, buf);
  char msgString[128];
  for (byte i = 0; i < len; i++) {
    sprintf(msgString, " 0x%.2X", buf[i]);
    Serial.print(msgString);
  }
  Serial.println("");
  unsigned long canId = rxId;
  //Serial.print(" motor Id = ");
  Serial.print(rxId);
  /// unpack ints from CAN buffer ///
  unsigned int id = buf[0];
  unsigned int p_int = (buf[1] << 8) | buf[2];
  unsigned int v_int = (buf[3] << 4) | (buf[4] >> 4);
  unsigned int i_int = ((buf[4] & 0xF) << 8) | buf[5];
  /// Convert ints to floats ///
  p_out = uint_to_float(p_int, P_MIN, P_MAX, 16);
  v_out = uint_to_float(v_int, V_MIN, V_MAX, 12);
  t_out = uint_to_float(i_int, -T_MAX, T_MAX, 12);

  p_in = p_out;
  v_in = v_out;
  t_in = t_out;

  Serial.print("  p_out = ");
  Serial.print(p_out);
  Serial.print(" v_out = ");
  Serial.print(v_out);
  Serial.print(" t_out = ");
  Serial.println(t_out);
}

unsigned int float_to_unit(float x, float x_min, float x_max, int bits){
    // Converts a float to an unsigned int, given range and number of bits 
    float span = x_max - x_min;
    float offset = x_min;
    unsigned int pgg = 0;
    if(bits == 12){
      pgg = (unsigned int) ((x-offset)*4095.0/span);
    }else if(bits == 16){
      pgg = (unsigned int) ((x-offset)*65535.0/span);
    }
    return pgg;
}

float uint_to_float(unsigned int x_int, float x_min, float x_max, int bits){
  float span = x_max - x_min;
  float offset = x_min;
  float pgg = 0;
  if(bits == 12){
    pgg = ((float)x_int)*span/4095.0 + offset;
  }else if(bits == 16){
    pgg = ((float)x_int)*span/65535.0 + offset;
  }
  return pgg;
}
// END FILE
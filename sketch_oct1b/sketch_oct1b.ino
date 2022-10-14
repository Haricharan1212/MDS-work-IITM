#include <mcp_can.h>
#include <SPI.h>

//Define LED Pins
#define LED2 8
#define LED3 7

//value limits
#define P_MIN -12.5f
#define P_MAX 12.5f
#define V_MIN -30.0f
#define V_MAX 30.0f
#define KP_MIN 0.0f
#define KP_MAX 500.0f
#define KD_MIN 0.0f
#define KD_MAX 5.0f
#define T_MIN -18.0f
#define T_MAX 18.0f

// 0x02 0x7F 0xFF 0x80 0x18 0x1C
//Set Values
float p_in = 0.0f;
float v_in = 0.0f;
float kp_in = 2.0f;
float kd_in = 3.0f;
float t_in = 5.0f;

//measured values
float p_out = 0.0f;
float v_out = 0.0f;
float t_out = 0.0f;

//array 3 = number of sep
float V1_in_array[60] = {0.021672534, 0.042954273, 0.064761234, 0.086177871, 0.107370717, 0.128667996, 0.149874541, 0.170868316, 0.191698782, 0.212232866, 0.232279549, 0.251619863, 0.269933322, 0.286829249, 0.301845472, 0.31447779, 0.324227394, 0.330646393, 0.333416955, 0.332406736, 0.327991137, 0.319859558, 0.308749682, 0.295229261, 0.279893434, 0.263285997, 0.245870952, 0.228010767, 0.209966164, 0.191912575, 0.173925676, 0.156045832, 0.138264386, 0.120448097, 0.102612252, 0.084850635, 0.066881647, 0.048524847, 0.030441767, 0, -0.098612093, -0.188659873, -0.271301852, -0.347052155, -0.415811644, -0.476915592, -0.52921793, -0.571225031, -0.6012819, -0.617794826, -0.619467312, -0.605504173, -0.575737194, -0.530632179, -0.471164012, -0.398586019, -0.314159703, -0.218943443, -0.113783994, 0.000212431};
float V2_in_array[60] = {0.037631325, 0.072336983, 0.102886638, 0.130020144, 0.153429229, 0.172588835, 0.187608227, 0.198521061, 0.205060706, 0.20713864,  0.204670031,  0.197503404 , 0.185566988 , 0.168848816 , 0.147473713 , 0.121752383 , 0.092206627 , 0.059659795 , 0.025173769, -0.010068507, -0.044118104  , -0.077008339  , -0.107019573  , -0.133290171  , -0.155242965  , -0.172607403  , -0.185303744  , -0.19339826 , -0.197042581  , -0.196406315  , -0.191699875  , -0.183059222  , -0.17060944 , -0.154598834  , -0.135017848  , -0.111789447  , -0.085344156  , -0.055986689  , -0.023207108,  0.012785042, 0.016566806, 0.029889201, 0.039108943, 0.043982031, 0.044753012, 0.04199422,  0.036444628, 0.028870976, 0.019966585, 0.01030595,  0.000357741 , -0.00944761 , -0.018624664  , -0.026556775  , -0.032480729  , -0.035559571  , -0.035044095  , -0.030498304  , -0.022049213  , -0.010618266};
float V3_in_array[60] = {-0.021743897 , -0.041815326  , -0.059799183  , -0.075142476  , -0.087583752  , -0.096978111  , -0.103224344  , -0.106312948  , -0.106295994  , -0.103265485  , -0.097355149  , -0.088732515  , -0.077609665  , -0.064247238  , -0.048966186  , -0.032153771  , -0.014259276,  0.004201408, 0.022685143, 0.040661122, 0.055161259, 0.071029668, 0.085151317, 0.097208214, 0.107012105, 0.114481622, 0.119589501, 0.12232619,  0.12265935,  0.120539079, 0.115906082, 0.108725598, 0.098978225, 0.086584498, 0.071541054, 0.053908112, 0.033643245, 0.010959  , -0.0133632  , -0.041856097  , -0.060451165  , -0.111208268  , -0.149965488  , -0.175279062  , -0.186425362  , -0.183333219  , -0.166596773  , -0.137544289  , -0.098305407  , -0.051834222,  -0.001813092  , 0.047572108 , 0.091979626 , 0.127329163 , 0.150213924 , 0.158242482 , 0.150287504 , 0.12667414  , 0.089389565 , 0.042429742};

int motor_id[1] = {0x01};
int motor_ID = 0x00;
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

long previousMillis = 0;
void loop()
{
  while (Serial.available() > 0)
  {
    String data_rec = Serial.readString();
    data_rec.trim();
    Serial.println(data_rec);
    float p_step = 2;


  
    if (data_rec == "RUN")
    {
      Serial.println("Running!!");
      for (int asd = 0; asd < 61 ; asd++) //asd<3 where 3 = step
      {
        v_in = V1_in_array[asd];
        motor_ID = motor_id[0];
        pack_cmd();
        unpack_reply();
      }
    }
    v_in = constrain(v_in, V_MIN, V_MAX);
    if (data_rec == "UP")
    {
      Serial.println("UP!!");

      //move motor backward
      p_in = p_in + p_step;
      pack_cmd();
      unpack_reply();
    }
    if (data_rec == "DOWN")
    {
      Serial.println("Down!!");
      

      //move motor backward
      p_in = p_in - p_step;
      pack_cmd();
      unpack_reply();
    }
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
    }

  }

  if (!digitalRead(CAN0_INT))
  {
    //unpack_reply();
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
  Serial.print("  p_out = ");
  Serial.print(p_out);
  Serial.print(" v_out = ");
  Serial.print(v_out);
  Serial.print(" t_out = ");
  Serial.println(t_out);
}

unsigned int float_to_unit(float x, float x_min, float x_max, int bits) {
  /// Converts a float to an unsigned int, given range and number of bits ///
  float span = x_max - x_min;
  float offset = x_min;
  unsigned int pgg = 0;
  if (bits == 12) {
    pgg = (unsigned int) ((x - offset) * 4095.0 / span);
  }
  if (bits == 16) {
    pgg = (unsigned int) ((x - offset) * 65535.0 / span);
  }
  return pgg;
}

float uint_to_float(unsigned int x_int, float x_min, float x_max, int bits) {
  /// Converts unsigned int to float, given range and number of bits ///
  float span = x_max - x_min;
  float offset = x_min;
  float pgg = 0;
  if (bits == 12) {
    pgg = ((float)x_int) * span / 4095.0 + offset;
  }
  if (bits == 16) {
    pgg = ((float)x_int) * span / 65535.0 + offset;
  }
  return pgg;
}
// END FILE

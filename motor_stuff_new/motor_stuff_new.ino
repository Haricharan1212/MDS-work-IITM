#include <mcp_can.h>
#include <SPI.h>

int theta_2[] = {1.97464578363245, 1.96988168006514, 1.96554813211814, 1.96163885635447, 1.95812130264314, 1.95493848246096, 1.95201219202905, 1.94924743215271, 1.94653774332982, 1.94377110838885, 1.94083603160725, 1.93762738756038, 1.93405164754367, 1.9300311366141, 1.92550704782318, 1.920441037164, 1.91481533587002, 1.9086314368713, 1.90190752920255, 1.89467495750764, 1.88697406379876, 1.87884981733395, 1.87034765050019, 1.86150989180086, 1.85237312293937, 1.84296669070323, 1.83331248433768, 1.82342595643857, 1.81331823282381, 1.80299903755103, 1.79248006559212, 1.78177837789812, 1.77091937872538, 1.75993896611828, 1.74888452181917, 1.73781452051434, 1.72679668003268, 1.71590473044288, 1.70521403547824, 1.69479643834387, 1.68471481076656, 1.67501784677175, 1.66573565270091, 1.65687663895667, 1.64842611892153, 1.64034687399544, 1.63258176327468, 1.62505825851745, 1.61769458862611, 1.61040700250584, 1.60311752317504, 1.59576148464418, 1.58829412686584, 1.5806955775762, 1.57297367107956, 1.56516423429475};
int omega_2[] = {-0.497479267059036, -0.455000926126009, -0.411813937067248, -0.370586790050131, -0.333879180411704, -0.30399568642664, -0.282854695432161, -0.271881536817669, -0.271933410548049, -0.283261682374641, -0.30551455881045, -0.337780223424901, -0.378667428695705, -0.426417546645243, -0.47903945183584, -0.53445659494336, -0.590654438773263, -0.645816223267006, -0.698435871237228, -0.747398716273157, -0.792023503047983, -0.832062559287325, -0.86766087165734, -0.899278666090209, -0.927585627269069, -0.953337738021006, -0.977249574508834, -0.999875538988166, -1.0215128404483, -1.0421370629971, -1.06137804101119, -1.07853975866131, -1.09266347853794, -1.1026287151767, -1.10728246495007, -1.1055837244421, -1.09674814991996, -1.08037699970064, -1.05655539051027, -1.02590736363454, -0.989599112227903, -0.949286635537279, -0.907009607089177, -0.865038841039816, -0.825689853924388, -0.791119113991644, -0.763122193517748, -0.742953865838497, -0.731189058841782, -0.72764051839939, -0.731344268377957, -0.740617874980208, -0.753189672871516, -0.76639012561746, -0.777390047339727, -0.783465152846866};

int theta_5[] = {1.50250321573238, 1.49756158588181, 1.49325675256927, 1.48910181044615, 1.48477532673584, 1.48011411341506, 1.47509996352603, 1.46984129976143, 1.46455084620639, 1.45952054411614, 1.45509498651086, 1.45164464334046, 1.44954009069465, 1.44912834812441, 1.45071227394578, 1.45453377768078, 1.46076139133912, 1.46948250789537, 1.48070035743018, 1.49433556032882, 1.51023188344424, 1.52816563894042, 1.54785801479687, 1.56898951692078, 1.59121563951542, 1.61418286445505, 1.63754412115241, 1.66097291266171, 1.68417542627113, 1.70690009048711, 1.72894420653805, 1.75015746178805, 1.7704423147614, 1.78975141692687, 1.80808239568161, 1.82547045791531, 1.84197937746018, 1.85769149783853, 1.87269741130094, 1.88708596570001, 1.9009352039617, 1.91430476054917, 1.92723013092923, 1.93971910067921, 1.95175047858514, 1.96327513151458, 1.97421917669126, 1.98448905750267, 1.99397811946995, 2.00257421951598, 2.01016784854162, 2.01666022704453, 2.02197084657951, 2.02604397476122, 2.02885371488246, 2.03040730805473, 2.03074647975076, 2.02994675650415, 2.02811480459113, 2.02538396308181, 2.021908251464, 2.01785522077328, 2.01339808173489, 2.00870758032402, 2.00394409861598, 1.99925043689668, 1.99474568360767, 1.99052050634482, 1.98663410477186, 1.98311296100526, 1.97995141153789, 1.97711395413631, 1.9745391002502, 1.97214449459918, 1.96983295406487, 1.9674990318266, 1.96503569231748, 1.96234068884581, 1.95932226772395, 1.95590387793903, 1.95202763980193, 1.94765641445405, 1.94277441258569, 1.93738637876868, 1.93151548094637, 1.9252001167662, 1.9184899142816, 1.91144124991559, 1.90411262869035, 1.89656026937984, 1.88883421088092, 1.88097520778623, 1.87301261642459, 1.86496339231026, 1.8568322317447, 1.84861280053805, 1.84028990790294, 1.83184240967911, 1.82324656763583, 1.81447955506873, 1.80552278627934, 1.79636476022663, 1.78700314637669, 1.77744590152307, 1.76771128644323, 1.75782674559656, 1.74782671542234, 1.73774953016071, 1.72763369116587, 1.71751384920233, 1.7074169125979, 1.6973587317824, 1.6873418184905, 1.67735453329054, 1.66737211758768, 1.65735985733635, 1.64727854889594, 1.63709229815933, 1.62677852928851, 1.61633991739196, 1.60581779940261, 1.59530646874458, 1.58496763141764, 1.57504420249068, 1.56587256008911};
int omega_5[] = {-0.546402783508385, -0.452815010883361, -0.416265867080759, -0.420067546754813, -0.447926661917919, -0.484588599235505, -0.516396826999852, -0.531748411668014, -0.521432031069136, -0.478840254284314, -0.40005355162656, -0.283799148873843, -0.131293198124789, 0.0540204315541632, 0.266817346216019, 0.500305219987138, 0.746679062076532, 0.997595405022041, 1.24464177993388, 1.47977907831007, 1.6957366662501, 1.88634328356981, 2.04678065291838, 2.17375113442803, 2.26555545865113, 2.3220813124167, 2.34470809794937, 2.33613730801137, 2.30016145716014, 2.24138721531091, 2.16493018254224, 2.07609955144665, 1.98009070668405, 1.88170264597985, 1.78509505925991, 1.69359710571508, 1.60957655352612, 1.53437419353421, 1.46830452335088, 1.41071984434718, 1.36013133536301, 1.31437755927222, 1.27082838715876, 1.22661061626654, 1.17884069291152, 1.12484996136873, 1.06238872476601, 0.989797055629745, 0.906132618941156, 0.811248619114222, 0.705818175898969, 0.591304777288111, 0.469881748927064, 0.344306724492137, 0.217759722946556, 0.0936554874481727, -0.0245578955951113, -0.133601470061026, -0.230556518602385, -0.313032772688387, -0.379303800667018, -0.428401836366167, -0.460166930141275, -0.475248189863994, -0.475057850120359, -0.461681780178928, -0.437752640025287, -0.406294063094756, -0.370545857017996, -0.333781178589855, -0.299126906503931, -0.26939799939291, -0.246955525517683, -0.233596363293378, -0.230480413719482, -0.238098679911017, -0.256282917514007, -0.284254913667329, -0.320710979970187, -0.363935102417284, -0.411932511645266, -0.462574322360951, -0.51374340654083, -0.563471834792312, -0.610061025569349, -0.652177123053802, -0.688915984648605, -0.71983437058081, -0.744946340973848, -0.764686317001922, -0.779842587193361, -0.791467080819127, -0.800768849381993, -0.808999783901943, -0.817341574249684, -0.826802751477099, -0.838133851770797, -0.851767350617131, -0.867787126991099, -0.885929953170755, -0.905619016211384, -0.926026929725495, -0.946163263882072, -0.96497947781371, -0.981482437189432, -0.994846570657798, -1.00451425835438, -1.01027430922771, -1.01230938211835, -1.01120490227868, -1.00791433887539, -1.00367851704084, -0.999899782362914, -0.997975132245799, -0.999095677476168, -1.00402279450024, -1.01285387801547, -1.02479252765166, -1.03793915518694, -1.04911827285083, -1.05375805837274, -1.04583617931205, -1.01790334159785, -0.961192700658452, -0.865819281316212};

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
  float kp_in = 100.0f;
  float kd_in = 5.0f;
  float t_in = 30.0f;

  //measured values
  float p_out = 0.0f;
  float v_out = 0.0f;
  float t_out = 0.0f;

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

//    on();
  }

  void loop()
  {
    while (Serial.available() > 0)
    {
      //p_in = 0;

      String data_rec = Serial.readString();
      data_rec.trim();
      Serial.println(data_rec);
      
    if (data_rec == "OUT"){
          Serial.print("p_in = ");
          Serial.print(p_in);
          Serial.print(" v_in = ");
          Serial.print(v_in);
          Serial.print(" t_in = ");
          Serial.print(t_in);
          Serial.print(" kp_in = ");
          Serial.print(kp_in);
          Serial.print(" kd_in = ");
          Serial.print(kd_in);
          Serial.println();
        }

    if (data_rec[0] == 'P' && data_rec[1] == '=')
      {

        float y = data_rec.substring(data_rec.indexOf("P") + 2, data_rec.indexOf(";")).toFloat();
        float z = data_rec.substring(data_rec.indexOf("V") + 2, data_rec.indexOf(";")).toFloat();
        p_in = y;
        v_in = z;

        Serial.print("Moving to:  ");
        Serial.print(p_in);
        Serial.print(" with velocity:  ");
        Serial.println(v_in);

        pack_cmd();
      }


      if (data_rec == "SINTRAJ"){
        float sin[] = {0.0, 0.26, 0.5, 0.71, 0.87, 0.97, 1.0, 0.97, 0.87, 0.71, 0.5, 0.26, 0, -0.26, -0.5, -0.71, -0.87, -0.97, -1.0, -0.97, -0.87, -0.71, -0.5, -0.26};
        float cos[] = {1.0, 0.97, 0.87, 0.71, 0.5, 0.26, 0, -0.26, -0.5, -0.71, -0.87, -0.97, -1.0, -0.97, -0.87, -0.71, -0.5, -0.26, 0, 0.26, 0.5, 0.71, 0.87, 0.97};
        for (int i = 0; i <= 24 * 10; i++) {
          p_in = 1 * sin[i%24];
          v_in = 0;
          pack_cmd();
          delay(10);
          }
          p_in = 0;
          v_in = 0;
          pack_cmd();
      }

      if (data_rec == "STANCELEGTRAJ"){
      for (int i = 0; i < 56 * 10; i++) {
          p_in = -(theta_2[i%56] - 1.57);
          v_in = -omega_2[i%56];
          pack_cmd();
          delay(10);
          }
          
          pack_cmd();
      }

      if (data_rec == "TRAJ"){
      for (int j =0; j < 1; j++){
          trajectory();
          p_in = 0;
          v_in = 0;
          pack_cmd();
          delay(100);
      }

      }

      if (data_rec == "TRAJ_NEW")
      {
        Serial.println("Following trajectory");
     int times[] = {1, 14, 24, 57, 125};
     int delta[] = {1, 13, 10, 33, 68};
     int theta5[] = {-0.0675, -0.1209, -0.0010, 0.4607, -0.0041};
     int omega5[] = {-0.5464, 0.0540, 2.1738, -0.0246, -0.8658};

      for (int j =0; j < 1; j++){

      for (int i =0 ; i < 5; i++){
        p_in = theta5[i] * 2;
        v_in = omega5[i] * 0;
        pack_cmd();
        delay(delta[i] * 100);
      }

      }
      }

  

      if (data_rec == "ON")
      {
        //Enable
        on();
      }
      if (data_rec == "OFF")
      {
        //Disable
        off(); 
      }
      if (data_rec == "ZERO")  // Don't use ZERO command!
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

void on(){
    Serial.println("Turning On!!");
    EnterMotorMode();
    digitalWrite(LED2, HIGH);
    unpack_reply();
}

void off(){
      Serial.println("Turning off!!");
        ExitMotorMode();
        digitalWrite(LED2, HIGH);
        unpack_reply();
}

void trajectory(){
for (int i = 0; i < 125; i++) {
          p_in = (theta_5[i%125] - 1.57);
          v_in = omega_5[i%125];
          pack_cmd();
          delay(0.10);
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

    /// 0: [position[15-8]]
    /// 1: [position[7-0]]
    /// 2: [velocity[11-4]]
    /// 3: [velocity[3-0], kp[11-8]]
    /// 4: [kp[7-0]]
    /// 5: [kd[11-4]]
    /// 6: [kd[3-0], torque[11-8]]
    /// 7: [torque[7-0]]

    byte buf[8];
    buf[0] = 0x00;
    buf[1] = 0x00;
    buf[2] = 0x00;
    buf[3] = 0x0F;
    buf[4] = 0x02;
    buf[5] = 0x01;
    buf[6] = 0xFF;
    buf[7] = 0xFE;
    //  CAN0.sendMsgBuf(0x02, 0, 8, buf);// 0x02 id
    byte sndStat = CAN0.sendMsgBuf(motor_id[0], 0, 8, buf);
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

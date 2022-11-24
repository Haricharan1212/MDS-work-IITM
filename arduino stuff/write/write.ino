#include <SPI.h>
#include <mcp2515.h>

struct can_frame canMsg1;
struct can_frame canMsg2;
MCP2515 mcp2515(10);

void setup() {
  canMsg1.can_id  = 0x0F6;
  canMsg1.can_dlc = 8;
  canMsg1.data[0] = 1;
  canMsg1.data[1] = 2;
  canMsg1.data[2] = 3;
  canMsg1.data[3] = 4;
  canMsg1.data[4] = 5;
  canMsg1.data[5] = 6;
  canMsg1.data[6] = 7;
  canMsg1.data[7] = 8;

  canMsg2.can_id  = 0x0B1;
  canMsg2.can_dlc = 8;
  canMsg2.data[0] = 2;
  canMsg2.data[1] = 6;
  canMsg2.data[2] = 1;
  canMsg2.data[3] = 5;
  canMsg2.data[4] = 3;
  canMsg2.data[5] = 4;
  canMsg2.data[6] = 8;
  canMsg2.data[7] = 7;

  while (!Serial);
  Serial.begin(9600);
  
  mcp2515.reset();
  mcp2515.setBitrate(CAN_500KBPS);
  mcp2515.setNormalMode();
  
  Serial.println("Example: Write to CAN");
}

void loop() {
  mcp2515.sendMessage(&canMsg1);
  mcp2515.sendMessage(&canMsg2);

  Serial.println("Messages sent");
  
  delay(2000);
}

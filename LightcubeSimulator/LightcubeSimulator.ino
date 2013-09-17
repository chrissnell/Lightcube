#include <Ansiterm.h>

#include <SPI.h>         // needed for Arduino versions later than 0018
#include <Ethernet.h>
#include <EthernetUdp.h>         // UDP library from: bjoern@cs.stanford.edu 12/30/2008

Ansiterm ansi;

byte mac[] = { 0xDE, 0xAD, 0xBE, 0xEF, 0xF0, 0x0D };
  
IPAddress ip(192, 168, 17, 2);

unsigned int localPort = 7070;      // local port to listen on

// buffers for receiving and sending data
uint8_t packetBuffer[250]; //buffer to hold incoming packet,

char  ReplyBuffer[] = "acknowledged";       // a string to send back

// An EthernetUDP instance to let us send and receive packets over UDP
EthernetUDP Udp;

void setup() {
  Ethernet.begin(mac,ip);
  Udp.begin(localPort);

  Serial.begin(9600);
}

void loop() {

  int packetSize = Udp.parsePacket();
  if(packetSize) {
    Serial.print("Received packet of size ");
    Serial.println(packetSize);
    Serial.print("From ");
    IPAddress remote = Udp.remoteIP();
    for (int i =0; i < 4; i++)  {
      Serial.print(remote[i], DEC);
      if (i < 3)  {
        Serial.print(".");
      }
    }
    Serial.print(", port ");
    Serial.println(Udp.remotePort());

    Udp.read(packetBuffer,250);
    int index = 0;
   
    int cmd = 0;
    int DISP_WIDTH, DISP_HEIGHT;
    int retain_delay;
    int num_pixels;
    
    int PIXEL_DATA_OFFSET = 8;
    
    cmd = (packetBuffer[0] & 0x0F);
    
    DISP_WIDTH = packetBuffer[2];
    DISP_HEIGHT = packetBuffer[3];
    
    retain_delay = packetBuffer[4];
    
    num_pixels = DISP_WIDTH * DISP_HEIGHT * 3;
    
    int offset = PIXEL_DATA_OFFSET;
    
    ansi.eraseScreen();

    
    Serial.println("+---+---+---+---+---+---+---+---+");

    for (int row = 1; row <= DISP_HEIGHT; row++) {
        offset = DISP_WIDTH * (DISP_HEIGHT - row) * 3;
        for (int col = 0; col < DISP_WIDTH; col++) {
          

          int red = packetBuffer[PIXEL_DATA_OFFSET + offset + (col * 3)] & B10000000;
          int green = packetBuffer[PIXEL_DATA_OFFSET + offset + (col * 3) + 1] & B10000000;
          int blue = packetBuffer[PIXEL_DATA_OFFSET + offset + (col * 3) + 2] & B10000000;


          ansi.setBackgroundColor(BLACK);
          Serial.print("|");
          if ((red > 0) && (green > 0) && (blue > 0)) {
              ansi.setBackgroundColor(WHITE);
          } else if ((red > 0) && (green == 0) && (blue > 0)) {
              ansi.setBackgroundColor(MAGENTA);
          } else if ((red > 0) && (green > 0) && (blue == 0)) {
              ansi.setBackgroundColor(YELLOW);
          } else if ((red > 0) && (green == 0) && (blue == 0)) {
              ansi.setBackgroundColor(RED);
          } else if ((red == 0) && (green > 0) && (blue == 0)) {
              ansi.setBackgroundColor(GREEN);
          } else if ((red == 0) && (green == 0) && (blue > 0)) {
              ansi.setBackgroundColor(BLUE);
          } else if ((red == 0) && (green > 0) && (blue > 0)) {
              ansi.setBackgroundColor(CYAN);
          } else {
              ansi.setBackgroundColor(BLACK);
          }
          Serial.print("   ");
//          Serial.print(col);
//          Serial.print(",");
//          Serial.print(row);
          ansi.setBackgroundColor(BLACK);
        }    
        Serial.println("|");
        Serial.println("+---+---+---+---+---+---+---+---+");
      }   
    


    // send a reply, to the IP address and port that sent us the packet we received
    Udp.beginPacket(Udp.remoteIP(), Udp.remotePort());
    Udp.write(ReplyBuffer);
    Udp.endPacket();
    }
  delay(10);
 
  
}

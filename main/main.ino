//SKELETON FOR ROBOT

/*      PIN OUTS ! ! !
 *       
 *        //OUR PIN OUT! ! ! !
 LS7366 Breakout    -------------   Arduino
   -----------------                    -------
   S1                       7
   MOSI                       51
   MISO                       50
   SCLK                       52
   GND                        RAIL GND
   5V                         RAIL 5V
   I                          FLOAT
   B                          ENCODER WHITE
   A                          ENCODER YELLOW
   V                          ENCODER BLUE
   G                          ENCODER GREEN
  MOTOR S1                    TX1

    TX                           10
    RX                            11
    
 */

//DEFINES, INCLUDES ETC...
//~sabertooth
#define USBCON //uses Tx1 (see SabertoothSimplified.h)
#include <SabertoothSimplified.h>
SabertoothSimplified ST;

//~encoders
const int slaveSelectEnc1 = 7;
signed long encoder1count = 0;





void initEncoders() {
  
  // Set slave selects as outputs
  pinMode(slaveSelectEnc1, OUTPUT);
  
  // Raise select pins
  // Communication begins when you drop the individual select signsl
  digitalWrite(slaveSelectEnc1,HIGH);
  
  SPI.begin();
  
  // Initialize encoder 1
  //    Clock division factor: 0
  //    Negative index input
  //    free-running count mode
  //    x4 quatrature count mode (four counts per quadrature cycle)
  // NOTE: For more information on commands, see datasheet
  digitalWrite(slaveSelectEnc1,LOW);        // Begin SPI conversation
  SPI.transfer(0x88);                       // Write to MDR0
  SPI.transfer(0x03);                       // Configure to 4 byte mode
  digitalWrite(slaveSelectEnc1,HIGH);       // Terminate SPI conversation 
}

long readEncoder(int encoder) {
  
  // Initialize temporary variables for SPI read
  unsigned int count_1, count_2, count_3, count_4;
  long count_value;  
  
  // Read encoder 1
  if (encoder == 1) {
    digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation
    SPI.transfer(0x60);                     // Request count
    count_1 = SPI.transfer(0x00);           // Read highest order byte
    count_2 = SPI.transfer(0x00);           
    count_3 = SPI.transfer(0x00);           
    count_4 = SPI.transfer(0x00);           // Read lowest order byte
    digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation 
  }
  
  // Calculate encoder count
  count_value = (count_1 << 8) + count_2;
  count_value = (count_value << 8) + count_3;
  count_value = (count_value << 8) + count_4;
  
  return count_value;
}

void clearEncoderCount() {
    
  // Set encoder1's data register to 0
  digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation  
  // Write to DTR
  SPI.transfer(0x98);    
  // Load data
  SPI.transfer(0x00);  // Highest order byte
  SPI.transfer(0x00);           
  SPI.transfer(0x00);           
  SPI.transfer(0x00);  // lowest order byte
  digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation 
  
  delayMicroseconds(100);  // provides some breathing room between SPI conversations
  
  // Set encoder1's current data register to center
  digitalWrite(slaveSelectEnc1,LOW);      // Begin SPI conversation  
  SPI.transfer(0xE0);    
  digitalWrite(slaveSelectEnc1,HIGH);     // Terminate SPI conversation   
  
}




void setup() {
  //bluetooth setup
  Serial.begin(9600); // Serial com for data output
  serial_connection.begin(9600);

  //motor setup
  SabertoothTXPinSerial.begin(9600); // This is the baud rate you chose with the DIP switches.


  //encoder setup
  initEncoders();       Serial.println("Encoders Initialized...");  
  clearEncoderCount();  Serial.println("Encoders Cleared...");

  //servo setup
 

}

void loop() {

  //poll bluetooth read
  if (serial_connection.available())
  {


    
  }
  
  
  Serial1.write(120);
  //delay(100);
  encoder1count = readEncoder(1); 
  Serial.print("Enc1: "); Serial.println(encoder1count); 

}






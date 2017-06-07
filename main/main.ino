//MAIN V2
/*      PIN OUTS ! ! !
 *       
 *        //OUR PIN OUT! ! ! !
 LS7366 Breakout    -------------   Arduino
   -----------------                    -------
   encoder chip:
   S1                         7
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
  bluetooth:
    TX                           10
    RX                            11
   servo:                       8
    
 */
 
#define USBCON //uses Tx1 (see SabertoothSimplified.h)
#include <SabertoothSimplified.h>
#include <Servo.h>
#include "SoftwareSerial.h"
 #include <SPI.h>


SabertoothSimplified ST;

Servo servo;

//~encoders
const int slaveSelectEnc1 = 7;
signed long encoder1count = 0;
signed long fake_encoder1count = 0;

//~main
boolean motors_on = false;
boolean motors_forward = true;
int required_counts = 0;

//~bluetooth
SoftwareSerial serial_connection(10,11);
char databuff[6];
char theta[4];//This is a character buffer where the data sent by the python script will go.
char dist[3];//This is a character buffer where the data sent by the python script will go.
char inChar = -1;
int i = 0;
int counter = 1;

//struct for return distance and angle from 1 bluetooth function
struct bluetooth{
  int distance;
  int angle;
};


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



bluetooth read_from_bt(bluetooth BluetoothInstance)
{
    Serial.println("we got data");
    byte byte_count = serial_connection.available();
    int distVal;
    int thetaVal;

    // Put the data into the array
     for(i=0;i<byte_count;i++)//Handle the number of incoming bytes
    {
      //Serial.println(byte_count);
      inChar=serial_connection.read();//Read one byte
      databuff[i] = inChar;
    }
     // Serial.println("the buffer is: " + String(databuff));
      int dist_hund = databuff[0] - '0'; 
      int dist_tens = databuff[1] - '0'; 
      int dist_ones = databuff[2] - '0'; 
      int theta_hund = databuff[3] - '0'; 
      int theta_tens = databuff[4] - '0'; 
      int theta_ones = databuff[5] - '0'; 
      distVal =   (dist_hund*100 + dist_tens*10 + dist_ones) - 100;
      thetaVal =  (theta_hund*100 + theta_tens*10 + theta_ones) - 100;
      BluetoothInstance.distance = distVal;
      BluetoothInstance.angle = thetaVal;
      
      Serial.println(distVal);
      Serial.println(thetaVal);
      return BluetoothInstance;
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
  servo.attach(8);
  servo.write(90); //calibrate servo for straight direction

}

void loop() 
{
  int distance;
  struct bluetooth BluetoothInstance;

 

  //poll bluetooth read
  if (serial_connection.available())
  {
      if (counter>1)
      {
        Serial.println("NEW COMMAND IN. STOP CUNT");
        Serial1.write(64);
        clearEncoderCount();  Serial.println("Encoders Cleared...");
        encoder1count = 0;
        
      }
      Serial.println("this loop has ran: "+String(counter));
      BluetoothInstance = read_from_bt(BluetoothInstance);
      Serial.println("THE DISTANCE IS: " + String(BluetoothInstance.distance));
      Serial.println("THE ANGLE IS: " + String(BluetoothInstance.angle));

      required_counts = BluetoothInstance.distance * 3.4; //3.4 encoder counts  = 1cm (with 60mm diameter wheels)
      Serial.println("required counts is : " + String(required_counts));


      if (BluetoothInstance.angle > 180)
      {
        Serial.println("angle big boi");
        BluetoothInstance.angle = BluetoothInstance.angle - 180;
        Serial.println("THE newnewnew ANGLE IS: " + String(BluetoothInstance.angle));
        motors_forward = false;
      }
      else if (BluetoothInstance.angle < 180)
      {
         motors_forward = true;
      }
      
        servo.write(BluetoothInstance.angle);    //write to servo
        delay(400); //wait till servo finished
        
        counter = counter + 1;
        motors_on = true;

  }
  if (motors_on)
  {
    if(motors_forward == true)
    {
    Serial1.write(90);
    Serial.println("motors on and FORWARD");
    }
    else if(motors_forward == false)
    {
     Serial1.write(50);
    Serial.println("motors on and REVERSE");
    }
  
  }
  //HAVING ENCODERS IN THE ABOVE IF LOOP FUCKS SHIT UP....NO CLUE WHY...
  encoder1count = readEncoder(1); 
  fake_encoder1count = encoder1count/30;
  Serial.print("Enc1: "); Serial.println(fake_encoder1count); 
  delay(200);

  if (abs(fake_encoder1count) > required_counts)
    {
      Serial.println("REACHED DESITNATION. STOP!...cunt");
      Serial1.write(64);
      motors_on = false;
      
    }

}



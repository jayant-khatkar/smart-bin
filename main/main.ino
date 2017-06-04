//ROBOT MAIN

/*      PIN OUTS ! ! !
 *       
 external hardware ------- Arduino
   --------------------------------
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

//~~VARIBLES

//encoders
const int slaveSelectEnc1 = 7;
signed long encoder1count = 0;
const int encoder_1cm_counts = 68;


//bluetooth
SoftwareSerial serial_connection(10,11);
char databuff[6];
char theta[4];//This is a character buffer where the data sent by the python script will go.
char dist[3];//This is a character buffer where the data sent by the python script will go.
char inChar = -1;
int i = 0;
int counter = 1;

//struct for return distance and angle from bluetooth function
struct bluetooth{
  int distance;
  int angle;
};

struct bluetooth BluetoothInstance;
boolean motor_on = false;
boolean motor_forward = true;             //true for forward, false for reverse
signed long required_encoder_counts = 0;





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

 
  //poll bluetooth read
  if (serial_connection.available())
  {
     //  Serial.println("THIS LOOP HAS RAN: "+String(counter)+" TIMES"); //DEBUG

      if (motor_on) //if new command is in, stop motors immediately.
      {
        Serial1.write(64);
        motor_forward = true;
        clearEncoderCount();  Serial.println("Encoders Cleared...");  //DEBUG
      }
      
      BluetoothInstance = read_from_bt(BluetoothInstance);
    //  Serial.println("THE ANGLE IS: " + String(BluetoothInstance.angle)); //DEBUG
    //  Serial.println("THE DISTANCE IS: " + String(BluetoothInstance.distance)); //DEBUG

      if (BluetoothInstance.angle > 180)
      {
        BluetoothInstance.angle = BluetoothInstance.angle - 180;
        motor_forward = false;
      }
    
      servo.write(BluetoothInstance.angle);                                     //write to servo
      delay(400);                                                               //wait till servo finished
      required_encoder_counts =  BluetoothInstance.distance * encoder_1cm_counts;
      counter = counter + 1;  //DEBUG
      motor_on = true;

  }
  if (motor_on)
  {
    //drive motors
    if (motor_forward)
    {
      Serial1.write(127);                                                        //write to motors at FORWARD max speed
    }
    else
    {
      Serial1.write(1);                                                        //write to motors at REVERSE max speed 
    }
    
    //check encoders
    encoder1count = readEncoder(1); 
    Serial.print("Enc1: "); Serial.println(encoder1count);  //DEBUG
    delay(200);

    if (encoder1count >= required_encoder_counts)
    {
      Serial1.write(64);                                                        //write to motors to STOP
      motor_on = false;
      motor_forward = true;
      clearEncoderCount();  Serial.println("Encoders Cleared...");  //DEBUG
    } 
    
  }
  

}






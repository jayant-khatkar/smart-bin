#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10, 11);//Create a serial connection with TX and RX on these pins


#define BUFFER_SIZE 64//This will prevent buffer overruns.
char theta[4];//This is a character buffer where the data sent by the python script will go.
char dist[3];//This is a character buffer where the data sent by the python script will go.
char databuff[6];
char inChar=-1;//Initialise the first character as nothing
int count=0;//This is the number of lines sent in from the python script
int i=0;//Arduinos are not the most capable chips in the world so I just create the looping variable once
int idx = 1;

void setup()
{
  Serial.begin(9600);//Initialize communications to the serial monitor in the Arduino IDE
  serial_connection.begin(9600);//Initialize communications with the bluetooth module
 // serial_connection.println("Ready!!!");//Send something to just start comms. This will never be seen.
//  Serial.println("Started");//Tell the serial monitor that the sketch has started.
}
void loop()
{

  
//This will prevent bufferoverrun errors
//  byte byte_count=serial_connection.available();//This gets the number of bytes that were sent by the python script
  if(serial_connection.available())//If there are any bytes then deal with them
  {
  //  Serial.println("we got data");
    byte byte_count = serial_connection.available();
    int distVal;
    int thetaVal;


    // Put the data into the array
     for(i=0;i<byte_count;i++)//Handle the number of incoming bytes
    {
      inChar=serial_connection.read();//Read one byte
      databuff[i] = inChar;
//      Serial.println(inChar);
      
////      Serial.println("char val is " + String(inChar));
//      if (i <= 2)
//      {
//       dist[i] = inChar;
//      }
//      else if (i > 2)
//      {
//        theta[i - 3] = inChar;
//      }
      
    }

//    Serial.println("Hunch value is " + String(databuff));
//    Serial.println("distance value is " + String(dist));
//    Serial.println("theta value is " + String(theta));

      int dist_hund = databuff[0] - '0'; 
      int dist_tens = databuff[1] - '0'; 
      int dist_ones = databuff[2] - '0'; 
      int theta_hund = databuff[3] - '0'; 
      int theta_tens = databuff[4] - '0'; 
      int theta_ones = databuff[5] - '0'; 

      distVal =   dist_hund*100 + dist_tens*10 + dist_ones;
      thetaVal =  theta_hund*100 + theta_tens*10 + theta_ones;

      Serial.print(distVal);
      Serial.print(thetaVal);



  }

 delay(100);//Pause for a moment 

}




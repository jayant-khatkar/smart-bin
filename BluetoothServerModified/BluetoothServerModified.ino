




#include "SoftwareSerial.h"
SoftwareSerial serial_connection(10, 11);//Create a serial connection with TX and RX on these pins


#define BUFFER_SIZE 64//This will prevent buffer overruns.
char inData[BUFFER_SIZE];//This is a character buffer where the data sent by the python script will go.
char inChar=-1;//Initialise the first character as nothing
int count=0;//This is the number of lines sent in from the python script
int i=0;//Arduinos are not the most capable chips in the world so I just create the looping variable once

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
    byte byte_count = serial_connection.available();
    
     for(i=0;i<byte_count;i++)//Handle the number of incoming bytes
    {
      inChar=serial_connection.read();//Read one byte
      inData[i]=inChar;//Put it into a character string(array)
      Serial.println(inChar);
    }

   Serial.println(inData);//Print to the monitor what was detected
    //serial_connection.println("Hello from Blue "+String(count));//Then send an incrmented string back to the python script

    inData[BUFFER_SIZE] = {0};
    

//    unsigned int part1;
//    unsigned int part2;
//
//    Serial.println("now we gonna split");
//    long int n;
//    n = 123456;
//    part1 = n / 1000;
//    part2 = n - (part1 * 1000);
//    Serial.println(part1);
//    Serial.println(part2);
    
  }

  
  
 delay(100);//Pause for a moment 






  
}




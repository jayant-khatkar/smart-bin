# **This is the communications branch.  **

The code here is to test catnet wireless communcations between a PC and the robot's raspberry pi.  


- Simple command line code to initiate server (PC) client (pi) coms is:  

__client:__
sudo nc -l 2999

__server:__
sudo nc <IP address of client> 2999

- server_forever and client_forever run automated python data between 2 PCs successfully. need to try on pi

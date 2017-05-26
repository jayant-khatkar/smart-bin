# **This is the communications branch.  **

The code here is to test catnet wireless communcations between a PC and the robot's raspberry pi.  


- Simple command line code to initiate server (PC) client (pi) coms is:  

__client:__
sudo nc -l 2999

__server:__
sudo nc <IP address of client> 2999



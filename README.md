# AtBot
An Off-road robot that can fallow a particular marker (tag), it can also be controlled manually from remote location.   It is focused on low cost application so it uses ultrasonic sensor instead of Laser sensors to sense its environment  and an RGB camera to track the marker.
Clone:  1. Genric_JoyStick_ROS-game_pad :https://github.com/dil2743/Genric_JoyStick_ROS-game_pad
        2. whycon : https://github.com/dil2743/whycon
        3.AtBot   : https://github.com/dil2743/AtBot
in your workspace and Faloow this page to setup rosserial so that arduino (any controller can communicate with ros)                 http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup
After setting up all above things configure Arduino for genrating ros headerfiles by fallowing above mentioned link.

Now its time upload code in Arduino, dowload the code from https://github.com/dil2743/AtBot/tree/master/atbot_arduino.
Upload atbot_arduino.ino in arduino uno (master)
and Atbot_mega.ino in Arduino mega (slave)


             

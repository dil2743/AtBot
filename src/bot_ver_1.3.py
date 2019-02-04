#!/usr/bin/env python
import rospy
from atonomousbot.msg import atbotmsg
from atonomousbot.msg import command
bot_data = atbotmsg()
send = command()

def atbot_callback(rec_data):
        global bot_data
        bot_data = rec_data
        #print  bot_data


def send_commandToBot():
    global  send
    #print send.motion
    atbot_publisher.publish(send)
    #rospy.sleep(.01)
    send.motion.forward = False
    send.motion.backward = False
    send.motion.left = False
    send.motion.right = False
    send.motion.stop = False
    send.velocity.left_wheel = 200
    send.velocity.right_wheel = 200
    return


def sensor_reading_Front():
    global bot_data
    UF1 = bot_data.front_sensor.sensor1
    UF2 = bot_data.front_sensor.sensor2
    UF3 = bot_data.front_sensor.sensor3
    UT = bot_data.front_sensor.sensor4
    return UF1,UF2,UF3,UT

def sensor_reading_Left():
    global bot_data
    UL1 = bot_data.left_sensor.sensor1
    UL2 = bot_data.left_sensor.sensor2
    UL3 = bot_data.left_sensor.sensor3    
    return UL1,UL2,UL3

def sensor_reading_Right():
    global bot_data
    UR1 = bot_data.right_sensor.sensor1
    UR2 = bot_data.right_sensor.sensor2
    UR3 = bot_data.right_sensor.sensor3    
    return UR1,UR2,UR3    



def obstcle_avoid():
    global bot_data,send
    threshold_F1=50
    threshold_F2=50
    threshold_F3=50
    threshold_R1=40
    threshold_R2=45
    threshold_R3=45
    threshold_L1=40
    threshold_L2=45
    threshold_L3=40
    threshold_T=35
    UF1,UF2,UF3,UT = sensor_reading_Front()
    UL1,UL2,UL3 = sensor_reading_Left()
    UR1,UR2,UR3 = sensor_reading_Right()
    

    if(UF1>threshold_F1 and UF2>threshold_F2 and UF3>threshold_F3 and UT>threshold_T):
        print "no obsticle"
        send.motion.forward = True
        send_commandToBot()        
        #motion()
    elif(UL1>threshold_L1 and UL2>threshold_L2 and UL3>threshold_L3):
        send.motion.stop = True
        send_commandToBot()
        print 'left clear'
        send.motion.left = True
        send_commandToBot()
        UF1,UF2,UF3,UT = sensor_reading_Front()
        while(not (UF1>threshold_F1 and UF2>threshold_F2 and UF3>threshold_F3 and UT>threshold_T)):
            send.motion.left = True
            send_commandToBot()
            print 'left clear while'
            UF1,UF2,UF3,UT = sensor_reading_Front()
        
        send.motion.stop = True
        send_commandToBot()
    elif(UR1>threshold_R1 and UR2>threshold_R2 and UR3>threshold_R3):
        send.motion.stop = True
        send_commandToBot()
        print 'right clear'
        send.motion.right = True
        send_commandToBot()
        UF1,UF2,UF3,UT = sensor_reading_Front()
        while(not (UF1>threshold_F1 and UF2>threshold_F2 and UF3>threshold_F3 and UT>threshold_T)):
            send.motion.right = True
            send_commandToBot()
            print 'right clear while'
            UF1,UF2,UF3,UT = sensor_reading_Front()
            
        send.motion.stop = True
        send_commandToBot()
    else:
        send.motion.stop = True
        send_commandToBot()
    rospy.sleep(.01)
            
            
    

if __name__ == '__main__':
    seq = 1
    rospy.init_node('combined')
    print 'code up and running'
    try:
        atbot = 'sensor_data'
        atbot_subscriber = rospy.Subscriber(atbot,atbotmsg,atbot_callback)
        send_command_atbot = 'Atbot_data'
        atbot_publisher = rospy.Publisher(send_command_atbot, command, queue_size=1)
        #Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():
            obstcle_avoid()
            #rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
    
        
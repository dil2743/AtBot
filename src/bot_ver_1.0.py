#!/usr/bin/env python

# porting code  for arduino to minimise load:

import rospy
from geometry_msgs.msg import Pose
from sensor_msgs.msg import Joy

joy_data = Pose()
Speed = 150
maxSpeed = 255
minSpeed = 70
incSpeed = 0
decSpeed = 0
speedFactor = 5*2
motionRight = 0

def xbox_joy_callback(joy_rec):
    global joy_data,Speed
    joy_data.position.x = joy_rec.buttons[4]
    joy_data.position.y = joy_rec.buttons[5]
    joy_data.position.z = joy_rec.buttons[6]
    joy_data.orientation.x = joy_rec.buttons[0]
    joy_data.orientation.y = joy_rec.buttons[1]
    joy_data.orientation.z = joy_rec.buttons[2]
    joy_data.orientation.w = joy_rec.buttons[3]
    incSpeed = joy_data.position.x
    decSpeed = joy_data.position.z
    if (decSpeed == True):
        Speed -= speedFactor
    else:
        if (incSpeed == True):
            Speed += speedFactor
    if (Speed > maxSpeed):
        Speed = maxSpeed
    else:
        if (Speed < minSpeed):
            Speed = minSpeed    
    joy_data.position.y = Speed
    return calSpeedMotion(joy_data)
    

def calSpeedMotion(joy_data):
    ard_joy_pub = rospy.Publisher('Ard_joy_data', Pose, queue_size=1)
    ard_joy_pub.publish(joy_data)
    print joy_data

def Ard_callbaack(rec_data):
    print rec_data



if __name__ == '__main__':
    rospy.init_node('JOY_SPEED_DIRECTION')
    print 'code up and running'
    try:
        xbox_joy = '/joy'
        xbox_joy_subscriber = rospy.Subscriber(
            xbox_joy, Joy, xbox_joy_callback)
        Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():
            pass
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")

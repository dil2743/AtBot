#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import Joy

global pose_X
global pose_Y
global pose_Z
global abs_X
global abs_Y
global abs_Z
Speed = 150
check = 0.0
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 4
positive_z_th_max = 50
even_seq = 0
odd_seq = 0
seq_rec= 0
maxSpeed = 220
minSpeed = 70
incSpeed = 0
decSpeed = 0
speedFactor = 5*2
motionRight = 0
self_pose = Pose()
pose = Pose()
joy_data = Pose()
auto = 0
manual = 0

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
    auto = joy_rec.buttons[5]
    manual = joy_rec.buttons[7]

def Whycon_callback(msg):
        global seq_rec
        pose_X = msg.poses[0].position.x
        pose_Z = msg.poses[0].position.z
        seq_rec = msg.header.seq 
        return calSpeedMotion(pose_X, pose_Z , True)


def Ardu_finala_publish(joy_data):
    joy_data.position.y = Speed
    ard_joy_pub = rospy.Publisher('Ard_joy_data', Pose, queue_size=1)
    ard_joy_pub.publish(joy_data)
    print joy_data
    #reset_value()

def reset_value():
    global pose_Z
    pose_Z = 0
    print 'reset data'
    


def calSpeedMotion(pose_X, pose_Z, condition):
    #print 'control in calSpeedMotion'
    rospy.sleep(.01)
    if(pose_Z < positive_z_th_min or pose_Z > positive_z_th_max):
        pose.orientation.w = 0
        pose.orientation.x = 0
        pose.orientation.y = 0
        return #Ardu_finala_publish(pose)
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
        pose.orientation.y = 1
        pose.orientation.x = 0
        pose.orientation.w = 0
        # print pose
        # print 'Right Turn'
        # rospy.sleep(0.01)
        return #Ardu_finala_publish(pose)
    else:
        if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):
            pose.orientation.w = 1
            pose.orientation.x = 0
            pose.orientation.y = 0
            # print pose
            # print 'Left Turn'
            # rospy.sleep(0.01)
            return #Ardu_finala_publish(pose)
        else:
            if (pose_X < positive_x_th_min and pose_X > negative_x_th_max):
                pose.orientation.x = 1
                pose.orientation.y = 0
                pose.orientation.w = 0
                return #Ardu_finala_publish(pose)

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)



if __name__ == '__main__':
   
    seq = 1
    rospy.init_node('WHYCON_DIRECTION')
    print 'code up and running'
    try:
        whyconSubscriber()
        xbox_joy = '/joy'
        xbox_joy_subscriber = rospy.Subscriber(
            xbox_joy, Joy, xbox_joy_callback)
        rospy.sleep(0.05)
        #Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():  
         while(1): 
          #checking for joy stick control    
          if(
              joy_data.position.x == 1
              or joy_data.position.y ==1
              or joy_data.position.z ==1
              or joy_data.orientation.x ==1
              or joy_data.orientation.y ==1
              or joy_data.orientation.z ==1
              or joy_data.orientation.w ==1):
            break
          else:      
            if( seq %2 == 0):
                even_seq = seq_rec
            else:
                if( seq % 2 != 0):
                    odd_seq = seq_rec
            if ( even_seq == odd_seq):
                    pose.orientation.w = 0
                    pose.orientation.x = 0
                    pose.orientation.y = 0
                    Ardu_finala_publish(pose)
            else:
                Ardu_finala_publish(pose)
            rospy.sleep(0.03)
            seq += 1              
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")

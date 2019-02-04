#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseArray

pose_X = 0.0 
pose_Y =0.0
pose_Z =0.0
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 2
positive_z_th_max = 20

pose= Twist()
rospy.init_node('whycon_bot',anonymous='false')

def Whycon_callback(msg):
        pose_X = msg.poses[0].position.x
        pose_Y = msg.poses[0].position.y
        pose_Z = msg.poses[0].position.z
        #print pose_Z
        #print msg
        leftOrRight(pose_X,pose_Z)

def Ard_callbaack(data):
    print "data from arduino"
    print data
    return

def leftOrRight(pose_X, pose_Z):        
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max) and \
    (pose_Z > positive_z_th_min and pose_Z < positive_z_th_max) :
        pose.linear.y=1
        pose.linear.x = - pose_X
        pose.linear.z =   pose_Z
        #print pose
        #print 'Right Turn'
        return Ardu_publish()
    else:
        if(pose_X < negative_x_th_max and pose_X > negative_x_th_min) and \
         (pose_Z > positive_z_th_min and pose_Z < positive_z_th_max):   
            pose.linear.y=-1
            pose.linear.x = - pose_X
            pose.linear.z =   pose_Z
            #print pose
            #print 'Left Turn'
            return Ardu_publish()    
        else:
            if (pose_X < positive_x_th_min and  pose_X > negative_x_th_max) and  \
            (pose_Z > positive_z_th_min and pose_Z < positive_z_th_max):
                pose.linear.y=0
                pose.linear.x = - pose_X
                pose.linear.z =   pose_Z
                #print pose
                #print 'Forward'
                return Ardu_publish()            

def Ardu_publish():

    ard_pub = rospy.Publisher('Ard_data',Twist,queue_size=10)
    ard_pub.publish(pose)
    print pose
    #rospy.sleep(0.2)
    

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback,queue_size=10)

def Ard_subscriber():
    rospy.Subscriber('bot_feedback',Twist,Ard_callbaack,queue_size=5)

while not rospy.is_shutdown():
    whyconSubscriber()
    Ard_subscriber()
    rospy.spin()

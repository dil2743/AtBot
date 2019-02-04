#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray

pose_X = 0.0 
pose_Y =0.0
pose_Z =0.0
check=0.0
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 2
positive_z_th_max = 20

pose= Pose()
rospy.init_node('dilbot')

def Whycon_callback(msg):
        pose_X = msg.poses[0].position.x
        pose_Y = msg.poses[0].position.y
        pose_Z = msg.poses[0].position.z
        pose.orientation.x=msg.poses[0].orientation.x
        #print pose_Z
        #print msg
        leftOrRight(pose_X,pose_Z)

def Ard_callbaack(data):
    print "data from arduino"
    print data
    return

def leftOrRight(pose_X, pose_Z):
    rospy.sleep(.01)        
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
    
        pose.position.y=1
        pose.position.x = - pose_X
        pose.position.z =   pose_Z
        #print pose
        print 'Right Turn'
        #rospy.sleep(0.01)
        return Ardu_publish()
    else:
        if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):  
            pose.position.y=-1
            pose.position.x = - pose_X
            pose.position.z =   pose_Z
            #print pose
            print 'Left Turn'
            #rospy.sleep(0.01)
            return Ardu_publish()    
        else:
            if (pose_X < positive_x_th_min and  pose_X > negative_x_th_max):
                pose.position.y=0
                pose.position.x = - pose_X
                pose.position.z =   pose_Z
                #print pose
                print 'Forward'
                #rospy.sleep(0.01)
                return Ardu_publish()            

def Ardu_publish():
    ard_pub=rospy.Publisher('Ard_data',Pose)
    ard_pub.publish(pose)
    print pose
    #rospy.sleep(0.2)
    

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)

def Ard_subscriber():
    rospy.Subscriber('bot_feedback',Pose,Ard_callbaack)


while not rospy.is_shutdown():
    whyconSubscriber()
    rospy.sleep(0.05)
    Ard_subscriber()
    rospy.spin()
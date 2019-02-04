#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray

global pose_X 
global pose_Y
global pose_Z
global abs_X
global abs_Y
global abs_Z
check=0.0
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 2
positive_z_th_max = 20

self_pose= Pose()
pose = Pose()
rospy.init_node('dilbot')

def Whycon_callback(msg):
        self_pose.position.x = msg.poses[0].position.x
        self_pose.position.y = msg.poses[0].position.y
        self_pose.position.z = msg.poses[0].position.z
        self_pose.orientation.x = msg.poses[0].orientation.x
        self_pose.orientation.y = msg.poses[0].orientation.y
        self_pose.orientation.z = msg.poses[0].orientation.z
        return Ardu_publish()

def Ardu_publish():
    ard_pub=rospy.Publisher('Ard_data',Pose,queue_size=2)
    ard_pub.publish(self_pose)

def Ard_subscriber():
    rospy.Subscriber('bot_feedback',Pose,Ard_callbaack)

def Ard_callbaack(msgself):       
        abs_X = 0.0
        abs_Y = 0.0
        abs_Z = 0.0
        print msgself
        for i in range (1,2):
            abs_X += msgself.position.x
            abs_Y += msgself.position.y
            abs_Z += msgself.position.z
        abs_X = abs_X / ( msgself.position.x * 10 )
        abs_Y = abs_Y / ( msgself.position.y * 10 )
        abs_Z = abs_Z / ( msgself.position.z * 10 )
        if( abs_X == 1 and abs_Y == 1 and abs_Z == 1 ):
            pose_X = 0.0
            pose_Y = 0.0 
            pose_Z = 0.0
            print 'MARKER NOT FOUND : BOT WILL STOP AND WAIT FOR MAKER TO BE TRACKED'
            #leftOrRight(pose_X,pose_Z)
        else:
            print 'MARKER AVAILABLE '
            #leftOrRight(msgself.position.x,msgself.position.z)
                                                                                                                                                                                                          

def leftOrRight(pose_X, pose_Z):
    rospy.sleep(.01)        
    
    pose.position.x = - pose_X
    pose.position.z =   pose_Z
    
    if(pose_X == 0.0 and pose_Y == 0.0 and pose_Z == 0.0):
        pose.position.y= 5
        #print pose
        #print 'Stop'
        #rospy.sleep(0.01)
        return Ardu_final_publish()        
    else:
        if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
            pose.position.y=1        
            #print pose
            #print 'Right Turn'
            #rospy.sleep(0.01)
            return Ardu_finala_publish()
        else:
            if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):  
                pose.position.y=-1
                #print pose
                #print 'Left Turn'
                #rospy.sleep(0.01)
                return Ardu_finala_publish()    
            else:
                if (pose_X < positive_x_th_min and  pose_X > negative_x_th_max):
                    pose.position.y=0
                    #print pose
                    #print 'Forward'
                    #rospy.sleep(0.01)
                    return Ardu_finala_publish()


def Ardu_final_publish():
    self_pub=rospy.Publisher('/Ard_finala_data',Pose,queue_size=2)
    self_pub.publish(self_pose)
    #print self_pose
    #rospy.sleep(0.2)

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)


while not rospy.is_shutdown():
    #check_status()synopsis
    whyconSubscriber()
    Ard_subscriber()
    rospy.sleep(0.05)
    Ard_subscriber()
    rospy.spin()
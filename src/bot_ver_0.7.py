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

pose= Pose()
rospy.init_node('dilbot')

def Whycon_callback(msg):
        pose_X = msg.poses[0].position.x
        pose_Y = msg.poses[0].position.y
        pose_Z = msg.poses[0].position.z
        pose.orientation.x=msg.poses[0].orientation.x
        last_x = pose_X
        last_y = pose_Y
        last_z = pose_Z
        abs_X = 0.0
        abs_Y = 0.0
        abs_Z = 0.0
        for i in range (1,10):
            abs_X += pose_X
            abs_Y += pose_Y
            abs_Z += pose_Z
        pose_X = abs_X / 10 
        pose_Y = abs_Y / 10
        pose_Z = abs_Z / 10

        if(pose_X == last_x and pose_Y == last_y and pose_Z == last_z):
            pose_X = 0.0
            pose_Y = 0.0 
            pose_Z = 0.0
            leftOrRight( 0.0 , 0.0 )
        else:
            leftOrRight(pose_X,pose_Z)
                
      

    

def Ard_callbaack(data):
    return                                                                                                                                                                                                            

def leftOrRight(pose_X, pose_Z):
    rospy.sleep(.01)        
    
    pose.position.x = - pose_X
    pose.position.z =   pose_Z
    
    if(pose_X == 0.0 and pose_Y == 0.0 and pose_Z == 0.0):
        pose.position.y= 5
        #print pose
        #print 'Stop'
        #rospy.sleep(0.01)
        return Ardu_publish()        
    else:
        if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
            pose.position.y=1        
            #print pose
            #print 'Right Turn'
            #rospy.sleep(0.01)
            return Ardu_publish()
        else:
            if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):  
                pose.position.y=-1
                #print pose
                #print 'Left Turn'
                #rospy.sleep(0.01)
                return Ardu_publish()    
            else:
                if (pose_X < positive_x_th_min and  pose_X > negative_x_th_max):
                    pose.position.y=0
                    #print pose
                    #print 'Forward'
                    #rospy.sleep(0.01)
                    return Ardu_publish()



def Ardu_publish():
    ard_pub=rospy.Publisher('Ard_data',Pose,queue_size=2)
    ard_pub.publish(pose)
    print pose
    #rospy.sleep(0.2)
    

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)

def Ard_subscriber():
    rospy.Subscriber('bot_feedback',Pose,Ard_callbaack)

whyconSubscriber()

while not rospy.is_shutdown():
    #check_status()
    rospy.sleep(0.05)
    Ard_subscriber()
    rospy.spin()
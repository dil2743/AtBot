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
Speed = 150
check = 0.0
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 4
positive_z_th_max = 20

self_pose = Pose()
pose = Pose()
def Whycon_callback(msg):
        pose_X = msg.poses[0].position.x
        pose_Z = msg.poses[0].position.z
        return calSpeedMotion(pose_X, pose_Z)


def Ardu_finala_publish(joy_data):
    joy_data.position.y = Speed
    ard_joy_pub = rospy.Publisher('Ard_joy_data', Pose, queue_size=1)
    ard_joy_pub.publish(joy_data)
    print joy_data


def calSpeedMotion(pose_X, pose_Z):
    rospy.sleep(.01)
    if(pose_Z < positive_z_th_min and pose_Z > positive_z_th_max):
        pose.orientation.w = 0
        pose.orientation.x = 0
        pose.orientation.y = 0
        return Ardu_finala_publish(pose)
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
        pose.orientation.y = 1
        pose.orientation.x = 0
        pose.orientation.w = 0
        # print pose
        # print 'Right Turn'
        # rospy.sleep(0.01)
        return Ardu_finala_publish(pose)
    else:
        if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):
            pose.orientation.w = 1
            pose.orientation.x = 0
            pose.orientation.y = 0
            # print pose
            # print 'Left Turn'
            # rospy.sleep(0.01)
            return Ardu_finala_publish(pose)
        else:
            if (pose_X < positive_x_th_min and pose_X > negative_x_th_max):
                pose.orientation.x = 1
                pose.orientation.y = 0
                pose.orientation.w = 0
                return Ardu_finala_publish(pose)

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)



if __name__ == '__main__':
    rospy.init_node('WHYCON_DIRECTION')
    print 'code up and running'
    try:
        whyconSubscriber()
        rospy.sleep(0.05)
        #Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():
                    pass
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")

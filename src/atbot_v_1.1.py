#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Pose
from geometry_msgs.msg import PoseArray
from sensor_msgs.msg import Joy
from atonomousbot.msg import command

send_data = command()

global pose_X
global pose_Y
global pose_Z
global abs_X
global abs_Y
global abs_Z
Speed = 200
check = 0.0
ppositive_x_th_min = 1
positive_x_th_max = 20
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 4
positive_z_th_max = 70
even_seq = 0
odd_seq = 0
seq_rec = 0
maxSpeed = 250
minSpeed = 70
incSpeed = 0
decSpeed = 0
speedFactor = 5*2
motionRight = 0
self_pose = Pose()
pose = Pose()
joy_data = Pose()
reset_speed = 170
Stop = 0
left_offset = 0
right_offset = 5



def xbox_joy_callback(joy_rec):
    global joy_data,Speed,Stop
    joy_data.position.x = joy_rec.buttons[4]
    joy_data.position.y = joy_rec.buttons[5]
    joy_data.position.z = joy_rec.buttons[6]
    joy_data.orientation.x = joy_rec.buttons[0]
    joy_data.orientation.y = joy_rec.buttons[1]
    joy_data.orientation.z = joy_rec.buttons[2]
    joy_data.orientation.w = joy_rec.buttons[3]
    
    incSpeed = joy_data.position.x
    decSpeed = joy_data.position.z
    if(joy_rec.buttons[5] == True):
        Speed = reset_speed
    elif (decSpeed == True):
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
    Stop = joy_rec.buttons[7]
    Ardu_finala_publish(joy_data)
    #print 'speed : ',Speed

def Whycon_callback(msg):
        global seq_rec,positive_x_th_min,negative_x_th_max
        pose_X = msg.poses[0].position.x
        pose_Z = msg.poses[0].position.z
        seq_rec = msg.header.seq
        if pose_Z > 20 :
            positive_x_th_min = 0.2 * pose_Z
            negative_x_th_max = -0.2 * pose_Z
        else:    
            positive_x_th_min = 0.15 * pose_Z
            negative_x_th_max = -0.15 * pose_Z
                    
        return calSpeedMotion(pose_X, pose_Z , True,)


def Ardu_finala_publish(pose):
    global left_offset,right_offset,Speed,Stop
    send_data.velocity.left_wheel = Speed + left_offset
    send_data.velocity.right_wheel = Speed + right_offset
    send_data.motion.forward = pose.orientation.x
    send_data.motion.backward = pose.orientation.z       
    send_data.motion.left = pose.orientation.w
    send_data.motion.right = pose.orientation.y
    send_data.motion.stop = Stop
    ard_joy_pub = rospy.Publisher('Atbot_command',command, queue_size=1)
    ard_joy_pub.publish(send_data)
    #print joy_data

def reset_value():
    global pose_Z
    pose_Z = 0
    print 'reset data'
    


def calSpeedMotion(pose_X, pose_Z, condition):
    #print 'control in calSpeedMotion'
    print 'positive_x_th_min',positive_x_th_min
    print 'negative_x_th_max',negative_x_th_max
    rospy.sleep(.01)
    if(pose_Z < positive_z_th_min ):
        pose.orientation.w = 0
        pose.orientation.x = 0
        pose.orientation.y = 0
        print ' stop collision'
        #final motion is being given from main loop so : Ardu_finala_publish(pose) commented
        return #Ardu_finala_publish(pose)
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
        pose.orientation.y = 1
        pose.orientation.x = 0
        pose.orientation.w = 0
        # print pose
        print 'Right Turn'
        # rospy.sleep(0.01)
        return #Ardu_finala_publish(pose)
    else:
        if(pose_X < negative_x_th_max and pose_X > negative_x_th_min):
            pose.orientation.w = 1
            pose.orientation.x = 0
            pose.orientation.y = 0
            # print pose
            print 'Left Turn'
            # rospy.sleep(0.01)
            return #Ardu_finala_publish(pose)
        else:
            if (pose_X < positive_x_th_min and pose_X > negative_x_th_max):
                pose.orientation.x = 1
                pose.orientation.y = 0
                pose.orientation.w = 0
                print 'Forward'
                return #Ardu_finala_publish(pose)

def whyconSubscriber():
    rospy.Subscriber('/whycon/poses',PoseArray,Whycon_callback)



if __name__ == '__main__':
    seq = 1
    rospy.init_node('Master')
    print 'code up and running'
    try:
        whyconSubscriber()
        xbox_joy = '/joy'
        xbox_joy_subscriber = rospy.Subscriber(
            xbox_joy, Joy, xbox_joy_callback)
        atbot = 'feedback_atbot'
        rospy.sleep(0.05)
        #Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():  
         while not rospy.is_shutdown(): 
          #checking for joy stick control    
          if(
              joy_data.position.x == 1
              or joy_data.position.y ==1
              or joy_data.position.z ==1
              or joy_data.orientation.x ==1
              or joy_data.orientation.y ==1
              or joy_data.orientation.z ==1
              or joy_data.orientation.w ==1):
            print 'control mode : manual control'
            break
          else:
            print 'control mode : Automatic '        
            if( seq %2 == 0):
                even_seq = seq_rec
            else:
                if( seq % 2 != 0):
                    odd_seq = seq_rec
            if ( even_seq == odd_seq):
                    pose.orientation.w = 0
                    pose.orientation.x = 0
                    pose.orientation.y = 0
                    print 'marker not found'
                    Ardu_finala_publish(pose)
            else:
                Ardu_finala_publish(pose)
            rospy.sleep(0.03)
            seq += 1              
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")


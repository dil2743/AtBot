#!/usr/bin/env python
import rospy
from atonomousbot.msg import command
from geometry_msgs.msg import PoseArray  # for whycon tracing
from sensor_msgs.msg import Joy  # for joy stick

send_data = command()

forward = False
backward = False
left = False
right = False
incSpeed = False
decSpeed = False
default_speed = False
speedFactor = 10
maxSpeed = 255 #chage for offset
minSpeed = 70
default_speed_value = 180
left_offset = 0
right_offset = 0
seq_rec = 0
left_wheel_vel = 0
right_wheel_vel = 0
Speed = default_speed_value
positive_x_th_min = 1
positive_x_th_max = 8
negative_x_th_max = -1
negative_x_th_min = -20
positive_z_th_min = 4
positive_z_th_max = 50
even_seq = 0
odd_seq = 0
seq_rec= 0
global pose_X
global pose_Y
global pose_Z


def atbot_callback(data):
    #print 'Recived Feedback ATBot :'
    #print data
    return

def xbox_joy_callback(joy_rec):
    global send_data,default_speed_value,speedFactor,minSpeed,maxSpeed,left_offset,right_offset,left_wheel_vel,right_wheel_vel,Speed
    global forward,backward,left,right
    incSpeed = joy_rec.buttons[4]
    decSpeed = joy_rec.buttons[5]
    default_speed = joy_rec.buttons[6]
    forward = joy_rec.buttons[0]
    left = joy_rec.buttons[3]
    backward = joy_rec.buttons[2]
    right = joy_rec.buttons[1]
    if(default_speed == True):
            Speed = default_speed_value
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
    left_wheel_vel = Speed + left_offset
    right_wheel_vel = Speed + right_offset

def Whycon_callback(msg):
        global seq_rec
        pose_X = msg.poses[0].position.x
        pose_Z = msg.poses[0].position.z
        seq_rec = msg.header.seq 
        return calSpeedMotion(pose_X, pose_Z )

def Ardu_finala_publish(send_data):
    global left_wheel_vel,right_wheel_vel
    send_data.velocity.right_wheel = right_wheel_vel
    send_data.velocity.left_wheel = left_wheel_vel
    atbot_publisher.publish(send_data)
    rospy.sleep(0.1)
    #print joy_data

def reset_value():
    global pose_Z
    pose_Z = 0
    print 'reset data'    

def calSpeedMotion(pose_X, pose_Z):
    #print 'control in calSpeedMotion'
    rospy.sleep(.01)
    if(pose_Z < positive_z_th_min or pose_Z > positive_z_th_max):
        send_data.motion.forward = False
        send_data.motion.backward = False
        send_data.motion.left = False
        send_data.motion.right = False
        send_data.motion.stop = False
        print 'Either about to collide'
        return #Ardu_finala_publish(send_data)
    if (pose_X > positive_x_th_min and pose_X < positive_x_th_max):
        send_data.motion.forward = False
        send_data.motion.backward = False
        send_data.motion.left = False
        send_data.motion.right = True
        send_data.motion.stop = False
        print 'whycon :Right Turn'
        return #Ardu_finala_publish(send_data)
        # print pose
        # rospy.sleep(0.01)
        #return #Ardu_finala_publish(pose)
    elif(pose_X < negative_x_th_max and pose_X > negative_x_th_min):
        send_data.motion.forward = False
        send_data.motion.backward = False
        send_data.motion.left = True
        send_data.motion.right = False
        send_data.motion.stop = False
        print 'WHYCON :Left Turn'
        return #Ardu_finala_publish(send_data)
        # print pose
        # rospy.sleep(0.01)
        #return #Ardu_finala_publish(pose)
    elif (pose_X < positive_x_th_min and pose_X > negative_x_th_max):
        send_data.motion.forward = True
        send_data.motion.backward = False
        send_data.motion.left = False
        send_data.motion.right = False
        send_data.motion.stop = False
        print 'whycon Forward'
        return #Ardu_finala_publish(send_data)


if __name__ == '__main__':
   
    seq = 1
    rospy.init_node('ATBot_combined')
    print 'code up and running'
    try:
        whycon = '/whycon/poses'
        rospy.Subscriber(whycon,PoseArray,Whycon_callback)
        xbox_joy = '/joy'
        rospy.Subscriber(xbox_joy, Joy, xbox_joy_callback)
        atbot = 'feedback_atbot'
        rospy.Subscriber(atbot,command,atbot_callback)
        send_command_atbot = 'Atbot_command'
        atbot_publisher = rospy.Publisher(send_command_atbot, command, queue_size=1)
        #Ard_subscriber = rospy.Subscriber('bot_feedback', Pose, Ard_callbaack)
        while not rospy.is_shutdown():
            while not rospy.is_shutdown(): 
              if(        
                forward == True
                or left == True
                or right == True
                or backward == True
                or default_speed ==True
                or incSpeed == True
                or decSpeed == True):
                    print 'joystick control'
                    send_data.motion.forward = forward
                    send_data.motion.backward = backward
                    send_data.motion.left = left
                    send_data.motion.right = right
                    send_data.motion.stop = False
                    #Ardu_finala_publish(send_data)
                    break
              else:   
                    if( seq %2 == 0):
                        even_seq = seq_rec
                    elif( seq % 2 != 0):
                        odd_seq = seq_rec   
                    if ( even_seq == odd_seq):
                        send_data.motion.forward = False
                        send_data.motion.backward = False
                        send_data.motion.left = False
                        send_data.motion.right = False
                        send_data.motion.stop = False
                        Ardu_finala_publish(send_data)
                        print 'No marker found'
                    else:
                        #print 'Whycon Avalible : Tracking'
                        Ardu_finala_publish(send_data)
                    rospy.sleep(0.03)
                    seq += 1                          
                    #rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")
              
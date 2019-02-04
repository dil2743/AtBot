#include <ros.h>
#include <atonomousbot/command.h>

ros::NodeHandle nh;
bool set_;

#define F 9 //ML1
#define B 6 //ML0
#define L 11 //MR1
#define R 10 //MR0

#define left_vel = 0
#define right_vel = 0
#define led_pos  4
#define led_neg 2
atonomousbot::command data;
atonomousbot::command feedback;

void master_messageCb(const atonomousbot::command& rec_data){
      data = rec_data;
      feedback = rec_data;    
      digitalWrite(led_pos , HIGH-digitalRead(led_pos )^1);
}

ros::Subscriber<atonomousbot::command> master("Atbot_command",master_messageCb);//subsccriber for joystick

ros::Publisher feed_back("feedback_atbot",&feedback);

void setup(){
  nh.initNode();
  nh.subscribe(master);
  nh.advertise(feed_back);
  pinMode(F,OUTPUT);
  pinMode(B,OUTPUT);
  pinMode(L,OUTPUT);
  pinMode(R,OUTPUT);
  pinMode(led_pos,OUTPUT);
  pinMode(led_neg ,OUTPUT);
  digitalWrite(led_neg,LOW);
  }

void move_forward(){
  digitalWrite(F,HIGH);
  digitalWrite(B,LOW);
  digitalWrite(L,LOW);
  digitalWrite(R,LOW);
}

void move_left(){
  digitalWrite(F,LOW);
  digitalWrite(B,LOW);
  digitalWrite(L,HIGH);
  digitalWrite(R,LOW);
}
void move_right(){
  digitalWrite(F,LOW);
  digitalWrite(B,LOW);
  digitalWrite(L,LOW);
  digitalWrite(R,HIGH);
}

void move_backward(){
  digitalWrite(F,LOW);
  digitalWrite(B,HIGH);
  digitalWrite(L,LOW);
  digitalWrite(R,LOW);
}
void pause(){
  digitalWrite(F,LOW);
  digitalWrite(B,LOW);
  digitalWrite(L,LOW);
  digitalWrite(R,LOW);
}

void move_it(){
  if(data.motion.forward==true)
  move_forward();
  else if(data.motion.right==true)
  move_right();
  else if(data.motion.left==true)
  move_left();
  else if(data.motion.backward==true)
  move_backward();
  else
  pause();
}
void loop(){
  feed_back.publish(&feedback);
  move_it();
  nh.spinOnce();
  
}

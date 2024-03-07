#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


ros::NodeHandle nh;

Servo Servo1;
Servo Servo2;
Servo Servo3;


#define HAND1_PIN 44 
#define HAND2_PIN 45 
#define HAND3_PIN 46 

int angle1 = 90;
int angle2 = 90;
int angle3 = 90;


int Servo1max = 180;  // максимальный угол серво1 это нижняя серва в рабочку край
int Servo1min = 0;   // минимальный угол серво1

int Servo2max = 180;  // максимальный угол серво1 это нижняя серва в рабочку край
int Servo2min = 0;   // минимальный угол серво1

int Servo3max = 180;  // максимальный угол серво1 это нижняя серва в рабочку край
int Servo3min = 0;   // минимальный угол серво1




int ServoTic = 3;



void Servo_cb_1( const std_msgs::UInt16& cmd_msg) {
  Servo1.write(cmd_msg.data); //set servo angle, should be from 0-180
}


void Servo_cb_2( const std_msgs::UInt16& cmd_msg) {
  Servo2.write(cmd_msg.data); //set servo angle, should be from 0-180
}


void Servo_cb_3( const std_msgs::UInt16& cmd_msg) {
  Servo3.write(cmd_msg.data); //set servo angle, should be from 0-180
}



ros::Subscriber<std_msgs::UInt16> sub1("servo_left_right", Servo_cb_1);
ros::Subscriber<std_msgs::UInt16> sub2("servo_up_down", Servo_cb_2);
ros::Subscriber<std_msgs::UInt16> sub3("servo_magnit", Servo_cb_3);




void setup() {
 { 
  ServoHand1.attach(HAND1_PIN);
  ServoHand1.write(angle1);
}
 { 
  Servo2.attach(HAND2_PIN);
  Servo2.write(angle2);
}
 { 
  Servo3.attach(HAND3_PIN);
  Servo3.write(angle3);
}

void loop() {
  // put your main code here, to run repeatedly:

}

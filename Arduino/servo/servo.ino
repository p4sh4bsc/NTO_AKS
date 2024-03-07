#include <ros.h>



#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <std_msgs/UInt16.h>
#include <Servo.h>


ros::NodeHandle nh;

Servo Servo1; //
Servo Servo2; //
Servo Servo3; //


#define HAND1_PIN 44 //// vrode vse znach
#define HAND2_PIN 45 //// min 40 (niznya polozh) max 180 (vse good) small hueta
#define HAND3_PIN 46 //// up down min 55(verhnya gran') max 130 (nizhnya gran') bolshaya balka

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

void magnit_cb( const std_msgs::UInt16& cmd_msg) {
  digitalWrite(5, cmd_msg.data); //set servo angle, should be from 0-180
}



ros::Subscriber<std_msgs::UInt16> sub1("servo_magnit", Servo_cb_1);
ros::Subscriber<std_msgs::UInt16> sub2("servo_up_down_small", Servo_cb_2);
ros::Subscriber<std_msgs::UInt16> sub3("servo_up_down", Servo_cb_3);
ros::Subscriber<std_msgs::UInt16> sub4("magnit", magnit_cb);




void setup() {

  nh.subscribe(sub1);
  nh.subscribe(sub2);
  nh.subscribe(sub3);
  nh.subscribe(sub4);

  Servo1.attach(HAND1_PIN);
  Servo2.attach(HAND2_PIN);
  Servo3.attach(HAND3_PIN);// menshiy ugol idet v verh

  Servo1.write(90);
  Servo2.write(90);
  Servo3.write(90);// menshiy ugol idet v verh
  
  delay(1000);

}

void loop() {
  nh.spinOnce();
  delay(100);

}

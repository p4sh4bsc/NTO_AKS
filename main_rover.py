import os
import time
import math
import cv2
import serial
import rospy
from cv_bridge import CvBridge
from main_control.srv import GetCommands, GetCommandsResponse
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Bool, String, Odometry, Twist, UInt16, Int16, UInt8MultiArray
from tf.transformations import quaternion_multiply, quaternion_inverse, euler_from_quaternion

rospy.init_node('main')

global odom
odom = Odometry()
stop = Bool()

def odom_callback(data):
    global odom
    odom = data

def stop_callback(data):
    global stop
    stop = data

def format_data(raw):
    data = list()
    for i in range(raw.commands_count):
        data.append(tuple(raw.commands[i * 3:(i * 3) + 3]))
    return data, raw.commands_count


def get_degree_diff(prev_orientation, current_orientation):
        prev_q = [prev_orientation.pose.pose.orientation.x, prev_orientation.pose.pose.orientation.y, prev_orientation.pose.pose.orientation.z, prev_orientation.pose.pose.orientation.w]
        current_q = [current_orientation.pose.pose.orientation.x, current_orientation.pose.pose.orientation.y, current_orientation.pose.pose.orientation.z, current_orientation.pose.pose.orientation.w]
        delta_q = quaternion_multiply(prev_q, quaternion_inverse(current_q))
        (_, _, yaw) = euler_from_quaternion(delta_q)
        angle = math.degrees(yaw)
        
        return angle


def get_distance(start_pose, current_pose):
    return math.sqrt(math.pow(start_pose.x - current_pose.x, 2) + math.pow(start_pose.y - current_pose.y, 2))

def move_func(x,z):
    pub_vel = Twist()
    pub_vel.linear.x = x
    pub_vel.angular.z = z
    cmd_vel_pub.publish(pub_vel)

def rotate(angle, vel):
    global odom
    rospy.sleep(0.5)
    start_orientation = odom
    current_angle = abs(get_degree_diff(start_orientation, odom))
    while not rospy.is_shutdown() and not stop.data and current_angle < angle:
        current_angle = abs(get_degree_diff(start_orientation, odom)) 
        print(current_angle, angle)
        z=vel
        move_func(0, z)
    move_func(0,0)
    rospy.loginfo('rotate done!')
    rospy.sleep(0.1)

def move(dist, vel):
    global odom
    time.sleep(0.2)
    start_pose = odom
    current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
    dist += current_distance
    while not rospy.is_shutdown() and not stop.data and current_distance <= dist:
        current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
        print(current_distance,dist) 
        move_func(vel, 0) 
    rospy.sleep(0.1)
    move_func(0, 0) 
    rospy.loginfo("move done!") 
    rospy.sleep(0.1)

def start():
    command = Int16()
    command.data = 1
    led_start.publish(command)


def main():
    rospy.Subscriber("odom", Odometry, odom_callback)
    rospy.Subscriber("/stop_topic", Bool, stop_callback)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    servo_cam_pub = rospy.Publisher("/cam_servo_cmd", Int16, queue_size=10)
    servo_up_down_pub = rospy.Publisher("/payload_servo_cmd", Int16, queue_size=10)
    hc12_setting_pub = rospy.Publisher("/setting_hc12", String, queue_size=10)
    hc12_send_bytes_pub = rospy.Publisher("/hc12_send_bytes", UInt8MultiArray, queue_size=3)
    rospy.loginfo("success main init")


    rospy.wait_for_service("RadioReceiver")
    data_reader = rospy.ServiceProxy("RadioReceiver", GetCommands)
    velocity = 0.1
    hc12_string = list()
    while not rospy.is_shutdown():
        raw_data = data_reader(1)
        if raw_data.commands_count > 0:
            commands, commands_count = format_data(raw_data)
            rospy.loginfo(commands)
            for i in range(commands_count):
                # W/S
                if int(commands[i][0]) == 1 or int(commands[i][0]) == 2:
                    v = velocity * -1 if int(commands[i][0]) == 2 else velocity
                    rospy.loginfo(velocity)
                    distance = float(commands[i][1] + commands[i][2])
                    move(v, distance)

                # A/D
                elif int(commands[i][0]) == 3 or int(commands[i][0]) == 4:
                    angle = float(commands[i][1])
                    vector = 1 if commands[i][2] == 1 else -1
                    if int(commands[i][0]) == 3:
                        rotate(vector, angle, velocity, False)
                    else:
                        rotate(vector, angle, 0.05, True)
                
                elif int(commands[i][0]) == 5:
                    velocity = (float(commands[i][2]) / 100.0) * 0.3
                    rospy.loginfo(f"set vel:  {velocity}")
                
                elif int(commands[i][0]) == 6:
                    d = Int16()
                    d.data = int(commands[i][1])
                    rospy.loginfo(d)
                    servo_cam_pub.publish(d)
                    
                elif int(commands[i][0]) == 7:
                    d = Int32()
                    d.data = int(commands[i][1])
                    rospy.loginfo(d)
                    servo_up_down_pub.publish(d)

if __name__ == '__main__':
    start()
    main()
import time                                                                                   #  
import math                                                                                   #
import rospy
import os                                                                                     # <- подгружаем нужные либы 
from std_msgs.msg import Bool, String, UInt16, Int16, UInt8MultiArray                         #
from tf.transformations import quaternion_multiply, quaternion_inverse, euler_from_quaternion #
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import sys,tty,os,termios
import cv2
import paramiko
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, Image



def odom_callback(data): # получение одометрии
    global odom
    odom = data
# def servo_left_right_callback(data):
#     global angle_l_r
#     angle_l_r = data
def image_cb(img):
    global image_msg
    image_msg = img
    

def move_func(x,z): # публикуем в топик /cmd_vel переменные x,z соответсвенно для прямолинейного движения и поворота
    pub_vel = Twist()
    pub_vel.linear.x = x
    pub_vel.angular.z = z
    cmd_vel_pub.publish(pub_vel)

def get_distance(start_pose, current_pose): # фунция для возврата пройденного расстояния 
    return math.sqrt(math.pow(start_pose.x - current_pose.x, 2) + math.pow(start_pose.y - current_pose.y, 2))


def get_degree_diff(prev_orientation, current_orientation): # фунция для возврата угла, на который повернулся ровер 
        prev_q = [prev_orientation.pose.pose.orientation.x, prev_orientation.pose.pose.orientation.y, prev_orientation.pose.pose.orientation.z, prev_orientation.pose.pose.orientation.w]
        current_q = [current_orientation.pose.pose.orientation.x, current_orientation.pose.pose.orientation.y, current_orientation.pose.pose.orientation.z, current_orientation.pose.pose.orientation.w]
        delta_q = quaternion_multiply(prev_q, quaternion_inverse(current_q))
        (_, _, yaw) = euler_from_quaternion(delta_q)
        angle = math.degrees(yaw)
        
        return angle

def move(dist, vel): # функция для движения ровера на dist метров вперед/назад(зависит от знака скорости) со скоростью vel
    global odom
    rospy.sleep(0.5)
    start_pose = odom
    current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
    dist += current_distance
    while not rospy.is_shutdown() and current_distance <= dist:
        current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
        print(current_distance,dist) 
        move_func(vel, 0) 
    rospy.sleep(0.1)
    move_func(0, 0) 
    rospy.loginfo("goal achived") 
    rospy.sleep(0.1)

def rotate(angle, vel): # функция для повората ровера на angle градусов со скорость vel (направление поворота зависит от знака скорости)
    global odom
    rospy.sleep(0.5)
    start_orientation = odom
    current_angle = abs(get_degree_diff(start_orientation, odom))
    while not rospy.is_shutdown() and current_angle < angle:
        current_angle = abs(get_degree_diff(start_orientation, odom)) 
        print(current_angle, angle)
        z=vel
        move_func(0, z)
    move_func(0,0)
    rospy.loginfo('goal of the angle achived')
    rospy.sleep(0.1) 


def get_frame(count):
    frame = cvBridge.imgmsg_to_cv2(image_msg, "bgr8")
    cv2.imwrite(f'/home/pi/photo/art{count+1}.jpeg', frame)

    
    


def getkey(): # функция для чтения нажатой кнопки
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())
    try:
        while True:
            
            b = os.read(sys.stdin.fileno(), 3).decode()
            if len(b) == 3:
                k = ord(b[2])
            else:
                k = ord(b[0])
            key_mapping = {
                127: 'backspace',
                10: 'return',
                32: 'space',
                9: 'tab',
                27: 'esc',
                65: 'up',
                66: 'down',
                67: 'right',
                68: 'left'
            }
            return key_mapping.get(k, chr(k))
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


if __name__ == "__main__":
    rospy.init_node('mover', log_level=rospy.INFO)
    rospy.Subscriber("odom", Odometry, odom_callback)
    rospy.Subscriber("/front_camera/image_raw", Image, image_cb)

    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    servo_up_down_small = rospy.Publisher('/servo_up_down_small', UInt16, queue_size=10) 
    servo_up_down = rospy.Publisher('/servo_up_down', UInt16, queue_size=10)  
    servo_magnit = rospy.Publisher('/servo_magnit', UInt16, queue_size=10)  
    magnit = rospy.Publisher('/magnit', UInt16, queue_size=10)  
    # add topic for magnit servo

    while True:
        servo_up_down.publish(90)
        time.sleep(1)
        servo_up_down.publish(80)
        time.sleep(1)
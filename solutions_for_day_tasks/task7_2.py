import time                                                                                   #  
import math                                                                                   #
import rospy                                                                                  # <- подгружаем нужные либы 
from std_msgs.msg import Bool, String, UInt16, Int16, UInt8MultiArray        #
from tf.transformations import quaternion_multiply, quaternion_inverse, euler_from_quaternion #
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
import sys

def odom_callback(data): # получение одометрии
    global odom
    odom = data

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
    print(1)
    time.sleep(0.3)
    start_pose = odom
    current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
    dist += current_distance
    print(dist, current_distance)
    while not rospy.is_shutdown() and current_distance <= dist:
        current_distance = abs(get_distance(start_pose.pose.pose.position, odom.pose.pose.position))
        move_func(vel, 0) 
    time.sleep(0.1)
    move_func(0, 0) 
    time.sleep(0.1)
    rospy.loginfo("goal achived") 

def rotate(angle, vel): # функция для повората ровера на angle градусов со скорость vel (направление поворота зависит от знака скорости)
    global odom
    time.sleep(0.3)
    start_orientation = odom
    current_angle = abs(get_degree_diff(start_orientation, odom))
    while not rospy.is_shutdown() and current_angle < angle:
        current_angle = abs(get_degree_diff(start_orientation, odom)) 
        print(current_angle, angle)
        z=vel
        move_func(0, z)
    time.sleep(0.1)
    move_func(0,0)
    time.sleep(0.1)
    rospy.loginfo('goal of the angle achived')

if __name__ == "__main__":
    rospy.init_node('mover2')
    rospy.Subscriber("odom", Odometry, odom_callback)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    
    rospy.loginfo("success main init")
    

    vel = 1
    print(f"Starting rover, vel={vel} ")
    while True:
        command = str(input('Введите команду: ')) # читаем команду
        param, value = command.split() # обрабатываем строку параметр и значение, указанные через пробел

        if param == 'W':
            print('starting forward')
            move(float(value), vel) # вперед/назад
            print('done!')
        elif param == 'R': # вправо/влево
            rotate(float(value), vel)
        elif param == 'V': # установить новое значение для скорости
            vel = float(value)
            print(f'vel = {vel}')
        else:
            rospy.signal_shutdown('reason')
            sys.exit()
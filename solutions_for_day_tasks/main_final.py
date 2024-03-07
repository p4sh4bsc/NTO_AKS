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




def odom_callback(data): # получение одометрии
    global odom
    odom = data
def servo_left_right_callback(data):
    global angle_l_r
    angle_l_r = data
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
    cv2.imwrite(f'/home/pi/ssh_photos/art{count+1}.jpeg', frame)

    
    


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
    #rospy.Subscriber("servo_left_right", Odometry, odom_callback)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
    pub_serv_left_right = rospy.Publisher('servo_left_right', UInt16, queue_size=10) 
    pub_serv_up_down = rospy.Publisher('servo_up_down', UInt16, queue_size=10)  
  
    # add topic for magnit servo

    rospy.loginfo("success main init")
    
    vel = 0.2
    count_of_arts = 0
    end = False
    ip = 'xxx.xxx.xxx.xxx'
    username = 'p4sh4bsc'
    password = 'Vino04122005@&'
    ssh = paramiko.SSHClient() 
    ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
    ssh.connect(ip, username=username, password=password)
    sftp = ssh.open_sftp()

    angle_l_r = 90
    angle_u_d = 90
    while not end:
        k = getkey()
        os.system('clear')
        if k == 'esc':
            stop_it = str(input('U rly wanna stop it and send photos of arts? (Y/n): '))
            if stop_it.lower() == 'y':
                for file in os.listdir('/home/pi/ssh_photos/'):
                    sftp.put(f'/home/pi/ssh_photos/{file}', remotepath)
                end = True
            else:
                os.system('clear')
                print('press btn for moving')

        elif k=='w':
            print(f'moving forward with {vel}m/s speed')
            x=1
            z=0
        elif k=='s':
            print(f'moving backward with {vel}m/s speed')
            x=-1
            z=0
        elif k=='a':
            print(f'rotating left with {vel}m/s speed')
            z=1
            x=0
        elif k=='d':
            print(f'rotating right with {vel}m/s speed')
            z=-1
            x=0
        elif k=='=':
            print(f'making faster (vel = {vel})')
            vel+=0.1
            x=0
            z=0
        elif k=='-':
            print(f'making slower (vel = {vel})')
            vel-=0.1
            z=0
            x=0
        elif k=='p':
            get_frame()
            z=0
            x=0
        elif k=='left':
            angle_l_r -= 1
            if angle_l_r>=0:
                pub_serv_left_right.publish(angle_l_r)
            else:
                pub_serv_left_right.publish(0)
        elif k=='right':
            angle_l_r += 1
            if angle_l_r<=180:
                pub_serv_left_right.publish(angle_l_r)
            else:
                pub_serv_left_right.publish(180)
        elif k=='up':
            angle_u_d -= 1
            if angle_u_d>=0:
                pub_serv_up_down.publish(angle_u_d)
            else:
                pub_serv_up_down.publish(0)
        elif k=='down':
            angle_u_d += 1
            if angle_u_d<=180:
                pub_serv_up_down.publish(angle_u_d)
            else:
                pub_serv_up_down.publish(180)
        elif k=='m':
            pass
        else:
            x = 0
            z = 0
        
        move_func(x, z)
        if vel<0:
            vel=0.1
        time.sleep(vel)
        move_func(0,0)
        
        
        
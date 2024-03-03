import time
import math
import rospy
from std_msgs.msg import Bool, String, Odometry, Twist, UInt16, Int16, UInt8MultiArray


def odom_callback(data):
    global odom
    odom = data

def move_func(x,z):
    pub_vel = Twist()
    pub_vel.linear.x = x
    pub_vel.angular.z = z
    cmd_vel_pub.publish(pub_vel)

def get_distance(start_pose, current_pose):
    return math.sqrt(math.pow(start_pose.x - current_pose.x, 2) + math.pow(start_pose.y - current_pose.y, 2))

def move(dist, vel):
    global odom
    time.sleep(0.2)
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


if __name__ == "__main__":
    rospy.init_node('mover', log_level=rospy.INFO)
    rospy.Subscriber("odom", Odometry, odom_callback)
    cmd_vel_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)

    rospy.loginfo("success main init")
    dist, vel = map(int, str(input('Введите дистанцию и скорость через пробел: ')).split())
    move(dist = dist, vel = vel)
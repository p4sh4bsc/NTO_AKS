import rospy
import cv2
from datetime import datetime as dt
from datetime import timedelta
from ball_searcher import BallSearcher
from cv_bridge import CvBridge
from std_msgs.msg import Bool
from sensor_msgs.msg import CompressedImage
from geometry_msgs.msg import Twist


angular_speed = 0.01
linear_speed = 0.01
l_centre, r_centre = 190, 240
rospy.init_node('demo_ball_tracking')
cmd_vel = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
bp = BallSearcher()
is_auto = False
is_stop = False
image_msg = CompressedImage()
params = dict()
params1 = dict()
params_p = dict()


def image_callback(data):
    global params
    global frame
    global params1
    image_msg = data
    im = bridge.compressed_imgmsg_to_cv2(image_msg, desired_encoding='passthrough')
    mask, frame = bp.process(im)
    params1 = params
    params = bp.get_current_data()

def button_callback(data):
    global is_auto
    is_auto = data.data

def stop_cb(data):
    global is_stop
    is_stop = data.data

rospy.Subscriber("/front_camera/image_raw/compressed", CompressedImage, image_callback)
rospy.Subscriber("/button_state", Bool, button_callback)
rospy.Subscriber("/stop_topic", Bool, stop_cb)
bridge = CvBridge()

def main():
    global is_auto
    global is_stop
    global params
    global params1
    global params_p
    while not rospy.is_shutdown():
        if is_auto and not is_stop:
            if params == dict() or params == params_p:
                continue
            move_cmd = Twist()
            rospy.loginfo("Begin search ball")

            while params['obj_r'] < 10 and not rospy.is_shutdown() and not is_stop:  # params['obj_x'] == 0 and params['obj_y'] == 0 and
                params['obj_r'] == 0
                move_cmd.angular.z = angular_speed
                cmd_vel.publish(move_cmd)
                for _ in range(5):
                    cmd_vel.publish(Twist())
                rospy.loginfo("Centring ball")
                t1 = dt.now()
                while True and not rospy.is_shutdown() and not is_stop:
                    move_cmd = Twist()
                    t2 = dt.now()
                    if t2 - t1 > timedelta(seconds=1):
                        t1 = t2
                        rospy.loginfo(params)
                    if params['obj_x'] > 0 and params['obj_y'] > 0 and params['obj_r'] > 10:

                        if params['obj_x'] > r_centre:
                            move_cmd.angular.z = -angular_speed
                            if params['obj_x'] > 500:
                                move_cmd.angular.z = -angular_speed * 2

                        elif params['obj_x'] < l_centre:
                            move_cmd.angular.z = angular_speed
                            if params['obj_x'] < 140:
                                move_cmd.angular.z = angular_speed * 2
                        
                        elif l_centre <= params['obj_x'] <= r_centre:
                            break
                        cmd_vel.publish(move_cmd)

            for _ in range(5):
                cmd_vel.publish(Twist())
            rospy.loginfo("Move to ball")
            t1 = dt.now()
            while params['obj_y'] < 360 and not rospy.is_shutdown() and not is_stop:
                t2 = dt.now()
                if t2 - t1 > timedelta(seconds=1):
                    t1 = t2
                    rospy.loginfo(params)
                move_cmd = Twist()
                move_cmd.linear.x = linear_speed
                cmd_vel.publish(move_cmd)
            for _ in range(5):
                cmd_vel.publish(Twist())
            
            t1 = dt.now()
            t2 = dt.now()

            while t2 - t1 < timedelta(seconds=10) and not rospy.is_shutdown() and not is_stop:
                move_cmd = Twist()
                move_cmd.linear.x = linear_speed
                cmd_vel.publish(move_cmd)
                t2 = dt.now()
            for _ in range(5):
                cmd_vel.publish(Twist())
            rospy.loginfo("Ball was finded")
            params_p = params
            is_auto = False
        is_stop = False
    
if __name__ == "__main__":
    rospy.loginfo("ball tracking inited")
    main()
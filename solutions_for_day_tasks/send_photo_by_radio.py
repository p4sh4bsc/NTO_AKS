from std_msgs.msg import UInt16
import rospy
from main_package.srv import GetCommands, GetCommandsResponse
from std_msgs.msg import Bool
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage, Image
from geometry_msgs.msg import Pose2D
from sensor_msgs.msg import BatteryState
from std_msgs.msg import Bool, String
import serial
import struct
import time
import cv2
import zlib
import os



def bat_cb(data):
    global bat_voltage
    bat_voltage = data.voltage

def image_cb(img):
    global image_msg
    image_msg = img

def pose_cb(data):
    global pose
    pose = data


pose = Pose2D()
image_msg = Image()
ser = serial.Serial("/dev/ttyUSB0", 38400, timeout = 0.2)
ser.setDTR(False)

rospy.init_node("radio_receiver")
rospy.Subscriber("/front_camera/image_raw", Image, image_cb)
rospy.Subscriber("/odom_pose2d", Pose2D, pose_cb)




def get_frame():
    frame = cvBridge.imgmsg_to_cv2(image_msg, "bgr8")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame, (100, 100))
    compressed_img = cv2.imencode('.jpg', resized_img)[1].tobytes()
    img_len = len(compressed_img)
    rospy.loginfo(img_len)

    return compressed_img, img_len


def get_meta():
    global can_change
    global btn_state
    ret = struct.pack('3df?', pose.x, pose.y, pose.theta, bat_voltage, btn_state)

    return ret 

def main():
    global data
    global data_length
    time.sleep(1)

    while not rospy.is_shutdown():
        frame, img_len = get_frame()
        for i in range(img_len // 512):
            meta = get_meta()
            ser.write(b"BGN" + frame[512*i:512*(i+1)] + b"META"+ meta + b"END")
        ost = img_len % 512
        if ost != 0:
            ser.write(b"BGN" + frame[-ost:] + b"META" + meta + b"END")

        

if __name__ == "__main__":
    main()
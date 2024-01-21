import os
import time
import math
import cv2
import serial
import rospy
from cv_bridge import CvBridge
from main_control.srv import GetCommands, GetCommandsResponse
from sensor_msgs.msg import CompressedImage, Image
from std_msgs.msg import Bool



def image_callback(data):
    global image_msg
    image_msg = data
    
radio = serial.Serial(port='', baudrate='', timeout=2)
radio.setDTR(False)

image_msg = CompressedImage()
cvBridge = CvBridge()

rospy.init_node('protocol_tranceiver')
rospy.Subscribe('front_camera/image_raw/compressed', CompressedImage, image_callback)
rospy.loginfo('radio ready!')



def handle_radio_receiver(request):
    response = GetCommandsResponse()
    response.commands = data
    response.commands_count = len_of_data
    data = list()
    len_of_data = 0

    return response

def read_answer():
    trash = radio.read_until(b'BGN')
    usefull_data = radio.read_until(b'END')
    commadns = usefull_data
    data.extend(commadns)
    len_of_data += len(commadns)

def get_img():
    cv_image = cvBridge.compressed_imgsg_to_cv2(image_msg, desired_encoding='passthrough')
    image = cv2.resize(cv_image, (120, 120))
    compressed_img = cv2.imencode('.jpg', image)[1].tobytes()
    img_len = len(compressed_img)

    return compressed_img, img_len






def main():
    global data
    global len_of_data
    radio_service = rospy.Service("RadioReciever", GetCommands, handle_radio_receiver)

    while not rospy.is_shutdown():
        img, img_len = get_img()

        for packet in range(img_len//512):
            radio.write(b'BGN' + img[512*packet:512*(packet+1)] + b'END')
            read_answer()

        if img_len%512 != 0:
            radio.write(b'BGN' + img[-1*(img_len%512):] + b'END')
            read_answer()

if __name__ == "__main__":
    main()
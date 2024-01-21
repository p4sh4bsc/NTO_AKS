import serial
#import rospy
import os
import cv2
import time
#from cv_bridge import CvBridge

#cvBridge = CvBridge()

def get_photo():
    #frame = cvBridge.imgmsg_to_cv2(image_msg, "bgr8")    TODO: download ros_pkg
    camera = cv2.VideoCapture(0)
    time.sleep(0.3)
    return_value, frame = camera.read()
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    resized_img = cv2.resize(frame_gray, (100, 100))
    compressed_img = cv2.imencode('.jpg', resized_img)[1]

    cv2.imwrite('photo_orig.png', frame)
    cv2.imwrite('photo_compresed.jpg', compressed_img)

    img_len = len(compressed_img)
    #rospy.loginfo(img_len)
    #return compressed_img, img_len

def main():
    # TODO: get photo
    #       create packets (512byts) for photo
    pass
if __name__ == "__main__":
    get_photo()
    #main()
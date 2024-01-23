# import rospy
#import asyncio
import cv2
import time
from datetime import datetime as dt
from datetime import timedelta
from ball_searcher import BallSearcher
# from cv_bridge import CvBridge
# from std_msgs.msg import Bool
# from sensor_msgs.msg import CompressedImage
# from geometry_msgs.msg import Twist


angular_speed = 0.01
linear_speed = 0.01
l_centre, r_centre = 320, 960
bp = BallSearcher()
is_auto = True
is_stop = False

params = dict()
params1 = dict()
params_p = dict()
global video

def image_callback(video):
    global params
    global frame
    global params1
    #video = cv2.VideoCapture(0)
    time.sleep(0.1)
    status, im = video.read()
    cv2.imwrite('.jpg', im)
    mask, frame = bp.process(im)
    cv2.imwrite('mask.jpg', frame)
    params1 = params
    params = bp.get_current_data()

def button_callback(data):
    global is_auto
    is_auto = data.data

def stop_cb(data):
    global is_stop
    is_stop = data.data


def main(video):
    global is_auto
    global is_stop
    global params
    global params1
    global params_p
    stop_it = False
    while True:
        image_callback(video)
        if is_auto and not is_stop:
            if params == dict() or params == params_p:
                continue
            
            print("Begin search ball")
            


            while params['obj_r'] < 160 and not is_stop:  # params['obj_x'] == 0 and params['obj_y'] == 0 and
                image_callback(video)
                #params['obj_r'] == 0
                for _ in range(5):
                    print('!!! rotating !!!')
                print("Centring ball")
                t1 = dt.now()
                while not stop_it and not is_stop:
                    image_callback(video) 
                    t2 = dt.now()
                    if t2 - t1 > timedelta(seconds=1):
                        t1 = t2
                        print(params)
                    if params['obj_x'] > 0 and params['obj_y'] > 0 and params['obj_r'] > 10:

                        if l_centre+300 <= params['obj_x'] <= r_centre-300:
                            print('!!! EXTRA STOP !!!')
                            stop_it = True
                            break
                        else:       

                            if params['obj_x'] > r_centre:
                                print('!!! reverse rotating !!!')
                                if params['obj_x'] > 500:
                                    print('!!! rotating left !!!')

                            elif params['obj_x'] < l_centre:
                                print('!!! rotating !!!')
                                if params['obj_x'] < 140:
                                    print('!!! rotsting right !!!')
                        

                        
            image_callback(video)
            print("Move to ball")
            t1 = dt.now()
            while params['obj_y'] < 360  and not is_stop:
                image_callback(video)
                t2 = dt.now()
                if t2 - t1 > timedelta(seconds=1):
                    t1 = t2

                print('!!! moving forward first !!!', params)
            
            t1 = dt.now()
            t2 = dt.now()

            while t2 - t1 < timedelta(seconds=10) and not is_stop:
                image_callback(video)
                print('!!! moving forward !!!', params)
                t2 = dt.now()
            print("Ball was finded")
            params_p = params
            is_auto = False
        is_stop = False
    
# async def start():
#     await asyncio.gather(image_callback(), main())
if __name__ == "__main__":
    print("ball tracking inited")
    video = cv2.VideoCapture(0)
    time.sleep(0.5)
    main(video)
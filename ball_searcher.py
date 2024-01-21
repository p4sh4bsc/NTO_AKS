import cv2
import numpy as np

class BallSearcher:
    def __init__(self):
        self.yellowLower = (14, 180, 200)# dark
        self.yellowUpper = (34, 255, 255) # light
        self.font                   = cv2.FONT_HERSHEY_SIMPLEX
        self.bottomLeftCornerOfText = (30,50)
        self.fontScale = 0.5
        self.fontColor = (255,255,255)
        self.lineType = 1
        self.current_data = {"obj_x":0,"obj_y":0, "obj_r":0}
        
        
        
    def process(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.yellowLower, self.yellowUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
        center = None
        self.current_data = {"obj_x":0,"obj_y":0, "obj_r":0}
        if len(cnts) > 0:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        else:
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        if radius > 10:
            self.current_data = {"obj_x": int(x),"obj_y": int(y), "obj_r": int(radius)}
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
        cv2.putText(frame,"({:d},{:d},{:d})".format(int(x),int(y),int(radius)), (int(x), int(y)), self.font, self.fontScale, self.fontColor, self.lineType)
        
        return mask, frame
    
    def get_current_data(self):
        return self.current_data
    
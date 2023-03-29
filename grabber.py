
import cv2
import win32api, win32con, win32ui, win32gui
import numpy as np
import threading
import time
import random
import dxcam
from win32api import GetSystemMetrics


import clr
# change this to wherever your built DLL is
clr.AddReference('CHANGE THIS TO THE REST OF THE PATH OF YOUR DIRECTORY\\DLL\\ClassLibrary1\\ClassLibrary1.dll')
from ClassLibrary1 import Class1
ud_mouse = Class1()
ud_mouse.Run_Me()





class Grabber:
    def __init__(self, x_multiplier, y_multiplier, y_difference) -> None:
        self.lower = np.array([139, 95, 154], np.uint8)
        self.upper = np.array([153, 255, 255], np.uint8)
        self.x_multiplier = x_multiplier         # multiplier on x-coordinate
        self.y_multiplier = y_multiplier         # multiplier on y-coordinate
        self.y_difference = y_difference         # the amount of pixels added to the y-coordinate (aims higher)

    def build_title(self, length) -> str:
        """return a randomly generated window title to prevent detections"""
        chars = [
            'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
            'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
            'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
            'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '!', '@', '#',
            '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+', '/', '?'
        ]
        return ''.join(random.choice(chars) for character in range(length))
 
    def find_dimensions(self, box_size): 
        """Calculates constants required for the bot."""
        self.box_size = box_size
        self.box_middle = int(self.box_size / 2) 
        self.y = int(((GetSystemMetrics(1)   / 2) - (self.box_size / 2))) 
        self.x = int(((GetSystemMetrics(0) / 2) - (self.box_size / 2))) 

        

    def process_frame(self, frame):
        """Performs operations on a frame to improve contour detection."""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        processed = cv2.inRange(hsv, self.lower, self.upper)

        processed = cv2.morphologyEx(processed, cv2.MORPH_CLOSE, np.ones((10, 10), np.uint8))
        dilatation_size = 15
        # dilation_shape = cv2.MORPH_RECT
        # dilation_shape = cv2.MORPH_ELLIPSE
        dilation_shape = cv2.MORPH_CROSS
        element = cv2.getStructuringElement(dilation_shape, (2 * dilatation_size + 1, 2 * dilatation_size + 1),
                                    (dilatation_size, dilatation_size))
        processed = cv2.dilate(processed, element)
        processed = cv2.blur(processed, (8, 8))        
        return processed

    def detect_contours(self, frame, minimum_size):
        """Returns contours larger then a specified size in a frame."""
        contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large_contours = []
        if len(contours) != 0:
            for i in contours:
                if ud_mouse.Check(cv2.contourArea(i), minimum_size):
                   if cv2.contourArea(i) > minimum_size:
                       large_contours.append(i)
        return large_contours

    def scale_contour(self,cnt, scale:float):
        M = cv2.moments(cnt)
        x = int(M['m10']/M['m00'])
        y = int(M['m01']/M['m00'])

        center = cnt - [x, y]
        cnt_scaled = center * scale
        cnt_scaled = cnt_scaled + [x, y]
        cnt_scaled = cnt_scaled.astype(np.int32)

        return cnt_scaled

    def on_target(self, contour, hitbox):
        for c in contour:
            cont = self.scale_contour(c, hitbox)
            test = cv2.pointPolygonTest(cont,( self.box_middle, self.box_middle),False)
            if test >= 0:
                return True
        return False

    def compute_centroid(self, contour):
        """Returns x- and y- coordinates of the center of the largest contour."""
        self.contour = contour
        c = max(contour, key=cv2.contourArea)
        rectangle = np.int0(cv2.boxPoints(cv2.minAreaRect(c)))
        new_box = []
        for point in rectangle:
            point_x = point[0]
            point_y = point[1]
            new_box.append([round(point_x, -1), round(point_y, -1)])
        M = cv2.moments(np.array(new_box))
        if M['m00']:
            center_x = (M['m10'] / M['m00'])
            center_y = (M['m01'] / M['m00'])
            x = -(self.box_middle - center_x)
            y = -(self.box_middle - center_y)
            self.cx = x
            self.cy = y
            return [], x, y



    def is_activated(self, key_code) -> bool:
        return ud_mouse.is_activated(key_code)

    def move_mouse(self, x, y):
       threading.Thread(target=self._move_mouse, args=[x, y, self.x_multiplier, self.y_multiplier, self.y_difference]).start()

    def _move_mouse(self, x, y, x_multiplier, y_multiplier, y_difference):
        ud_mouse.move_mouse(x, y, self.box_size, x_multiplier, y_multiplier, y_difference)

    def mouse_right(self):
        threading.Thread(target= self._mouse_right).start()

    def _mouse_right(self):
        ud_mouse.rclick_mouse()        

    def click(self):
        threading.Thread(target=self._click).start()

    def trigger(self):
        threading.Thread(target=self._click).start()

    def _click(self):        
        ud_mouse.click_mouse()



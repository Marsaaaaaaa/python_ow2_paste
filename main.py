
from grabber import *
import time
from os import system
import math
import win32gui
import win32con
import os
import cv2
import threading
#from settings import *
#from predict import *
#from overlay import *

# fov, over 290 will break shit, 
fov = 160
# lower to get more fps but worse performance
fps = 72
# list of virtual keys: https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes
# default = mouse1
aim_key = 0x01

# default = v
trigger_key = 0x12

hitbox_size = 0.6


# DO NOT SET THIS TO 0 YOU LL HAVE MASSIVE FRAME DROPS
sleep = 1

magnet_accel = 1.2

right_click_key = 0x12
right_click_magnet = True

shift_key = 0
shift_magnet = False

E_key = None
E_magnet = False

grabber = Grabber(
    # x and y accel. higher = faster
    x_multiplier = 0.60,
    y_multiplier = 0.14,
    # idk this shit is supposed to set the height of where u aim but I think its broken
    y_difference = 6,
    trigger_sleep = sleep

)


#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################

#obj_flow = Prediction()
#prediction.screen_size(fov)

left, top = (1920 - fov) // 2, (1080 - fov) // 2
right, bottom = left + fov, top + fov
region = (left, top, right, bottom)
time.sleep(1)
camera = dxcam.create(region=region, output_color="BGR")
camera.start(target_fps=fps)


grabber.find_dimensions(fov)
random_title = grabber.build_title(20)
system('title ' + f"'{random_title}'")
system('cls')

print(f'box_size = {grabber.box_size}')
print(f'random_title = {random_title}')
print(f"x accel = {grabber.x_multiplier}")
print(f"y accel = {grabber.y_multiplier}")

#################################################################################################


Dababy = True
PID = os.getpid()
count = 0

while True:
        
    og = np.array(camera.get_latest_frame())
    if grabber.is_activated(aim_key):
        frame = grabber.process_frame(og)
        contours = grabber.detect_contours(frame, 100)
        if contours:
            rec, x, y = grabber.compute_centroid(contours)

            grabber.move_mouse(x, y)
    
    if grabber.is_activated(trigger_key):
        frame = grabber.process_frame(og)
        contours = grabber.detect_contours(frame, 100)
        if contours:            
            if grabber.on_target(contours, hitbox_size):
                grabber.trigger()

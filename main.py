from grabber import *
import time
from os import system
import math
import win32gui
import win32con
import os
import cv2
import threading
#from predict import *
#from overlay import *

# fov, over 290 will break shit, 
fov = 160
# lower to get more fps but worse performance
fps = 144

# list of virtual keys: https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes

# default = mouse1
aim_key = 0x01

#shoots if enemies are detected inside the crosshair
trigger_key = 0x39


# hitbox size for the triggerbots
hitbox_size = 0.6

# sleep for the triggerbots
sleep = 0

# aim assist on the triggerbot
trigger_magnet = True

# speed of the aim assist on triggerbot (x_multiplies*magnet_accel, y_multiplies*(magnet_accel/2))
magnet_accel = 2

# triggerbot and magnet settings for different abilities
right_click_key = 0x56
right_click_magnet = True

shift_key = 0
shift_magnet = False


E_key = 0
E_magnet = False

grabber = Grabber(
    # x and y accel. higher = faster
    x_multiplier = 0.22,
    y_multiplier = 0.08,
    # delta of the y axis, change this in order to shoot higher/ lower
    y_difference = 6,
   
    trigger_sleep = sleep

)


#################################################################################################

#obj_flow = Prediction()
#prediction.screen_size(fov)

# creates a camera of the specified size (fov = 150 then camera will be 150x150 pixels)
left, top = (1920 - fov) // 2, (1080 - fov) // 2
right, bottom = left + fov, top + fov
region = (left, top, right, bottom)
time.sleep(1)
camera = dxcam.create(region=region, output_color="BGR", max_buffer_len=60)
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


# main loop, processes new frames, if enemies are detected listens to hotkeys 
# to perform related features
while True:

    og = np.array(camera.get_latest_frame())
    frame = grabber.process_frame(og)
    contours = grabber.detect_contours(frame, 900)

    if contours:
        rec, x, y = grabber.compute_centroid(contours)
        if grabber.is_activated(aim_key):
            grabber.move_mouse(x, y)


        if grabber.is_activated(trigger_key):
              if trigger_magnet:
                 grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
              if grabber.on_target(contours, hitbox_size):
                 grabber.trigger()


        if grabber.is_activated(shift_key):
           if shift_magnet:
               grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
               if grabber.on_target(contours, hitbox_size):
                   grabber.shift()


        if grabber.is_activated(E_key):
           if shift_magnet:
              grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
               
              if grabber.on_target(contours, hitbox_size):
                   grabber.E()

     
        if grabber.is_activated(right_click_key):
           if right_click_magnet:
               grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
               if grabber.on_target(contours, hitbox_size):
                  grabber.mouse_right()

        



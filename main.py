
from grabber import *
import time
from os import system
import math
from win32api import GetSystemMetrics
import os
import cv2
import threading


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


grabber = Grabber(
    # x and y accel. higher = faster
    x_multiplier = 0.60,
    y_multiplier = 0.14,
    # idk this shit is supposed to set the height of where u aim but I think its broken
    y_difference = 6,
)



#################################################################################################

left, top = (GetSystemMetrics(0) - fov) // 2, (GetSystemMetrics(1) - fov) // 2
right, bottom = left + fov, top + fov
region = (left, top, right, bottom)


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



while True:       
    og = np.array(camera.get_latest_frame())
    frame = grabber.process_frame(og)
    contours = grabber.detect_contours(frame, 100)
    if grabber.is_activated(aim_key) and contours:
        rec, x, y = grabber.compute_centroid(contours)
        grabber.move_mouse(x, y)
    
    if grabber.is_activated(trigger_key) and contours:
        if grabber.on_target(contours, hitbox_size):
            grabber.trigger()

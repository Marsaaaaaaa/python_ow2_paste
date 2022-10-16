
from grabber import *
import time
from os import system
import math
import win32gui
import win32con
import os
import cv2
 

# fov, over 290 will break shit, 
fov = 150
# lower to get more fps but worse performance
fps = 160
# list of virtual keys: https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes
# default = mouse1
aim_key = 0x01

# default = alt
flick_key = 0x12

# default = v
trigger_key = 0x56

hitbox_size = 0.6
flick_hitbox_scale = 1
trigger_sleep = 0.1


grabber = Grabber(
    # x and y accel. higher = faster
    x_multiplier = 0.2,
    y_multiplier = 0.08,
    # idk this shit is supposed to set the height of where u aim but I think its broken
    y_difference = 5,
    # flick speed multiplier ( flick speed = x_multiplier*flick_speed)
    flick_speed = 5.5
)

#closes the cheat
kill_switch = 0x2E



#################################################################################################
#################################################################################################
#################################################################################################
#################################################################################################


left, top = (1920 - fov) // 2, (1080 - fov) // 2
right, bottom = left + fov, top + fov
region = (left, top, right, bottom)
camera = dxcam.create(region=region, output_color="RGB", max_buffer_len=512)
camera.start(target_fps=fps)


grabber.find_dimensions(fov)
random_title = grabber.build_title(20)
system('title ' + f"'{random_title}'")
system('cls')

print(f'box_size = {grabber.box_size}')
print(f'random_title = {random_title}')
print(f"x accel = {grabber.x_multiplier}")
print(f"y accel = {grabber.y_multiplier}")
print(f"flick speed = {grabber.flick_speed}")


Dababy = True
PID = os.getpid()
 

while True:

    if grabber.is_activated(kill_switch):
        os.kill(PID)               

    last_time = time.time()
    count = 0
    og = np.array(camera.get_latest_frame())
    frame = grabber.process_frame(og)
    contours = grabber.detect_contours(frame, 100)
    if contours:
        rec, x, y = grabber.compute_centroid(contours)
        if grabber.is_activated(aim_key):
            grabber.move_mouse(x, y)

        if grabber.is_activated(flick_key):
                grabber.flick_mouse(x , y)            
                if  grabber.on_target(contours, hitbox_size*flick_hitbox_scale):
                    grabber.trigger()
                    time.sleep(trigger_sleep)




        if grabber.is_activated(trigger_key) and grabber.on_target(contours, hitbox_size):
                     time.sleep(trigger_sleep)
                     grabber.trigger()
                     time.sleep(trigger_sleep)

    




# uncomment these lines to show conturs and the screen.
# note: this has a performance impact in my testing.


        cv2.drawContours(og, contours, -1, (0, 0, 0), 4)
        if rec:
            cv2.drawContours(og, rec, -1, (0, 255, 0), 4)
    cv2.imshow('frame', og)
    if (cv2.waitKey(1) & 0x2D) == ord('q'):
        cv2.destroyAllWindows()
        exit()





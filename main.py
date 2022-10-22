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
fps = 200
# list of virtual keys: https://learn.microsoft.com/windows/win32/inputdev/virtual-key-codes
# default = mouse1
aim_key = 0x01

# default = alt
flick_key = 0x12

# default = v
trigger_key = 0x39

show_capture = True

hitbox_size = 0.6
flick_hitbox_scale = 1
abilities_hitbox_scale = 0.8
# DO NOT SET THIS TO 0 YOU LL HAVE MASSIVE FRAME DROPS
sleep = 1

trigger_magnet = True

magnet_accel = 2

right_click_key = 0x56
right_click_magnet = True

shift_key = None
shift_magnet = False

Q_key = None
Q_magnet = False

E_key = None
E_magnet = False

grabber = Grabber(
    # x and y accel. higher = faster
    x_multiplier = 0.22,
    y_multiplier = 0.08,
    # idk this shit is supposed to set the height of where u aim but I think its broken
    y_difference = 6,
    # flick speed multiplier ( flick speed = x_multiplier*flick_speed)
    flick_speed = 5.5,
    # DO NOT SET THIS TO 0 YOU LL HAVE MASSIVE FRAME DROPS
    trigger_sleep = sleep

)

#closes the cheat
kill_switch = 0x2E



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
camera = dxcam.create(region=region, output_color="BGR", max_buffer_len=144)
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

#################################################################################################


Dababy = True
PID = os.getpid()
#fps = 0
#start = time.time()
while True:

    og = np.array(camera.get_latest_frame())
    if og is not None:
        #fps += 1
        frame = grabber.process_frame(og)
        contours = grabber.detect_contours(frame, 900)

    if contours:
        rec, x, y = grabber.compute_centroid(contours)
        if grabber.is_activated(aim_key):
            grabber.move_mouse(x, y)


        if flick_key is not None:
            if grabber.is_activated(flick_key):
               grabber.flick_mouse(x , y)            
               if  grabber.on_target(contours, hitbox_size*flick_hitbox_scale):
                   grabber.trigger()



        if trigger_key is not None:
            if grabber.is_activated(trigger_key):
                if trigger_magnet:
                    grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
                if grabber.on_target(contours, hitbox_size):
                    grabber.trigger()


        if shift_key is not None:
            if grabber.is_activated(shift_key):
                if shift_magnet:
                    grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
                if grabber.on_target(contours, hitbox_size*abilities_hitbox_scale):
                    grabber.shift()



        if Q_key is not None:       
            if grabber.is_activated(Q_key):
                if Q_magnet:
                    grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
                if grabber.on_target(contours, hitbox_size*abilities_hitbox_scale):
                   grabber.Q()




        if E_key is not None:        
            if grabber.is_activated(E_key):
                if shift_magnet:
                   grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
                if grabber.on_target(contours, hitbox_size*abilities_hitbox_scale):
                   grabber.E()





        if right_click_key is not None:        
            if grabber.is_activated(right_click_key):
                if right_click_magnet:
                    grabber.move_mouse(x*magnet_accel, y*(magnet_accel/2))
                if grabber.on_target(contours, hitbox_size*abilities_hitbox_scale):
                    grabber.mouse_right()


        cv2.drawContours(og, contours, -1, (0, 0, 0), 4)
        if rec:
            cv2.drawContours(og, rec, -1, (0, 255, 0), 4)


    if show_capture:
        cv2.imshow('frame', og)
        if (cv2.waitKey(1) & 0x2D) == ord('q'):
            cv2.destroyAllWindows()
            exit()


    if grabber.is_activated(kill_switch):
        camera.stop()
        os.kill(PID) 
        



# record_dataset.py
# captures screen images and gamepad input from cv2.VideoCapture
# Usage:
#   Plug in a wheel,
#   launch a game,
#   set up virtual webcam app(e.g. SCFH DSF) to feed screen to this.
#   Then, run this script.

# While script is running,
#   Press button 3 to start recording.
#   Press button 2 to stop. To change this settings, modify main loop.

# Screen recording will be saved to saved_dataset/*.jpg.
# Controller input will be saved to saved_dataset/data.txt and dataplus.txt.
# create saved_dataset directory before running.

import scipy.misc
import model
import cv2
import time
import os
import threading
import logging
import queue
import signal
import sys
import pygame
from subprocess import call

# objects and numbers

cap = cv2.VideoCapture(1)
#TODO: above line contains a magic number
# change above line to suit your PC

smoothed_angle = 0
wheel = 0
acc = 0
brake = 0
i = 0
accumulated_brake = 0
capture_enable = False
start_time = (int(time.time()))
input_queue = queue.Queue()
image_queue = queue.Queue()
clock = pygame.time.Clock()
shutdown_signal = False

ret, last_image = cap.read()

# functions
def capture_image(filename):
    global last_image
    ret, frame = cap.read()
    #image = scipy.misc.imresize(frame, [66, 200]) / 255.0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = (filename, frame)
    image_queue.put(image)
    last_image = frame

def store_image():
    while(shutdown_signal == False):
        while(image_queue.empty != True):
            image = image_queue.get()
            scipy.misc.imsave("saved_dataset/" + image[0], image[1])
            #cv2.imshow("frame", cv2.cvtColor(image[1], cv2.COLOR_RGB2BGR))

def store_driving_data():
    with open("saved_dataset\dataplus.txt", "a") as dataplus, open("saved_dataset\data.txt", "a") as data:
        while(shutdown_signal == False):
            while(input_queue.empty() != True):
                vals = input_queue.get()
                print(vals[0], vals[1], vals[2], vals[3], file=dataplus)
                print(vals[0], vals[1],file=data)
                data.flush()
                dataplus.flush()
        data.flush()
        dataplus.flush()

def signal_handler(signal, frame):
    global shutdown_signal
    global cap
    shutdown_signal = True
    capture_enable = False
    print("SIGINT received")
    cap.release()
    cv2.destroyAllWindows()
    #pygame.quit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

pygame.init()
joystick = pygame.joystick.Joystick(0)
# TODO: above line contains magic number
# change above line to suit your PC
joystick.init()
# init
print(str(joystick.get_name()))
print(str(joystick.get_numaxes()))

# main loop
while(True):
    pygame.event.pump()
    filename = str(str(start_time) + "." + str(i) + ".jpg")
    for event in pygame.event.get(): # event handling loop
        if event.type == pygame.JOYAXISMOTION:
            # TODO: this code only works for steering with Xbox 360/One peripherals
            # e.g. "Ferrari 458 Italia Racing Wheel for Xbox 360" I wrote this for
            # use following if needed
            # http://www.pygame.org/project-Windows+Xbox+360+Controller+for+pygame-2945-.html
            axis = event.dict['axis']
            value = event.dict['value']
            if (axis == 0):
                wheel = (value * 450)
            if (axis == 1):
                if value < 0:
                    acc = 0
                    brake = (-1) * value
                else:
                    acc = value
                    brake = 0
        if event.type == pygame.JOYBUTTONUP:
                button = event.button
                if (button == 3 and capture_enable == False):
                    with image_queue.mutex, input_queue.mutex:
                        image_queue.queue.clear()
                        input_queue.queue.clear()
                    start_time = (int(time.time()))
                    i = 0
                    capture_enable = True
                    print("##############################################")
                    print(" ")
                    print(" ")
                    print(" ")
                    print(" ")
                    print(" ")
                    print("starting capture")
                    print(" ")
                    print(" ")
                    print(" ")
                    print(" ")
                    print(" ")
                    print("##############################################")
                if button == 2:
                    capture_enable = False
                    i = 0
                    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-")
                    print("stopping capture")
                    print("%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-%-")
    pygame.event.clear()
    print(capture_enable, "wheel: ", wheel, " gas:", acc, " brake: ", brake, " frame: ", i)
    capim = threading.Thread(target=capture_image, name="capim", args=(filename,))
    capim.start()
    input_val = (filename, wheel, acc, brake)
    input_queue.put(input_val)
    if i % 25 == 0:
        if(capture_enable == False):
            with image_queue.mutex, input_queue.mutex:
                image_queue.queue.clear()
                input_queue.queue.clear()
            i = 0
        if(capture_enable == True):
            storedata = threading.Thread(target=store_driving_data, name="storedata", args=())
            storedata.start()
            storeimage = threading.Thread(target=store_image, name="storeimage", args=())
            storeimage.start()
    cv2.imshow("frame", cv2.cvtColor(last_image, cv2.COLOR_RGB2BGR))
    clock.tick(10)
    # limits to 10fps
    i += 1

print("Ending capture")
cap.release()
cv2.destroyAllWindows()

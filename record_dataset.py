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
from subprocess import call
from inputs import devices
from inputs import get_gamepad

img = cv2.imread('steering_wheel_image.jpg',0)
rows,cols = img.shape

cap = cv2.VideoCapture(1)

smoothed_angle = 0

wheel = 0
acc = 0
brake = 0
start_time = (int(time.time()))
i = 0

accumulated_brake = 0
capture_enable = False


# aiming for input sampling frequency at 125Hz/8ms
# NVIDIA paper says 10fps ... what about 8 * 12 = 96ms / 10.417fps


# TODO: make it threaded because I think it's not working realtime-ish on my PC
# esp. image compression and logging, current version has a problem when C-c'd
# TODO: variable normalization support
# for gamepad input, value range is -32767 to 32767
# and 270 degrees between -135 to 135 degrees are mapped to it
#ys.append(float(line.split()[1]) * (135/32767) * (scipy.pi / 180))

# make it threaded and realtime

def capture_image(filename):
    ret, frame = cap.read()
    image = scipy.misc.imresize(frame, [66, 200]) / 255.0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    scipy.misc.imsave("saved_dataset/" + filename, frame)

def show_image():
    time.sleep(1)
    while True:
        if not image_queue.empty():
            cv2.imshow("frame", cv2.cvtColor(image_queue.get(), cv2.COLOR_RGB2BGR))
        time.sleep(0.2)

def capture_wait():
    ctr = 3
    print("Press and hold gas and brake all the way to start/stop recording")
    while ctr > 0:
        print("Starting capture in:", str(ctr))
        ctr += -1
        time.sleep(1)

def process_gamepad():
    events = get_gamepad()
    global wheel
    global acc
    global brake
    for event in events:
        if event.code == "ABS_X":
            wheel = (event.state * (135/32767))
        if event.code == "ABS_RZ":
            acc = event.state
        if event.code == "ABS_Z":
            brake = event.state

def signal_handler(signal, frame):
    cap.release()
    cv2.destroyAllWindows()
    data.flush()
    dataplus.flush()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

while(cv2.waitKey(10) != ord('q')):

    filename = str(str(start_time) + "." + str(i) + ".jpg")
    status  = process_gamepad()
    image_queue = queue.Queue()
    #showim = threading.Thread(target=show_image, name="showim", args=())
    #showim.start()

    if capture_enable == True:
        #frame = capture_image(filename,)
        with open("saved_dataset\dataplus.txt", "a") as dataplus:
            print(filename, wheel, acc, brake, file=dataplus)
        with open("saved_dataset\data.txt", "a") as data:
            print(filename, wheel, file=data)
        print("wheel: ", wheel, "\tgas:", acc, "\tbrake: ", brake, "\tframe: ", i)
        capim = threading.Thread(target=capture_image, name="capim", args=(filename,))
        capim.start()

    else:
        print("PAUSED ", "wheel: ", wheel, "\tgas:", acc, "\tbrake: ", brake, "\tframe: ", i)

    if (acc > 250) and (brake > 250) and (accumulated_brake < (250 * 10 * 20)):
        accumulated_brake += brake

    if (acc > 250) and (brake > 250) and (accumulated_brake > (250 * 10 * 20)):
        accumulated_brake = 0
        capture_wait()
        if capture_enable:
            capture_enable = False
        else:
            capture_enable = True

    i += 1

print("Ending capture")
cap.release()
cv2.destroyAllWindows()

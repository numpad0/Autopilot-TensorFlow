import scipy.misc
import model
import cv2
import time
import os
import threading
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

# aiming for input sampling frequency at 125Hz/8ms
# NVIDIA paper says 10fps ... what about 8 * 12 = 96ms / 10.417fps

captureCounter = 0

def timerThread():
    # Every 8ms this should be called using timer
    # and get control inputs
    control = threading.Thread(target=getControlInputs)
    control.start()
    if !(captureCounter % 12)
        # Every 8 * 12 = 96ms capture image
        # and store on ram
        capt = threading.Thread(target=captureImage)
        capt.start()
    if !(captureCounter % 125)
        # Every 8 * 125 = 1 second save data
        save = threading.Thread(target=saveData)
        save.start()
        captureCounter = 0
    captureCounter += 1
    time.sleep(0.0000)

def getControlInputs():
    # gets control inputs, output to vJoy
    events = get_gamepad()
    for event in events:
        if event.code == "ABS_X":
            wheel = (event.state * (135/32767) * (scipy.pi / 180))
        if event.code == "ABS_RZ":
            acc = event.state
        if event.code == "ABS_Z":
            brake = event.state
    # TODO: pipe events to vJoy

def captureImage():
    ret, frame = cap.read()
    image = scipy.misc.imresize(frame, [66, 200]) / 255.0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # atomically read input
    inputData = [wheel, acc, brake]
    print("wheel: ", wheel, "\tgas:", acc, "\tbrake: ", brake, "\tframe: ", i)
    filename = (str(start_time) + "." + str(i) + ".jpg")

def saveData():
    # save captured frames + input data associated with it
    with open("saved_dataset\dataplus.txt", "a") as dataplus:
        print(filename, wheel, acc, brake, file=dataplus)
    with open("saved_dataset\data.txt", "a") as data:
        print(filename, wheel, file=data)

ctr = 7
while ctr > 0:
    ctr += -1
    print("Starting capture in:", str(ctr))
    time.sleep(1)


t = threading.Timer(0.0008, timerThread)

t.start()
var = 'something'
if var == 'something':
    t.cancel()





# TODO: make it threaded because I think it's not working realtime-ish on my PC
# esp. image compression and logging, current version has a problem when C-c'd
# TODO: variable normalization support
# for gamepad input, value range is -32767 to 32767
# and 270 degrees between -135 to 135 degrees are mapped to it
#ys.append(float(line.split()[1]) * (135/32767) * (scipy.pi / 180))

# make it threaded and realtime

while(cv2.waitKey(10) != ord('q')):
    ret, frame = cap.read()
    image = scipy.misc.imresize(frame, [66, 200]) / 255.0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    events = get_gamepad()
    for event in events:
        if event.code == "ABS_X":
            wheel = (event.state * (135/32767) * (scipy.pi / 180))
        if event.code == "ABS_RZ":
            acc = event.state
        if event.code == "ABS_Z":
            brake = event.state
        print("wheel: ", wheel, "\tgas:", acc, "\tbrake: ", brake, "\tframe: ", i)
        filename = (str(start_time) + "." + str(i) + ".jpg")
        with open("saved_dataset\dataplus.txt", "a") as dataplus:
            print(filename, wheel, acc, brake, file=dataplus)
        with open("saved_dataset\data.txt", "a") as data:
            print(filename, wheel, file=data)

    scipy.misc.imsave("saved_dataset/" + filename, frame)
    cv2.imshow("frame", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
    #cv2.imshow("frame", frame)
    i += 1

cap.release()
cv2.destroyAllWindows()

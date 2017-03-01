import scipy.misc
import model
import cv2
import time
import os
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

ctr = 7
while ctr > 0:
    ctr += -1
    print("Starting capture in:", str(ctr))
    time.sleep(1)

# TODO: make it threaded because I think it's not working realtime-ish on my PC
# esp. image compression and logging, current version has a problem when C-c'd
# TODO: couple it with vJoy so that this script pass-through input rather than
# listening to side by side with apps
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

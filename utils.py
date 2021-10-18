import numpy as np
from djitellopy import Tello
import cv2 as cv
import time

fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]

def init_tello() -> Tello:
    tello = Tello()
    # drone connection
    tello.connect()

    # set all speed to 0
    tello.for_back_velocity = 0
    tello.left_right_velocity = 0
    tello.up_down_velocity = 0
    tello.yaw_velocity = 0
    tello.speed = 0

    print_battery(tello)
    tello.streamoff()  # for better Socket communication
    return tello


def print_battery(tello):
    str_battery = str(tello.get_battery())
    print("\n * Drone battery percentage : " + str_battery + "%")
    return


def detect_face(img):
    face_cascade = cv.CascadeClassifier('haarcascades_XML/haarcascade_frontalface_default.xml')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 8)

    myFaceListC = []  # Center point
    myFaceListArea = []  # Area

    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h

        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

        cv.circle(img, (cx, cy), 5, (0, 255, 0), cv.FILLED)  # Center of face
        roi_face = img[y: y + h, x:x + w]
        cv.imshow("roi_face", roi_face)  # show faces

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trace_face(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    if fbRange[0] < area < fbRange[1]:
        fb = 0
    elif area > fbRange[1]:
        fb = - 20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    me.send_rc_control(0, fb, 0, speed)
    return error


def moveTello(tello):
    tello.takeoff()
    time.sleep(5)

    tello.move_back(50)
    time.sleep(5)

    tello.rotate_clockwise(360)
    time.sleep(5)

    tello.move_forward(50)
    time.sleep(5)

    tello.flip_right()
    time.sleep(5)

    tello.flip_left()
    time.sleep(5)

    tello.land()
    time.sleep(5)

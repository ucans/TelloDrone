"""
201834952 suyeon Chung
Tello + openCV

"""

import time

from utils import *
import cv2 as cv

TOLERANCE_X = 5
TOLERANCE_Y = 5
SLOWDOWN_THRESHOLD_X = 20
SLOWDOWN_THRESHOLD_Y = 20

w, h = 360, 240
pError = 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tello = init_tello()

    tello.takeoff()
    time.sleep(1)

    tello.streamon()
    cv.namedWindow("Drone")
    frame_read = tello.get_frame_read()
    time.sleep(2)

    while True:
        img = frame_read.frame
        img = cv.resize(img, (w, h))
        img, info = detect_face(img)
        pError = trace_face(tello, info, w, pid, pError)

        print("Center :", info[0], "Area : ", info[1])
        cv.imshow('img', img)
        keyborad = cv.waitKey(1)

        if keyborad & 0xFF == ord('q'):
            tello.land()
            frame_read.stop()
            tello.streamoff()
            exit(0)
            break
        if keyborad == ord('w'): tello.move_forward(20)
        if keyborad == ord('s'): tello.move_back(20)
        if keyborad == ord('a'): tello.move_left(20)
        if keyborad == ord('d'): tello.move_right(20)

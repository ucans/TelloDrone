# 201834952 정수연
# My Tello Project
# The Tello pet

import time

from utils import *
import cv2 as cv

TOLERANCE_X = 5
TOLERANCE_Y = 5
SLOWDOWN_THRESHOLD_X = 20
SLOWDOWN_THRESHOLD_Y = 20

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tello = init_tello()

    tello.takeoff()
    time.sleep(1)

    tello.streamon()
    cv.namedWindow("Drone")
    frame_read = tello.get_frame_read()
    time.sleep(2)

    show_window(tello)

    while True:
        img = frame_read.frame
        # TODO : gray scaling
        cv.imshow("Drone", img)

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

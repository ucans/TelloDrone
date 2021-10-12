# 201834952 정수연
# My Tello Project
# 어떤 프로젝트를 만들 것인가?

# time이 어떤 클래스인가?
import time

from utils import *
import cv2 as cv

# Press the green button in the gutter to run the script.
if __name__ == '__main1__':
    # 201834952 정수연
    myDrone = initTello()
    # moveTello(myDrone)

    myDrone.takeoff()
    time.sleep(1)
    myDrone.streamon()
    cv.namedWindow("Drone")
    frame_read = myDrone.get_frame_read()
    time.sleep(2)

    while True:
        img = frame_read.frame
        cv.imshow("Drone", img)

        keyborad = cv.waitKey(1)
        if keyborad & 0xFF == ord('q'):
            myDrone.land()
            frame_read.stop()
            myDrone.streamoff()
            exit(0)
            break
        if keyborad == ord('w'): myDrone.move_forward(20)
        if keyborad == ord('s'): myDrone.move_back(20)
        if keyborad == ord('a'): myDrone.move_left(20)
        if keyborad == ord('d'): myDrone.move_right(20)

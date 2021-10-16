from djitellopy import Tello
import cv2 as cv
import time


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
    tello.streamoff()   # for better Socket communication
    return tello


def print_battery(tello):
    str_battery = str(tello.get_battery())
    print("\n * Drone battery percentage : " + str_battery + "%")
    return


def show_window(tello):
    # tello = Tello()
    while True:
        img = tello.get_frame_read().frame
        cv.imshow("Tello", img)
        cv.waitKey(1)


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

import time
from utils import *
import cv2 as cv

w, h = 360, 240
pError = 0

if __name__ == '__main__':
    # face_collect()

    tello = init_tello()
    time.sleep(1)

    tello.takeoff()
    time.sleep(1)

    tello.streamon()
    frame_read = tello.get_frame_read()
    time.sleep(2)

    tello.move_up(50)
    model = learning()

    while True:
        img = frame_read.frame
        img = cv.resize(img, (w, h))
        # 얼굴 검출
        img, info, theRoi = detect_face(img)

        try:
            theRoi = np.asarray(theRoi)
            face = cv.cvtColor(theRoi, cv.COLOR_BGR2GRAY)
            # 예측
            result = model.predict(face)

            if result[1] < 500:
                confidence = int(100 * (1 - (result[1]) / 300))
                display_string = str(confidence) + '% Confidence it is user'
                cv.putText(img, display_string, (100, 120), cv.FONT_HERSHEY_COMPLEX, 1, (250, 120, 255), 2)

            # 신뢰도가 75보다 크면, 드론이 나를 따라옴.
            if confidence > 70:
                cv.putText(img, "Suyeon", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                pError = trace_face(tello, info, w, pid, pError)

            # 신뢰도가 그 밑이면, 드론 가만히 있음.
            else:
                cv.putText(img, "Unknown", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                tello.send_rc_control(0, 0, 0, 0)

        except:
            # 얼굴 검출 안됨
            cv.putText(img, "Face Not Found", (250, 450), cv.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            tello.send_rc_control(0, 0, 0, 0)
            pass


        print("Center :", info[0], "Area : ", info[1])
        cv.imshow('Output', img)
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
import numpy as np
from djitellopy import Tello
import cv2 as cv
import time
from os import listdir
from os.path import isfile, join

fbRange = [6200, 6800]
pid = [0.4, 0.4, 0]


def init_tello():
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
    # 1.2 scale factor,
    # 8 얼굴 사이의 최소 간격 pixel

    myFaceListC = []  # Center point
    myFaceListArea = []  # Area
    roi = []
    for (x, y, w, h) in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h

        roi = img[y:y + h, x:x + w]
        roi = cv.resize(roi, (200, 200))

        myFaceListC.append([cx, cy])
        myFaceListArea.append(area)

        cv.circle(img, (cx, cy), 5, (0, 255, 0), cv.FILLED)  # Center of face

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]], roi
    else:
        return img, [[0, 0], 0], roi


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


# 전체 사진에서, 얼굴 부위만 추출
def face_extractor(img):
    face_classifier = cv.CascadeClassifier('haarcascades_XML/haarcascade_frontalface_default.xml')
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray, 1.3, 5)

    if faces is ():
        return None

    for (x, y, w, h) in faces:
        cropped_face = img[y:y + h, x:x + w]

    return cropped_face


# 사용자 얼굴 수집
def face_collect():
    cap = cv.VideoCapture(0)    # 웹 캠에서 먼저 얼굴 수집
    count = 0

    while True:
        ret, frame = cap.read()
        if face_extractor(frame) is not None:
            count += 1
            # 200 x 200 정사각형 사이즈로 저장하기
            face = cv.resize(face_extractor(frame), (200, 200))
            face = cv.cvtColor(face, cv.COLOR_BGR2GRAY)

            file_name_path = 'Facial-Recognition/faces/user' + str(count) + '.jpg'
            cv.imwrite(file_name_path, face)

            cv.putText(face, str(count), (50, 50), cv.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        else:
            print("Face not Found")
            pass

        if cv.waitKey(1) == 13 or count == 100:
            break

    cap.release()
    cv.destroyAllWindows()
    print('Colleting Samples Complete!!!')


# 얼굴 학습
def learning():
    data_path = 'Facial-Recognition/faces/'
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path, f))]

    Training_Data, Labels = [], []

    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        images = cv.imread(image_path, cv.IMREAD_GRAYSCALE)
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        Labels.append(i)

    Labels = np.asarray(Labels, dtype=np.int32)
    # 모델 생성
    model = cv.face.LBPHFaceRecognizer_create()
    # 학슴
    model.train(np.asarray(Training_Data), np.asarray(Labels))

    print("Model Training Complete!!!!!")
    return model


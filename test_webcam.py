from keras.models import load_model
import cv2
import numpy as np
import os
import sys

REV_CLASS_MAP = {
    0: "rock",
    1: "paper",
    2: "scissors",
    3: "none"
}

def skinmask(img):
    hsvim = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2, 2))
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)
    return thresh


def mapper(val):
    return REV_CLASS_MAP[val]

model = load_model("play.h5")
cap = cv2.VideoCapture(0)

start = True


while True:
    ret, frame = cap.read()
    if not ret:
        continue


    cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)

    if start:
        roi = frame[100:500, 100:500]
        mask_img = skinmask(roi)
        cv2.imshow("mask_img", mask_img)
        img = cv2.cvtColor(mask_img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        pred = model.predict(np.array([img]))
        move_code = np.argmax(pred[0])
        move_name = mapper(move_code)


        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "result {}(conf:{:.2f})".format(move_name,pred[0][move_code]),
                (5, 50), font, 0.7, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Collecting images", frame)

    k = cv2.waitKey(10)

    if k == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

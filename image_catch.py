import cv2
import numpy as np
import os

# 影像大小設定
image_x, image_y = 50, 50

# 鏡頭設置
cap = cv2.VideoCapture(0)

# 建立影像儲存位置
def create_folder(folder_name):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def main(g_id):
    # 設置影像儲存位置
    create_folder("dataset_images/" + str(g_id))
    counter = 601

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)

        # 設定mask
        kernel = np.ones((3, 3),np.uint8)
        roi = frame[100:500, 100:500]
        cv2.rectangle(frame, (100, 100), (500, 500), (0, 255, 0), 3)    
            
        # 轉換
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([2, 50, 60]), np.array([25, 150, 255]))   

        # loop catch 設定
        if cv2.waitKey(1) & 0xFF == ord('c'):
            path = f'dataset_images/{g_id}/{counter}.png'
            cv2.imwrite(path, mask)

            print(f'image captured #{counter}')
            counter = counter + 1

        cv2.namedWindow('frame', cv2.WINDOW_NORMAL)
        cv2.resizeWindow('frame', (800, 1200))
        cv2.imshow('mask', mask)
        cv2.imshow('frame', frame)
        cv2.moveWindow("mask", 20,20);
        cv2.moveWindow("frame", 500,0);

g_id = input("Enter images: ")
main(g_id)


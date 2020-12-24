#!/usr/bin/env python
# coding: utf-8

import tkinter as tk
from PIL import Image, ImageTk
import cv2
import numpy as np
import time
from keras.models import load_model
import tensorflow as tf
from random import choice
import numpy as np
from tkinter import font as tkFont

#game1 預設關閉
game1_exit = True

#model導入
model = load_model("play.h5")

def close_window():
    global game1_exit
    #如果 game1 處於開啟狀態，關閉它
    if game1_exit == False:
        game1_exit = True
        game1_cvs.pack_forget()

def close_game():
    #關閉 game window
    close_window()
    #關閉 debug window
    cv2.destroyAllWindows()
    #關閉 tkinter window
    win.destroy()

def mapper(val):
    REV_CLASS_MAP = {
        0: "rock",
        1: "paper",
        2: "scissors",
        3: "none"}
    return REV_CLASS_MAP[val]

def skinmask(img_load):
    #影像轉灰階
    hsvim = cv2.cvtColor(img_load, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 48, 80], dtype="uint8")
    upper = np.array([20, 255, 255], dtype="uint8")
    skinRegionHSV = cv2.inRange(hsvim, lower, upper)
    blurred = cv2.blur(skinRegionHSV, (2, 2))
    ret, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)
    return thresh

def calculate_winner(move1, move2):
    #勝負判斷
    if move1 == move2:
        return "Tie"

    if move1 == "rock":
        if move2 == "scissors":
            return "User"
        if move2 == "paper":
            return "Computer"

    if move1 == "paper":
        if move2 == "rock":
            return "User"
        if move2 == "scissors":
            return "Computer"

    if move1 == "scissors":
        if move2 == "paper":
            return "User"
        if move2 == "rock":
            return "Computer"

def game1_open():
    global game1_exit, cap, game1_cvs, img
    
    prepare_time = 30
    
    if game1_exit == True:
        game1_cvs = tk.Canvas(win, bg='#191970', height=720, width=1280)
        game1_cvs.pack()
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280) #Scaling Width
        cap.set(4, 720)  # Scaling Height
        game1_exit = False
        game1_open()
        
    else:
        while (cap.isOpened() and game1_exit == False):
            prev_move = None
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)
            
            # start_time = time.time() 測試迴圈速度行
            if not ret:
                continue

            # rectangle for user to play
            cv2.rectangle(frame, (100, 100), (500, 500), (255, 255, 255), 2)
            # rectangle for computer to play
            cv2.rectangle(frame, (800, 100), (1200, 500), (255, 255, 255), 2)       
            
            # extract the region of image within the user rectangle
            roi = frame[100:500, 100:500]         
            
            mask_img = skinmask(roi)
            
            #翻轉debug window
            flip_mask_img = cv2.flip(mask_img, 1)
            cv2.imshow("mask_img", flip_mask_img)
            
            #灰階img讀入model
            img = cv2.cvtColor(mask_img, cv2.COLOR_GRAY2RGB)
            img = cv2.resize(img, (227, 227))
            pred = model.predict(np.array([img]))
            move_code = np.argmax(pred[0])
            user_move_name = mapper(move_code)

            # 勝負判斷
            
            if prepare_time == 30:
                if prev_move != user_move_name:
                    if user_move_name != "none":
                        computer_move_name = choice(['rock', 'paper', 'scissors'])
                        winner = calculate_winner(user_move_name, computer_move_name)
                    else:
                        computer_move_name = "none"
                        winner = "Waiting..."

                prev_move = user_move_name

                font = cv2.FONT_HERSHEY_SIMPLEX           
                cv2.putText(frame, "Computer: " + computer_move_name, (800, 70), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)        
                cv2.putText(frame, "User: " + user_move_name, (100, 70), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "Winner is: " + winner, (400, 600), font, 2, (0, 0, 255), 4, cv2.LINE_AA)

                if computer_move_name != "none":
                    icon = cv2.imread("images/{}.png".format(computer_move_name))
                    icon = cv2.resize(icon, (400, 400))
                    frame[100:500, 800:1200] = icon
                prepare_time -= 1
                    
            if prepare_time < 0:
                prepare_time = 30
                
            else:
                font = cv2.FONT_HERSHEY_SIMPLEX           
                cv2.putText(frame, "Computer: " + computer_move_name, (800, 70), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)        
                cv2.putText(frame, "User: " + user_move_name, (100, 70), font, 1.2, (255, 255, 255), 2, cv2.LINE_AA)
                cv2.putText(frame, "Winner is: " + winner, (400, 600), font, 2, (0, 0, 255), 4, cv2.LINE_AA)
                frame[100:500, 800:1200] = icon
                prepare_time -= 1
                
            
            if isinstance(frame, np.ndarray):
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frame = Image.fromarray(frame.astype(np.uint8))
                photo = ImageTk.PhotoImage(image=frame)
                game1_cvs.create_image([645, 360], image=photo)

                win.update_idletasks()
                win.update()

            # print("--- %s seconds ---" % (time.time() - start_time)) 測試迴圈速度行

        cap.release()

if __name__ == '__main__':
    
    #基本視窗設置
    win = tk.Tk()
    win.geometry("1320x840")
    
    #右上X鍵關閉時，結束
    win.protocol('WM_DELETE_WINDOW', close_game)
    
    #button設置
    font_text_style = tkFont.Font(family='Helvetica', size=20, weight=tkFont.BOLD)
    
    bt_open_game1 = tk.Button(win,text='猜拳比賽', font=font_text_style, height=2, width=16, command=game1_open, bg='#0052cc', fg='#ffffff')
    bt_open_game1.place(x=50, y=726.5)

    bt_close_camera = tk.Button(win,text='結束比賽(q)', font=font_text_style, height=2, width=16, command=close_window, bg='#0052cc', fg='#ffffff')
    bt_close_camera.place(x=430, y=726.5)

    #bt_show = tk.Button(win,text='戰績紀錄', font=font_text_style, height=2, width=16, command='戰績', bg='#0052cc', fg='#ffffff')
    #bt_show.place(x=620, y=726.5)
    
    bt_close_window = tk.Button(win,text='關閉視窗', font=font_text_style, height=2, width=16, command=close_game, bg='#0052cc', fg='#ffffff')
    bt_close_window.place(x=980, y=726.5)

    win.mainloop()


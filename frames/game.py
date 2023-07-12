import os
import random
import time
import numpy as np
import cv2

folderpath ='frames'
mylist = os.listdir(folderpath)
graphic = [cv2.imread(f'{folderpath}/{impath}') for impath in mylist ]
green = graphic[0];
red = graphic[1];
kill = graphic[2];
winner = graphic[3];
intro = graphic[4];

cv2.imshow('Squid Game',cv2.resize(intro,(0,0),fx=0.69,fy=0.69))
cv2.waitkey(1)

while True:
    cv2.imshow('Squid Game',cv2.resize(intro,(0,0),fx=0.69,fy=0.69))
    if cv2.waitkey(1) & 0xFF==ord('q'):
        break
    
TIMER_MAX=45
TIMER=TIMER_MAX
maxMove=6500000
font=cv2.FONT_HERSHEY_COMPLEX_SMALL
cap=cv2.VideoCapture(0)
frameHeight=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
frameWidth=cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

win=False

prev=time.time()
prevDoll=prev
showFrame=cv2.resize(green,(0,0),fx=0.69,fy=0.69)
isgreen=True

while cap.isOpened() and TIMER>=0:
    if isgreen and(cv2.waitkey(10) & 0xFF==ord('w')):
        win=True
        break
    
    ret,frame=cap.read()
    
    cv2.putText(showFrame, str(TIMER),
                (50, 50), font,
                1, (0, int(255 * (TIMER) / TIMER_MAX), int(255 * (TIMER_MAX - TIMER) / TIMER_MAX)),
                4, cv2.LINE_AA)
    
    cur=time.time()
    
    no=random.randint(1,5)
    if cur-prev>=no:
        prev=cur
        TIMER=TIMER-no
        if cv2.waitkey(10) & 0xFF==ord('w'):
            win=True
            break
        
        if isgreen:
            showFrame=cv2.resize(red,(0,0),fx=0.69,fy=0.69)
            isgreen=False
            ref=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
        else:
            showFrame=cv2.resize(green,(0,0),fx=0.69,fy=0.69)
            isgreen=True
            
    if not isgreen:
        gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        frameDelta=cv2.absdiff(ref,gray)
        thresh=cv2.threshold(frameDelta,20,255,cv2.THRESH_BINARY)[1]
        change=np.sum(thresh)
        
        if change>maxMove:
            break
    else:
        if cv2.waitkey(10) & 0xFF==ord('w'):
            win=True
            break
        
    camshow=cv2.resize(frame,(0,0),fx=0.4,fy=0.4)
    
    camW,camH=camshow.shape[0],camshow.shape[1]
    showFrame[0:camH,-camW:]=camshow
    
    cv2.imshow('Squid Game',showFrame)
    if cv2.waitkey(10) & 0xFF==ord('q'):
        break
    
cap.release()
if not win:
    for i in range(10):
        cv2.immshow('Squid Game',cv2.resize(kill,(0,0),fx=0.69,fy=0.69))
    while True:
        cv2.imshow('Squid Game',cv2.resize(kill,(0,0),fx=0.69,fy=0.69))
        if cv2.waitkey(10) & 0xFF==ord('q'):
            break
else:
    cv2.imshow('Squid Game',cv2.resize(winner,(0,0),fx=0.69,fy=0.69))
    cv2.waitkey(125)
    
    while True:
        cv2.imshow('Squid Game',cv2.resize(winner,(0,0),fx=0.69,fy=0.69))
        if cv2.waitkey(10) & 0xFF==ord('q'):
            break
cv2.destroyAllWindows()
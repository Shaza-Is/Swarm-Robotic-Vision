import cv2
import numpy as np
n = 1190
cap = cv2.VideoCapture('../MOV_1107.mp4')   
while(cap.isOpened()):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.resize(gray,None,fx=0.25, fy=0.25, interpolation = cv2.INTER_CUBIC)
    cv2.imwrite('../Big_robots_classifier_1/pos/' + str(n)+".jpg",res)
    n = n + 1

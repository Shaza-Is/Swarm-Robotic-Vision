import cv2
import numpy as np

kilo_cascade = cv2.CascadeClassifier('cascade.xml')

#try_img = cv2.imread('IMG_try.jpg')
#try_img = cv2.resize(try_img, (200, 200))

#gray = cv2.cvtColor(try_img, cv2.COLOR_BGR2GRAY)

 # image, reject levels level weights.
cap = cv2.VideoCapture('VID_20161105_181824891.mp4')   
while(cap.isOpened()):
    ret, frame = cap.read()
    

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (17,17), 0)
    kilobots = kilo_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(70,70) ,maxSize=(130,130))

    for (x,y,w,h) in kilobots:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,255,0),2)

    cv2.imshow('output', frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()

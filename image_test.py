import cv2
import numpy as np

kilo_cascade = cv2.CascadeClassifier('kf_casc.xml')
try_img = cv2.imread('/home/shaza/Desktop/Swarm_vision/Kilobots/IMG_20161202_113739647.jpg')
try_img = cv2.resize(try_img, (1300, 700))
gray = cv2.cvtColor(try_img, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7,7), 0)

kilobots = kilo_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=7, minSize=(70,70),maxSize=(130,130))

for (x,y,w,h) in kilobots:
    cv2.rectangle(try_img,(x,y),(x+w,y+h),(255,255,0),2)
cv2.imshow('out', try_img)
cv2.waitKey()

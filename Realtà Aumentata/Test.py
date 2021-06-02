import bf
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
imgTarget = cv2.imread('AR_Test.jpg')
myVid = cv2.VideoCapture('Video_Test.mp4')

detection = False
frameCounter = 0
#
success, imgVideo = myVid.read()

print(imgTarget.shape)
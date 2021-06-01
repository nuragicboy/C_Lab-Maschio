import bf as bf
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
imgTarget = cv2.imread('Targetimage.jpg')
myVid = cv2.VideoCapture('Video_Test.mp4')

detection = False
frameCounter = 0
#
success, imgVideo = myVid.read()

hT,wT,cT = imgTarget.shape
imgVideo = cv2.resize(imgVideo,(wT,hT))

orb = cv2.ORB_create(nfeatures=1000)
kp1, des1 = orb.detectAndCompute(imgTarget, None)
imgTarget = cv2.drawKeypoints(imgTarget, kp1, None)


def stackimages(imgarray,scale,lables=[]):
    sizeW= imgarray[0][0].shape[1]
    sizeH = imgarray[0][0].shape[0]
    rows = len(imgarray)
    cols = len(imgarray[0])
    rowsAvailable = isinstance(imgarray[0], list)
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgarray[x][y] = cv2.resize(imgarray[x][y], (sizeW, sizeH), None, scale, scale)
                if len(imgarray[x][y].shape) == 2: imgarray[x][y]= cv2.cvtColor(imgarray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((sizeH, sizeW, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgarray[x])
            hor_con[x] = np.concatenate(imgarray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgarray[x] = cv2.resize(imgarray[x], (sizeW, sizeH), None, scale, scale)
            if len(imgarray[x].shape) == 2: imgarray[x] = cv2.cvtColor(imgarray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgarray)
        hor_con = np.concatenate(imgarray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver


while True:
    success, imgWebcam = cap.read()

    imgAug = imgWebcam.copy()
    kp2, des2 = orb.detectAndCompute(imgWebcam, None)
    imgWebcam = cv2.drawKeypoints(imgWebcam, kp2, None)

    if not detection:
        myVid.set(cv2.CAP_PROP_POS_FRAMES,0)
        frameCounter = 0
    else:
        if frameCounter == myVid.get(cv2.CAP_PROP_FRAME_COUNT):
            myVid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, imgVideo = myVid.read()
        imgVideo = cv2.resize(imgVideo, (wT, hT))
    bf=cv2.BFMatcher()
    matches = bf.knnMatch(des1,des2,k=2)
    good =[]
    for m,n in matches:
        if m.distance < 0.75 *n.distance:
            good.append(m)
    print(len(good))
    imgFeatures = cv2.drawMatches(imgTarget, kp1, imgWebcam, kp2, good, None, flags=2)
    if len(good) > 8:
        detection = True
        srcPts = np.float32([kp1[m.queryIdx].pt for m in good]).reshape(-1, 1, 2)
        dstPts = np.float32([kp2[m.trainIdx].pt for m in good]).reshape(-1, 1, 2)
        matrix, mask = cv2.findHomography(srcPts,dstPts,cv2.RANSAC,5)
        print(matrix)

        pts = np.float32([[0,0],[0,hT],[wT,hT],[wT,0]]).reshape(-1,1,2)
        dst = cv2.perspectiveTransform(pts,matrix)
        img2 = cv2.polylines(imgWebcam,[np.int32(dst)],True,(255,0,255),3)
        #
        imgWarp = cv2.warpPerspective(imgVideo,matrix, (imgWebcam.shape[1],imgWebcam.shape[0]))

        maskNew = np.zeros((imgWebcam.shape[0],imgWebcam.shape[1]),np.uint8)
        cv2.fillPoly(maskNew,[np.int32(dst)],(255,255,255))
        maskInv = cv2.bitwise_not(maskNew)
        imgAug = cv2.bitwise_and(imgAug,imgAug,mask = maskInv)
        imgAug = cv2.bitwise_or(imgWarp,imgAug)
        #
        imgStacked = stackimages(([imgWebcam, imgVideo, imgTarget], [imgFeatures, imgWarp, imgAug]), 0.5)
    #
        #cv2.imshow('maskNew', imgAug)
        #cv2.imshow('imgWarp', imgWarp)
        #cv2.imshow('img', img2)
        #cv2.imshow('imgFeatures', imgFeatures)
        #cv2.imshow('ImgTarget',imgTarget)
        #cv2.imshow('myVid',imgVideo)
        #cv2.imshow('Webcam', imgWebcam)

        cv2.imshow('imgStacked', imgStacked)
        cv2.waitKey(1)
        frameCounter +=1
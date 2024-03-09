##################################################
#### Written By: SATYAKI DE                   ####
#### Written On: 23-May-2022                  ####
#### Modified On 24-May-2022                  ####
####                                          ####
#### Objective: This is the main calling      ####
#### python script that will invoke the       ####
#### clsVideoZoom class to initiate           ####
#### the model to read the real-time          ####
#### human hand gesture from video            ####
#### Web-CAM & control zoom-in & zoom-out.    ####
##################################################

import mediapipe as mp
import cv2
import time
import clsHandMotionScanner as hms
import math
import imutils
import numpy as np

from clsConfig import clsConfig as cf

class clsVideoZoom():
    def __init__(self):
        self.title = str(cf.conf['TITLE'])
        self.minVal = float(cf.conf['minVal'])
        self.maxVal = int(cf.conf['maxVal'])

    def zoomVideo(self, image, Iscale=1):
        try:
            scale=Iscale

            #get the webcam size
            height, width, channels = image.shape

            #prepare the crop
            centerX,centerY=int(height/2),int(width/2)
            radiusX,radiusY= int(scale*centerX),int(scale*centerY)

            minX,maxX=centerX-radiusX,centerX+radiusX
            minY,maxY=centerY-radiusY,centerY+radiusY

            cropped = image[minX:maxX, minY:maxY]
            resized_cropped = cv2.resize(cropped, (width, height))

            return resized_cropped

        except Exception as e:
            x = str(e)

            return image

    def runSensor(self):
        try:
            pTime = 0
            cTime = 0
            zRange = 0
            zRangeBar = 0
            cap = cv2.VideoCapture(0)
            detector = hms.clsHandMotionScanner(detectionCon=0.7)

            while True:
                success,img = cap.read()
                img = imutils.resize(img, width=720)
                #img = detector.findHands(img, draw=False)
                #lmList = detector.findPosition(img, draw=False)

                img = detector.findHands(img)
                lmList = detector.findPosition(img, draw=False)

                if len(lmList) != 0:
                    print('*'*60)
                    #print(lmList[4], lmList[8])
                    #print('*'*60)

                    x1, y1 = lmList[4][1], lmList[4][2]
                    x2, y2 = lmList[8][1], lmList[8][2]

                    cx, cy = (x1+x2)//2, (y1+y2)//2

                    cv2.circle(img, (x1,y1), 15, (255,0,255), cv2.FILLED)
                    cv2.circle(img, (x2,y2), 15, (255,0,255), cv2.FILLED)

                    cv2.line(img, (x1,y1), (x2,y2), (255,0,255), 3)

                    cv2.circle(img, (cx,cy), 15, (255,0,255), cv2.FILLED)

                    lenVal = math.hypot(x2-x1, y2-y1)
                    print('Length:', str(lenVal))
                    print('*'*60)

                    # Hand Range is from 50 to 270
                    # Camera Zoom Range is 0.01, 1
                    minVal = self.minVal
                    maxVal = self.maxVal

                    zRange = np.interp(lenVal, [50, 270], [minVal, maxVal])
                    zRangeBar = np.interp(lenVal, [50, 270], [400, 150])

                    print('Range: ', str(zRange))

                    if lenVal < 50:
                        cv2.circle(img, (cx,cy), 15, (0,255,0), cv2.FILLED)

                cv2.rectangle(img, (50, 150), (85, 400), (255,0,0), 3)
                cv2.rectangle(img, (50, int(zRangeBar)), (85, 400), (255,0,0), cv2.FILLED)

                cTime = time.time()
                fps = 1/(cTime-pTime)
                pTime = cTime


                image = cv2.flip(img, flipCode=1)
                cv2.putText(image, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.imshow("Original Source",image)

                # Creating the new zoom video
                cropImg = self.zoomVideo(img, zRange)
                cv2.putText(cropImg, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
                cv2.imshow("Zoomed Source",cropImg)

                if cv2.waitKey(1) == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

            return 0
        except Exception as e:
            x = str(e)
            print('Error:', x)

            return 1

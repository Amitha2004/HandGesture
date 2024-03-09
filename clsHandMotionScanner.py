##################################################
#### Written By: SATYAKI DE                   ####
#### Modified On 23-May-2022                  ####
####                                          ####
#### Objective: This is the main calling      ####
#### python class that will capture the       ####
#### human hand gesture on real-time basis    ####
#### and that will enable the video zoom      ####
#### capability of the feed directly coming   ####
#### out of a Web-CAM.                        ####
##################################################

import mediapipe as mp
import cv2
import time

class clsHandMotionScanner():
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, modelComplexity=1, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.modelComplex = modelComplexity
        self.trackCon = trackCon
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,self.modelComplex,self.detectionCon, self.trackCon)

        # it gives small dots onhands total 20 landmark points
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        try:
            # Send rgb image to hands
            imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
            self.results = self.hands.process(imgRGB)

            # process the frame
            if self.results.multi_hand_landmarks:
                for handLms in self.results.multi_hand_landmarks:

                    if draw:
                        #Draw dots and connect them
                        self.mpDraw.draw_landmarks(img,handLms,self.mpHands.HAND_CONNECTIONS)

            return img
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            return img

    def findPosition(self, img, handNo=0, draw=True):
        try:
            lmlist = []

            # check wether any landmark was detected
            if self.results.multi_hand_landmarks:
                #Which hand are we talking about
                myHand = self.results.multi_hand_landmarks[handNo]
                # Get id number and landmark information
                for id, lm in enumerate(myHand.landmark):
                    # id will give id of landmark in exact index number
                    # height width and channel
                    h,w,c = img.shape
                    #find the position
                    cx,cy = int(lm.x*w), int(lm.y*h) #center
                    #print(id,cx,cy)
                    lmlist.append([id,cx,cy])

                # Draw circle for 0th landmark
                if draw:
                    cv2.circle(img,(cx,cy), 15 , (255,0,255), cv2.FILLED)

            return lmlist
        except Exception as e:
            x = str(e)
            print('Error: ', x)

            lmlist = []
            return lmlist

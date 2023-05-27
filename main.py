from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np

# Parameters
width, height = 1280, 720
gestureThreshold = 300
folderPath = "Presentation"

# Camera Setup
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

# Hand Detector
detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imgList = sorted(os.listdir(folderPath), key=len)
imgNumber = 0
buttonPressed = False
buttonCounter = 0
annotations = [[]]
annotationStart = False
annotationNumber = 0
buttonDelay = 20

# Small Image Display
hs, ws = int(120 * 1), int(213 * 1)
imgSmall = np.zeros((hs, ws, 3), np.uint8)

while True:
    # Get image frame
    success, img = cap.read()
    img = cv2.flip(img, 1)
    imgCurrent = cv2.imread(os.path.join(folderPath, imgList[imgNumber]))

    # Find the hand and its landmarks
    hands, img = detectorHand.findHands(img)  # with draw
    # Draw Gesture Threshold line
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)

    if hands and not annotationStart and buttonPressed is False:
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        fingers = detectorHand.fingersUp(hand)

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [150, width - 150], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:  # If hand is at the height of the face
            if fingers == [1, 0, 0, 0, 0]:
                if imgNumber > 0:
                    buttonPressed = True
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                if imgNumber < len(imgList) - 1:
                    buttonPressed = True
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = 0
                    annotationStart = False

        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingers == [0, 1, 0, 0, 0]:
            if not annotationStart:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            cv2.circle(imgCurrent, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationNumber].append(indexFinger)
        else:
            annotationStart = False

        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop()
                annotationNumber -= 1
                buttonPressed = True

    else:
        annotationStart = False

        # Button Press Iteration
    if buttonPressed:
        buttonCounter += 1

        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for annotation in annotations:
        for i in range(1, len(annotation)):
            cv2.line(imgCurrent, annotation[i - 1], annotation[i], (0, 0, 200), 12)

    imgSmall = cv2.resize(img, (ws, hs))
    h, w, _ = imgCurrent.shape
    imgCurrent[0:hs, w - ws: w] = imgSmall

    cv2.imshow("Slides", imgCurrent)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

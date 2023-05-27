import os
import cv2
import numpy as np

from cvzone.HandTrackingModule import HandDetector


# Parameters
width, height = 1280, 720
folderPath = "Presentation"

# Camera Setup
capture = cv2.VideoCapture(0)
capture.set(3, width)
capture.set(4, height)

# Hand Detector
detector = HandDetector(detectionCon=0.8, maxHands=1)

# Variables
imageCount = 0
heightOfSmallImg, widthOfSmallImg = int(120 * 1), int(213 * 1)  # width and height of small image
gestureThreshold = 300
buttonPressed = False
buttonCounter = 0
buttonDelay = 30
annotations = [[]]
annotationCount = 0
annotationStart = False

# Get list of images
pathImages = sorted(os.listdir(folderPath), key=len)
# print(pathImages)

while True:
    # import images
    success, img = capture.read()
    img = cv2.flip(img, 1)
    fullImagePath = os.path.join(folderPath, pathImages[imageCount])
    currentImage = cv2.imread(fullImagePath)

    # Hand Detector
    hands, img = detector.findHands(img)
    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 5)

    if hands and buttonPressed is False:
        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]  # List of 21 Landmark points
        fingersUp = detector.fingersUp(hand)  # List of which fingers are up

        # Constrain values for easier drawing
        xVal = int(np.interp(lmList[8][0], [150, width - 150], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal

        if cy <= gestureThreshold:
            if fingersUp == [1, 0, 0, 0, 0]:    # first gesture - Left
                print("Left")
                if imageCount > 0:
                    buttonPressed = True
                    imageCount -= 1
                    annotations = [[]]
                    annotationCount = 0
                    annotationStart = False

            if fingersUp == [0, 0, 0, 0, 1]:    # second gesture - Right
                print("Right")
                if imageCount < len(pathImages) - 1:
                    buttonPressed = True
                    imageCount += 1
                    annotations = [[]]
                    annotationCount = 0
                    annotationStart = False

        if fingersUp == [0, 1, 1, 0, 0]:   # third gesture - Index and Middle finger - show pointer
            cv2.circle(currentImage, indexFinger, 12, (0, 0, 255), cv2.FILLED)

        if fingersUp == [0, 1, 0, 0, 0]:   # fourth gesture - Index finger - draw with pointer
            if annotationStart is False:
                annotationStart = True
                annotationCount += 1
                annotations.append([])
            cv2.circle(currentImage, indexFinger, 12, (0, 0, 255), cv2.FILLED)
            annotations[annotationCount].append(indexFinger)
        else:
            annotationStart = False

        if fingersUp == [0, 1, 1, 1, 0]:    # fifth gesture - erase draw points
            if annotations:
                annotations.pop(-1)
                annotationCount -= 1
                buttonPressed = True

    else:
        annotationStart = False

    # Button Press Iteration
    if buttonPressed:
        buttonCounter += 1

        if buttonCounter > buttonDelay:
            buttonCounter = 0
            buttonPressed = False

    for i in range(len(annotations)):
        for j in range(len(annotations[i])):
            if j != 0:
                cv2.line(currentImage, annotations[i][j - 1], annotations[i][j], (0, 0, 200), 12)


    # Add webcam image on the slides
    imgSmall = cv2.resize(img, (widthOfSmallImg, heightOfSmallImg))
    h, w, _ = currentImage.shape
    currentImage[0:heightOfSmallImg, w - widthOfSmallImg: w] = imgSmall

    cv2.imshow("Image", img)
    cv2.imshow("Slides", currentImage)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break

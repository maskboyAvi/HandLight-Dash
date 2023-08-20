import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import math
from keras.models import load_model

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

offset = 20
imgSize = 300

model = load_model("Models\hand_det_model2.h5", compile=False)
class_names = ["A","B","C","D","E","F"]
gesture_names = ["HI","ROCK","VICTORY","THUMBS_UP","OK","NONE"]
while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        hand = hands[0]
        x, y, w, h = hand['bbox']

        imgWhite = np.ones((imgSize, imgSize, 3), np.uint8) * 255
        imgCrop = img[y - offset:y + h + offset, x - offset:x + w + offset]

        imgCropShape = imgCrop.shape

        aspectRatio = h / w

        try:
            if aspectRatio > 1:
                k = imgSize / h
                wCal = math.ceil(k * w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize - wCal) / 2)
                imgWhite[:, wGap:wCal + wGap] = imgResize

            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize

            prediction = model.predict(imgWhite.reshape(1,300,300,3))
            index = np.argmax(prediction)
            class_name = class_names[index]
            gesture = gesture_names[index]

            # Print prediction and confidence score
            print("Class :", class_name)
            print("Gesture :",gesture)
            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageWhite", imgWhite)
        except:
            print("Error in try block")

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
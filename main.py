import cv2
import numpy as np
import time
from tkinter import *
from threading import Thread
from PIL import Image, ImageTk
from screeninfo import get_monitors
from cvzone.HandTrackingModule import HandDetector
import math
import time
from keras.models import load_model


class GreenRedLightGame:
    def __init__(self, root):

        self.monitors = get_monitors()  
        self.width = self.monitors[0].width

        # Creating tkinter window
        self.root = root
        self.root.title("HandLIGHT Dash")

        self.bg_image = Image.open("Images/bgimg.jpg")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        self.bg_label = Label(root, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.start_button = Button(self.root, text="Start Game", command=self.start_game , height = 2 , width = 14 , bg = "black" , fg = 'white',font = "Times 20 bold" , borderwidth = 20)
        self.start_button.place(relx=0.5, rely=1, anchor="s")

        # VideoCapture Object
        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(maxHands=1)
        self.offset = 20
        self.imgSize = 300
        self.model = load_model("Weights/hand_det_model2.h5", compile=False)
        self.class_names = ["A","B","C","D","E","F"]
        self.gesture_names = ["HI","ROCK","VICTORY","THUMBS_UP","OK","NONE"]
        self.hi = cv2.imread('Images/Signs/Hi.png')
        self.rock = cv2.imread('Images/Signs/rock.png')
        self.peace = cv2.imread('Images/Signs/peace.png')
        self.thumbUp = cv2.imread('Images/Signs/thumbUp.png')
        self.ok = cv2.imread('Images/Signs/ok.png')
        self.gesture_imgList = [self.hi,self.rock,self.peace,self.thumbUp,self.ok]

        self.imoji = 0
        # To track if Gesture done or not
        self.imoji_made = False
        self.imoji_img = self.gesture_imgList[self.imoji]
        self.red_window = 0

        # to know if currently Red Light or Green
        self.curr_window = None
        # To track Points
        self.cPos = 0
        # Track Time
        self.startT = 0
        self.endT = 0
        self.dur = 0
        self.isAlive = True
        self.isInit = False
        self.cStart, self.cEnd = 0, 0
        self.isCinit = False
        # To track If Won or not
        self.winner = False

        # Reading Background Images
        self.green = cv2.imread('Images/green_light.jpg')
        self.red = cv2.imread('Images/red_Light.jpg')
        self.dead = cv2.imread('Images/Dead.png')
        self.WinImg = cv2.imread('Images/Winner.png')
           

    # Reset all game-related attributes and state
    def reset_game(self):
        self.isAlive = True
        self.winner = False
        self.cPos = 0
        self.isInit = False
        self.isCinit = False
        self.red_window = 0

    def play_game(self):
        first_frame = None
        while True:
            _, frm = self.cap.read()
            hands, img = self.detector.findHands(frm)
                        
            if not self.isInit:
                self.curr_window = self.green
                first_frame = None
                self.red_window = 0
                self.startT = time.time()
                self.endT = self.startT
                self.dur = np.random.randint(1, 5)
                self.isInit = True

                # Finding Random Gesture to perform when Just turned GREEN
                self.imoji = np.random.randint(0,5)
                self.imoji_img = self.gesture_imgList[self.imoji]
                frm[10:210,10:210] = self.imoji_img
                


            if (self.endT - self.startT) <= self.dur:
                try:

                    # If still GREEN but already did gesture then finding next Gesture to perform
                    if self.imoji_made:
                        self.imoji = np.random.randint(0,5)
                        self.imoji_img = self.gesture_imgList[self.imoji]
                        frm[10:210,10:210] = self.imoji_img
                        self.imoji_made = False

                    # Impose Gesture to perform Image on Top Left
                    frm[10:210,10:210] = self.imoji_img

                    # If Hands Detected then preprocessing gesture for MODEl prediction
                    if hands:
                        hand = hands[0]
                        x, y, w, h = hand['bbox']

                        imgWhite = np.ones((self.imgSize, self.imgSize, 3), np.uint8) * 255
                        imgCrop = img[y - self.offset:y + h + self.offset, x - self.offset:x + w + self.offset]

                        aspectRatio = h / w

                        try:
                            # Preprocessing Image for Model for Higher accuracy
                            if aspectRatio > 1:
                                k = self.imgSize / h
                                wCal = math.ceil(k * w)
                                imgResize = cv2.resize(imgCrop, (wCal, self.imgSize))
                                wGap = math.ceil((self.imgSize - wCal) / 2)
                                imgWhite[:, wGap:wCal + wGap] = imgResize

                            else:
                                k = self.imgSize / w
                                hCal = math.ceil(k * h)
                                imgResize = cv2.resize(imgCrop, (self.imgSize, hCal))
                                hGap = math.ceil((self.imgSize - hCal) / 2)
                                imgWhite[hGap:hCal + hGap, :] = imgResize

                            # Getting Prediction from MODEL
                            prediction = self.model.predict(imgWhite.reshape(1,300,300,3))
                            index = np.argmax(prediction)
                            class_name = self.class_names[index]

                            #If correct Gestrue then +10 points
                            if index == self.imoji:
                                self.cPos +=10
                                self.imoji_made = True
                                print("Current progress is: ", self.cPos)
                                print("Imoji Made: ",self.gesture_names[index])

                            print("Class:", class_name)
                        except:
                            print("Error in try block")
                except:
                    print("Not visible")

                self.endT = time.time()

            else:
                # If 100 points then WINNER
                if self.cPos >= 100:
                    print("WINNER")
                    self.winner = True
                else:
                    # RED LIGHT MODE initialise
                    if not self.isCinit:
                        self.isCinit = True
                        self.cStart = time.time()
                        self.cEnd = self.cStart
                        self.curr_window = self.red
                        self.red_window = 1

                    if (self.cEnd - self.cStart) <= 3:
                        self.cEnd = time.time()

                    else:
                        self.isInit = False
                        self.isCinit = False
                        first_frame = None
            
            if self.red_window == 1:
                # Finding movement during RED Light
                frame_bw = cv2.cvtColor(frm,cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(frame_bw,(21,21),0)

                # If just turned red then first frame is saved 
                if first_frame is None:
                    first_frame = gray
                else:
                    delta_frame = cv2.absdiff(first_frame,gray)
                    thresold_frame = cv2.threshold(delta_frame,50,255,cv2.THRESH_BINARY)[1]
                    thresold_frame = cv2.dilate(thresold_frame,None,iterations=2)

                    (cntr,_) = cv2.findContours(thresold_frame.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                    for contour in cntr:
                        if cv2.contourArea(contour)<2000:
                            continue
                        else:
                            self.isAlive = False
                    first_frame = gray

            # Attach Red and Green light Image
            frm_resized = cv2.resize(frm, (1920, 1080))
            curr_window_resized = cv2.resize(self.curr_window, (600, 400))
            canvas = np.zeros((1080, 1920, 3), dtype=np.uint8)
            canvas[:1080, :1920] = frm_resized
            canvas[680:1080, 1320:1920] = curr_window_resized

            # Display Score
            score_text = f"Score: {self.cPos}" 
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 2.5 
            font_color = (255, 0, 0) 
            text_size = cv2.getTextSize(score_text, font, font_scale, 2)[0]
            text_x = canvas.shape[1] - text_size[0] - 20 
            text_y = text_size[1] + 20  
            thickness = 8
            cv2.putText(canvas, score_text, (text_x, text_y), font, font_scale, font_color, thickness)

            # Displaying Main WIndow
            cv2.imshow("Main Window", canvas)

            if cv2.waitKey(1) == 27 or not self.isAlive or self.winner:
                self.cap.release()
                cv2.destroyAllWindows()
                break

        # If DEAD, this runs
        if not self.isAlive:
            temp = self.dead
            cv2.imshow("Main Window", temp)
            self.start_button.config(state="active")

        # If WON, this runs
        if self.winner:
            temp = self.WinImg
            cv2.imshow("Main Window", temp)
            self.start_button.config(state="active")

        cv2.waitKey(0)

    def start_game(self):
        #Restart game logic
        self.reset_game()
        
        self.start_button.config(state="disabled")
        self.cap = cv2.VideoCapture(0)

        t = Thread(target=self.play_game)
        t.start()

if __name__ == "__main__":
    root = Tk()
    game = GreenRedLightGame(root)
    root.mainloop()
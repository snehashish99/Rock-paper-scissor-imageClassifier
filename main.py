import cv2
import numpy as np
import random
from tensorflow.keras.models import load_model
CATEGORIES = ['rock', 'paper','scissor']

cam = cv2.VideoCapture(0)

#cv2.namedWindow("Rock-Paper-Scissor")
random.seed(1)
#box corner points
start_point = (160, 120)
end_point = (450, 400)
comp_score=0
user_score=0
size_x=50
size_y=50

comp_move="//"
user_move="//"

while True:
    ret, framemain = cam.read()
    #for rectangular box
    cv2.rectangle(img=framemain, pt1=start_point, pt2=end_point, color=(255, 0, 0), thickness=2)

    #flipping frame
    frame = cv2.flip(framemain,1)
    #updating scores
    scores="Computer= "+str(comp_score)+"   User= "+str(user_score)
    #print scores on video frame
    cv2.putText(frame, scores, (200, 105), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (225, 255, 0))
    #print last moves
    cv2.putText(frame, comp_move, (130, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (225, 255, 0))
    cv2.putText(frame, user_move, (400, 450), cv2.FONT_HERSHEY_COMPLEX_SMALL, .7, (225, 255, 0))
    cv2.imshow("test", frame)
    if not ret:
        break
    k = cv2.waitKey(1)

    if k%256 == 27:
        # ESC pressed
        print("====Final Scores====")
        print("Computer=",comp_score," User=",user_score)
        if(comp_score>user_score):
            print("Computer WON")
        elif(user_score>comp_score):
            print("User WON")
        else:
            print("DRAW")
        print("====================")
        print("Escape hit, closing...")
        break
    elif k%256 == 32:
        # SPACE pressed
        model = load_model('rps-model3.h5')
        ROI = frame[123:400, 192:450]
        #cv2.imshow('Frame', ROI)
        #img_arr = cv2.imread(ROI, cv2.IMREAD_GRAYSCALE)
        ROI=cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
        ROI=cv2.resize(ROI,(size_x,size_y))
        #print(ROI)
        comp=CATEGORIES[random.randint(0,2)]
        #cv2.imshow(CATEGORIES[np.argmax(model.predict(ROI.reshape(-1, size_x, size_y, 1)))], ROI)
        user=CATEGORIES[np.argmax(model.predict(ROI.reshape(-1, size_x, size_y, 1)))]

        user_move="user's move= "+user
        comp_move="computer's move= "+comp

        print("computer=",comp,"  user=",user)
        if(comp=="rock"):
            if(user=="scissor"):
                comp_score+=1
                print("Computer won the round")
            elif(user=="rock"):
                print("Draw")
            elif(user=="paper"):
                user_score+=1
                print("User wins")
        elif(comp == "paper"):
            if (user == "scissor"):
                user_score += 1
                print("User won the round")
            elif (user == "rock"):
                comp_score+=1
                print("Computer won")
            elif (user == "paper"):
                print("Draw")
        elif(comp == "scissor"):
            if (user == "scissor"):
                print("Draw")
            elif (user == "rock"):
                user_score+=1
                print("User won")
            elif (user == "paper"):
                comp_score += 1
                print("Computer wins")
        print("----Score----")
        print("Computer=",comp_score," User=",user_score)
        print("-------------")



cam.release()

cv2.destroyAllWindows()
import cv2 as cv
import mediapipe as mp
import time 
import pyautogui as pyag
import math as mt

def distance(x1,x2,y1,y2):
    return mt.sqrt((x2 - x1)**2 + (y2 - y1)**2)

CONTROL_CHOICE = input("which will you prefer to gesture control the mouse: [L/R]")

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1)

cam_input = cv.VideoCapture(0)

p_time = 0
n_time = 0
run = True
while run:
    ret , frame = cam_input.read()
    frame = cv.flip(frame,1)
    if not ret:
        break
    img_color = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
    result = hands.process(img_color)

    if result.multi_hand_landmarks:
        for hand_landmark in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame,hand_landmark,mp_hands.HAND_CONNECTIONS)

            Rx1, Ry1 = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
            Rx2, Ry2 = hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].x, hand_landmark.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y
            
            Lx1, Ly1 = hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x, hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
            Lx2, Ly2 = hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].x, hand_landmark.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y
        
        if(CONTROL_CHOICE == 'L'):
            if(distance(Rx1,Rx2,Ry1,Ry2)*100 <= 10):
                pyag.rightClick()
            elif(distance(Lx1,Lx2,Ly1,Ly2)*100 <= 10):
                pyag.click()
        elif(CONTROL_CHOICE == 'R'):
            if(distance(Lx1,Lx2,Ly1,Ly2)*100 <= 10):
                pyag.rightClick()
            elif(distance(Rx1,Rx2,Ry1,Ry2)*100 <= 10):
                pyag.click()

#<---input stream along with fps--->#
    frame_time = time.time()
    fps = str(int(1/(frame_time-p_time)))
    p_time = frame_time
    cv.putText(frame,fps,(50,50),2,cv.FONT_HERSHEY_PLAIN,(255,0,0),3)
    cv.imshow("input video stream",frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

try:
    cam_input.release()
finally:
    cv.destroyAllWindows()
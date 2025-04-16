import cv2
import numpy as np
import cvzone
import pyautogui
from cvzone.FPS import FPS
#from mss import mss


fps=FPS()

def capture_screen_region_opencv(x,y,w,h):
    screenshot=pyautogui.screenshot(region=(x,y,w,h))
    screenshot=np.array(screenshot)
    screenshot=cv2.cvtColor(screenshot,cv2.COLOR_RGB2BGR)
    return screenshot


def pre_process(imgcrop):
    gray_frame=cv2.cvtColor(imgcrop,cv2.COLOR_BGR2GRAY)
    _,binary_frame=cv2.threshold(gray_frame,127,255,cv2.THRESH_BINARY_INV)
    canny_frame=cv2.Canny(binary_frame,50,50)
    kernel=np.ones((5,5),np.uint8)
    dilated_frame=cv2.dilate(canny_frame,kernel,iterations=1)
    #cv2.imshow("dilated",dilated_frame)
    return dilated_frame

def find_obstacles(imgcrop,imgpre):
    imgcontours,confound=cvzone.findContours(imgcrop,imgpre,minArea=100,filter=None)
    return imgcontours,confound
def gamelogic(confound,imgcontours,jump_distance=63):
    if confound:
        left_most_contour=sorted(confound,key=lambda x:x["bbox"][0])
        cv2.line(imgcontours,(0,left_most_contour[0]["bbox"][1]+10),
                 (left_most_contour[0]["bbox"][0],left_most_contour[0]["bbox"][1]+10),(0,200,0),10)
        # cv2.imshow("",imgcontours)
        if left_most_contour[0]["bbox"][0] < jump_distance:
            pyautogui.press("space")
            print("jump")

    return imgcontours




while True:
    img=capture_screen_region_opencv(400,300,800,250)

    imgcrop=img[100:180,90:]
    imgpre=pre_process(imgcrop)
    imgcontours,confound=find_obstacles(imgcrop,imgpre)
    imgcontours=gamelogic(confound,imgcontours)

    img[100:180,90:]=imgcontours

    Fps,img=fps.update(img)

    cv2.imshow("img",img)
    #cv2.imshow("imgcrop", imgcrop)
    # cv2.imshow("imgcontours", imgcontours)
    cv2.waitKey(1)


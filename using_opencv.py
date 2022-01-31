import ctypes
import time
import win32com.client as comclt
import win32api, win32con, win32gui, win32ui
import keyboard
import cv2
import numpy as np
import pyautogui
import math
from PIL import ImageGrab, Image, ImageDraw



SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time",ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                 ("mi", MouseInput),
                 ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

# Actuals Functions

def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput( 0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra) )
    x = Input( ctypes.c_ulong(1), ii_ )
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def capture_window():

    hwnd = win32gui.FindWindow(None, "Halo Infinite")
    window_rect = win32gui.GetWindowRect(hwnd)
    #temp_rect = (window_rect[0]+8,window_rect[1]+25, window_rect[2]-8,window_rect[3]-8)
    temp_rect = (window_rect[0]+8,window_rect[1]+130, window_rect[2]-8,window_rect[3]-170)
    image = ImageGrab.grab(temp_rect)
    # size = (int(image.size[0]/6),int(image.size[1]/6))
    # image = image.resize(size, Image.ANTIALIAS)
    # image.show()
    # print("stop")
    return image,temp_rect

def click():
    # win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    time.sleep(0.001)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

img, temp_rect = capture_window()
mid_x = int(img.size[0] / 2)
mid_y = int(img.size[1] / 2)
time.sleep(2)
while(True):

    if keyboard.is_pressed('Esc'):
        print("\nyou pressed Esc, so exiting...")
        print("esc pressed")
        break

    img, temp_rect = capture_window()
    image = np.array(img)

    #image = cv2.imread("D:\python_projects\halo_automation\image_with_hit_point.png")
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    img_rgb =  cv2.blur(img_rgb,(20,20))

    # Filter the image and get the binary mask, where white represents
    # your target color


    ## Gen lower mask (0-5) and upper mask (175-180) of RED
    #mask1 = cv2.inRange(img_hsv, (0,50,20), (5,255,255))
    #mask2 = cv2.inRange(img_hsv, (175,50,20), (180,255,255))
    mask = cv2.inRange(img_hsv, (128,82,53), (173,190,136))

    ## Merge the mask and crop the red regions
    #mask = cv2.bitwise_or(mask1, mask2 )
    croped = cv2.bitwise_and(img_rgb, img_rgb, mask=mask)

    #cv2.imshow("image_cropped", croped)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    #cv2.drawContours(img_rgb, contours, -1, (0,0,255), 2)
    x_distance = 0
    y_distance = 0
    flag = False
    hit_8 = False
    for c in contours:
        area = cv2.contourArea(c)

        if 5 < area:
            x,y,w,h = cv2.boundingRect(c)
            cv2.rectangle(img_rgb, (x,y), (x+w, y+h), (0,0,255),2)
            cv2.drawContours(img_rgb, c, -1 ,(255,255,255),2)
            # print(area)
            mid_box_x  = x
            mid_box_y  = y

            x_distance = int(((mid_box_x - mid_x)/mid_x)*100)
            # adding 10 so we actually hit the person under the dot
            # y_distance = int((y_corner - mid_y)*1.5)
            y_distance = int(((mid_box_y - mid_y)/mid_y)*100)-10
            # print(x_distance, " x_distance")
            # print(y_distance, " y_distance")
            flag = True
            # print(area)



    if flag:
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)
        click()

    cv2.imshow('image', img_rgb)

    cv2.waitKey(1)



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

def click():
    # win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    time.sleep(0.2)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)

# def capture_window():
#
#     hwnd = win32gui.FindWindow(None, "Halo Infinite")
#     window_rect = win32gui.GetWindowRect(hwnd)
#     temp_rect = (window_rect[0]+8,window_rect[1]+25, window_rect[2]-8,window_rect[3]-8)
#     image = ImageGrab.grab(temp_rect)
#     # size = (int(image.size[0]/6),int(image.size[1]/6))
#     # image = image.resize(size, Image.ANTIALIAS)
#     # image.show()
#     # print("stop")
#     return image,temp_rect

# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
wsh= comclt.Dispatch("WScript.Shell")
wsh.AppActivate("Halo Infinite") # select another application
time.sleep(3)

w, h = 10, 10
shape = [(0, 0), (w, h)]
# creating new Image object
img = Image.new("RGB", (w, h))
image, temp_rect = capture_window()

mid_x = int(image.size[0] / 2)
mid_y = int(image.size[1] / 2)

while (True):
    if keyboard.is_pressed('Esc'):
        print("\nyou pressed Esc, so exiting...")
        print("esc pressed")
        break

    # ====================================================================================================================================

    # PressKey(0x1F)
    for i in range(5):
        output = pyautogui.locateOnScreen(image="D:\python_projects\halo_automation\dot.png", region=temp_rect, confidence=0.8)
        if output != None:
            break
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 800,0 , 0, 0)
        # time.sleep(0.1)

    output = pyautogui.locateOnScreen(image="D:\python_projects\halo_automation\dot.png",region=temp_rect,  confidence=0.8)
    if output != None:
        print("found")
        x_corner = output.left - temp_rect[0]
        y_corner = output.top - temp_rect[1]
        # image.paste(img, (x_corner, y_corner))
        # image.show()

        x_distance = int((x_corner - mid_x)*1.5)
        # adding 10 so we actually hit the person under the dot
        # y_distance = int((y_corner - mid_y)*1.5)
        y_distance = int((y_corner - mid_y)*1.5) + 20
        # print(x_distance, " x_distance")
        # print(y_distance, " y_distance")
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x_distance, y_distance, 0, 0)
        # if x_distance < 5 or y_distance < 5:
        click()

    # ====================================================================================================================================

    # PressKey(0x1F)
    # time.sleep(1)
    # time.sleep(1)
    # ReleaseKey(0x11)
    # time.sleep(1)
    # time.sleep(0.1)

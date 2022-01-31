import cv2
import time
import win32com.client as comclt
import win32api, win32con, win32gui, win32ui
import keyboard
import cv2
import numpy as np
import pyautogui
import math
from PIL import ImageGrab, Image, ImageDraw

# A required callback method that goes into the trackbar function.
def nothing(x):
    pass

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


# Initializing the webcam feed.
#cap = cv2.imread("D:\python_projects\halo_automation\image_with_hit_point.png")

#cap = cv2.imread('D:/downloaded_images_from_pexel/no_faces/aerial-view-of-beach-8647637.jpg')
# cap.set(3, 1280)
# cap.set(4, 720)

# Create a window named trackbars.
cv2.namedWindow("Trackbars")

# Now create 6 trackbars that will control the lower and upper range of
# H,S and V channels. The Arguments are like this: Name of trackbar,
# window name, range,callback function. For Hue the range is 0-179 and
# for S,V its 0-255.
cv2.createTrackbar("L - H", "Trackbars", 0, 179, nothing)
cv2.createTrackbar("L - S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L - V", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("U - H", "Trackbars", 179, 179, nothing)
cv2.createTrackbar("U - S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U - V", "Trackbars", 255, 255, nothing)
cv2.namedWindow("Trackbars", cv2.WINDOW_NORMAL)

while True:

    # Start reading the webcam feed frame by frame.
    # ret, frame = cap.read()
    # if not ret:
    #     break
    # Flip the frame horizontally (Not required)
    # frame = cv2.flip(frame, 1)

    # Convert the BGR image to HSV image.

    img, temp_rect = capture_window()
    image = np.array(img)
    cap = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Get the new values of the trackbar in real time as the user changes
    # them
    l_h = cv2.getTrackbarPos("L - H", "Trackbars")
    l_s = cv2.getTrackbarPos("L - S", "Trackbars")
    l_v = cv2.getTrackbarPos("L - V", "Trackbars")
    u_h = cv2.getTrackbarPos("U - H", "Trackbars")
    u_s = cv2.getTrackbarPos("U - S", "Trackbars")
    u_v = cv2.getTrackbarPos("U - V", "Trackbars")

    # Set the lower and upper HSV range according to the value selected
    # by the trackbar
    lower_range = np.array([l_h, l_s, l_v])
    upper_range = np.array([u_h, u_s, u_v])

    # Filter the image and get the binary mask, where white represents
    # your target color
    mask = cv2.inRange(hsv, lower_range, upper_range)

    # You can also visualize the real part of the target color (Optional)
    res = cv2.bitwise_and(cap, cap, mask=mask)

    # Converting the binary mask to 3 channel image, this is just so
    # we can stack it with the others
    mask_3 = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

    # stack the mask, orginal frame and the filtered result
    stacked = np.hstack((mask_3, cap, res))

    # Show this stacked frame at 40% of the size.

    cv2.imshow('Trackbars', cv2.resize(stacked, None, fx=0.5, fy=0.5))

    # If the user presses ESC then exit the program
    key = cv2.waitKey(1)
    if key == 27:
        break

    # If the user presses `s` then print this array.
    if key == ord('s'):
        thearray = [[l_h, l_s, l_v], [u_h, u_s, u_v]]
        print(thearray)

        # Also save this array as penval.npy
        np.save("D:\python_projects\halo_automation\image_with_hit_point_1_edit.png", thearray)
        break

# Release the camera & destroy the windows.
cap.release()
cv2.destroyAllWindows()
import cv2 as cv
import numpy as np
from time import time
import win32gui, win32ui,win32con
from vision import Vision

def windowCapture():

    hwnd = win32gui.FindWindow(None, 'Minecraft 1.16.5 - Singleplayer')

    # get the window size
    windowRectangle = win32gui.GetWindowRect(hwnd)
    w = windowRectangle[2] - windowRectangle[0] - 16
    h = windowRectangle[3] - windowRectangle[1]

    wDC = win32gui.GetWindowDC(hwnd)
    dcObj = win32ui.CreateDCFromHandle(wDC)
    cDC = dcObj.CreateCompatibleDC()
    dataBitMap = win32ui.CreateBitmap()
    dataBitMap.CreateCompatibleBitmap(dcObj, w, h)
    cDC.SelectObject(dataBitMap)
    cDC.BitBlt((0, 0), (w, h), dcObj, (8, 30), win32con.SRCCOPY)

    # save the screenshot
    signedIntsArray = dataBitMap.GetBitmapBits(True)
    img = np.fromstring(signedIntsArray, dtype ='uint8')
    img.shape = (h, w, 4)

    # Free Resources
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

    img = img[...,:3]
    img = np.ascontiguousarray(img)

    return img


v1 = Vision('Zombie.png')
v2 = Vision('creeper.png')
v3 = Vision('steeve.png')

loopTime = time()
while (True):

    screenshot = windowCapture()

    points = v1.findObjects(screenshot, 0.5, 'rectangles')
    points = v2.findObjects(screenshot, 0.5, 'rectangles')
    points = v3.findObjects(screenshot, 0.7, 'rectangles')


    print('Fps: {}'. format(1/(time()-loopTime)))
    loopTime = time()

    if cv.waitKey(1) == ord('q'):
        break


cv.destroyAllWindows()
print('Done')

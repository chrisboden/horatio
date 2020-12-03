import cv2
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image as im

#-----------------------------------------------------------#
imageLink = r'C:\Users\Nicole\Desktop\openCV\bottlecaps.jpeg'
#-----------------------------------------------------------#

img = cv2.imread(imageLink)
img = img[0:480, 0:640]
erode = cv2.erode(img, np.ones((5, 5)), iterations=2)
imgGrey = cv2.cvtColor(erode, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(imgGrey, 100, 255, cv2.THRESH_BINARY)
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

def getSample(img, centerX, centerY):
    pixelCrop0 = img[centerY-5:centerY+5, centerX-5:centerX+5]
    cv2.imwrite('pxl.jpg', pixelCrop0)
    pixelCrop = im.open('pxl.jpg')
    r = 0
    g = 0
    b = 0
    for i in range(10):
        for a in range(10):
            r += pixelCrop.getpixel((i, a))[0]
            g += pixelCrop.getpixel((i, a))[1]
            b += pixelCrop.getpixel((i, a))[2]
    r /= 100
    g /= 100
    b /= 100
    return r, g, b

def rgb2hsv(r, g, b):
    r /= 255
    g /= 255
    b /= 255
    maxc = max(r, g, b)
    minc = min(r, g, b)
    v = maxc
    if minc == maxc:
        return 0.0, 0.0, v
    s = (maxc-minc) / maxc
    rc = (maxc-r) / (maxc-minc)
    gc = (maxc-g) / (maxc-minc)
    bc = (maxc-b) / (maxc-minc)
    if r == maxc:
        h = bc-gc
    elif g == maxc:
        h = 2.0+rc-bc
    else:
        h = 4.0+gc-rc
    h = (h/6.0) % 1.0
    h *= 255
    s *= 255
    v *= 255
    return h, s, v

def getColour(h, s, v):
    if s <= 60 and v >= 180:
        return 'white'
    elif s <= 40:
        return 'grey'
    elif (h >= 0 and h <= 12) or (h >= 215 and h <= 255):
        return 'red'
    elif h >= 13 and h <= 70:
        return 'yellow'
    elif h >= 71 and h <= 148:
        return 'green'
    elif h >= 149 and h <= 214:
        return 'blue'

for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.01*cv2.arcLength(contour, True), True)
    cv2.drawContours(img, [approx], 0, (255, 0, 255), 2)
    x = approx.ravel()[0]
    y = approx.ravel()[1] - 15
    maxX = max(approx.ravel()[::2])
    maxY = max(approx.ravel()[1::2])
    minX = min(approx.ravel()[::2])
    minY = min(approx.ravel()[1::2])
    centerX = round(minX+((maxX-minX)/2))
    centerY = round(minY+((maxY-minY)/2))
    center = [centerX, centerY]
    if len(approx) == 3:
        cv2.putText(img, 'triangle', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
        print('triangle: '+str(center))
        r, g, b = getSample(img, centerX, centerY)
        h, s, v = rgb2hsv(r, g, b)
        cv2.putText(img, getColour(h, s, v), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
    elif len(approx) == 4:
        x1, y1, w, h = cv2.boundingRect(approx)
        aspectRatio = float(w)/h
        if aspectRatio >= 0.95 and aspectRatio >= 1.05:
            cv2.putText(img, 'square', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
            print('square: '+str(center))
            r, g, b = getSample(img, centerX, centerY)
            h, s, v = rgb2hsv(r, g, b)
            cv2.putText(img, getColour(h, s, v), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
        else:
            cv2.putText(img, 'rectangle', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
            print('rectangle: '+str(center))
            r, g, b = getSample(img, centerX, centerY)
            h, s, v = rgb2hsv(r, g, b)
            cv2.putText(img, getColour(h, s, v), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
    elif len(approx) == 5:
        cv2.putText(img, 'pentagon', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
        print('pentagon: '+str(center))
        r, g, b = getSample(img, centerX, centerY)
        h, s, v = rgb2hsv(r, g, b)
        cv2.putText(img, getColour(h, s, v), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
    else:
        cv2.putText(img, 'circle', (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))
        print('circle: '+str(center))
        r, g, b = getSample(img, centerX, centerY)
        h, s, v = rgb2hsv(r, g, b)
        cv2.putText(img, getColour(h, s, v), (x, y - 15), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 255))

cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
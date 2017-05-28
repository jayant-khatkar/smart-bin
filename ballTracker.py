import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


def SearchForBall(dep_arr, l_dep_arr):

    # Find blocks of movement
    diff = (l_dep_arr-dep_arr)*(dep_arr>0)*(l_dep_arr>0)
    diff = diff*(diff>100)
    diff = cv2.boxFilter(diff, -1, (7,7), anchor=(-1,-1), normalize=False)

    # Get the locations of the biggest blocks of movement
    n = 100 #search n best matches
    max_pos = diff.flatten().argsort()[-n:][::-10]
    xpos = max_pos%512
    ypos = np.floor(max_pos/512).astype('int')


    regionSize = 150
    borderSize = 50 + regionSize/2
    found = False
    pos = (0,0,0)
    #print(max_pos)
    #search for circles in the blocks of movement
    for i in reversed(range(0, len(xpos))):
        #if the region is not on the edge of the image
        if xpos[i]>borderSize and xpos[i]<(512-borderSize) and ypos[i]>borderSize and ypos[i]<(424-borderSize):
            found, pos = SearchRegion(dep_arr, (xpos[i],ypos[i]), regionSize)
    return found, pos


def getInitialState(pos,pos_last):

    x_hat = pos - pos_last

    return x_hat


def KalmanPredict(x_hat, timeSinceFound):

    x,y,z = 0,0,0
    predicted_pos   = (x,y,z)

    return predicted_pos


def SearchRegion(dep_arr, predicted_pos, regionSize):

    xpos = predicted_pos[0]
    ypos = predicted_pos[1]

    # Crop Region
    region = dep_arr[xpos-regionSize/2:xpos+regionSize/2,
                     ypos-regionSize/2:ypos+regionSize/2]

    img = (region/2**4).astype('uint8')

    #find the circles
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,100,param1=50,param2=20,minRadius=0,maxRadius=15)

    found = False
    pos = (0,0,0)
    if  not circles is None:
        circles = np.uint16(np.around(circles))

        found = True
        pos = tuple(circles[0,0])
        pos = (int(pos[0] + ypos-regionSize/2) , int(pos[1] + xpos-regionSize/2), pos[2])
        pos = (pos[0], pos[1], dep_arr[pos[0],pos[1]])
        pos2 = getCoordinates(pos)
        print(pos2)

    return found,pos


def KalmanUpdate(x_hat, Pk):

    x_hat = 0
    Pk = 0

    return x_hat, Pk


def getCoordinates(pos):

    cx = 254.746398
    cy = 200.459396
    fx = 366.051208
    fy = 366.051208

    z = pos[2]*1e-3
    x = (pos[1] - cx) * fx * z/1e4
    y = (pos[0] - cy) * fy * z/1e4

    coordinates = (y,x,z)
    return coordinates

def getPixel(pos):
    cx = 254.746398
    cy = 200.459396
    fx = 366.051208
    fy = 366.051208

    z = pos[2]/1e3
    x = int(pos[1]/(fx * z) + cx - 0.5)
    y = int(pos[0]/(fy * z) + cy - 0.5)

    return (x,y,z)

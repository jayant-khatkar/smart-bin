import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


def SearchForBall(depth, l_depth):

    x,y,z = 0,0,0
    found = False
    pos   = (x,y,z)

    return found, pos


def getInitialState(pos,pos_last):

    x_hat = pos - pos_last

    return x_hat


def KalmanPredict(x_hat, timeSinceFound):

    x,y,z = 0,0,0
    predicted_pos   = (x,y,z)

    return predicted_pos


def SearchRegion(predicted_pos):

    found = False
    pos = (0,0,0)

    return found,pos


def KalmanUpdate(x_hat, Pk):

    x_hat = 0
    Pk = 0

    return x_hat, Pk

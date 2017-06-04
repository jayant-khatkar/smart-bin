import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel


def SearchForBall(dep_arr, l_dep_arr):

    # Find blocks of movement
    diff = np.absolute(l_dep_arr-dep_arr)#*(dep_arr>0)*(l_dep_arr>0)
    diff = diff*(diff>100)
    diff = cv2.boxFilter(diff, -1, (7,7), anchor=(-1,-1), normalize=False)

    # Get the locations of the biggest blocks of movement
    n = 100 #search n best matches
    max_val = np.max(np.max(diff))
    max_pos = diff.flatten().argsort()[-n:][::-10]
    xpos = max_pos%512
    ypos = np.floor(max_pos/512).astype('int')


    regionSize = 150
    borderSize = 50 + regionSize/2
    found = False
    pos = (0,0,0)
    posxyz = (0,0,0)
    #print(max_pos)
    #search for circles in the blocks of movement
    if max_val>10e3:
        for i in reversed(range(0, len(xpos))):
            #if the region is not on the edge of the image
            if xpos[i]>borderSize and xpos[i]<(512-borderSize) and ypos[i]>borderSize and ypos[i]<(424-borderSize):
                found, pos = SearchRegion(dep_arr, (xpos[i],ypos[i]), regionSize)
                posxyz = getCoordinates(pos)

    return found, pos, posxyz


def getInitialState(pos,pos_last, dt):

    x_hat = np.array([  pos[1],
                        pos[0],
                        pos[2],
                        (pos[1] - pos_last[1])*dt,
                        (pos[0] - pos_last[0])*dt,
                        (pos[2] - pos_last[2])*dt])

    return x_hat


def predict_pixel(x_hat, timeSinceFound):
    x_new = RungeKutta4(x_hat, timeSinceFound)
    pos = (x_new[0],x_new[1], x_new[2])
    pos = getPixel(pos)
    return pos


def SearchRegion(dep_arr, predicted_pos, regionSize):

    xpos = predicted_pos[0]
    ypos = predicted_pos[1]

    # Crop Region
    region = dep_arr[xpos-regionSize/2:xpos+regionSize/2,
                     ypos-regionSize/2:ypos+regionSize/2]

    img = (region/2**4).astype('uint8')

    #find the circles
    circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,100,param1=50,param2=30,minRadius=0,maxRadius=15)

    found = False
    pos = (0,0,0)
    if  not circles is None:
        circles = np.uint16(np.around(circles))

        found = True
        pos = tuple(circles[0,0])
        pos = (int(pos[0] + ypos-regionSize/2) , int(pos[1] + xpos-regionSize/2), pos[2])
        pos = (pos[0], pos[1], dep_arr[pos[0],pos[1]])


    return found,pos


def KalmanUpdate(x_hat, Pk, dt):

    A = np.matrix([[1,0,0,dt,0,0],
                   [0,1,0,0,dt,0],
                   [0,0,1,0,0,dt],
                   [0,0,0,1+a*dt,0,0],
                   [0,0,0,0,1+a*dt,0],
                   [0,0,0,0,0,1+a*dt]])

    C = np.matrix([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])

    Q = np.ones((6,6))*1e-6
    R = np.matrix([[1,0,0],[0,1,0],[0,0,1]])
    P_k_predicted   = np.matmul(np.matmul(A,Pk),A.T) + Q
    frac = (np.matmul(np.matmul(C,P_k_predicted),C.T)+ R)
    Kk = np.matmul(np.matmul(P_k_predicted, C.T),frac.I);
    #x_hat = x_hat_predicted + Kk*(yt - C*x_hat_predicted);
    #Pk = (I-Kk*C)*P_k_predicted;

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

    z = pos[2]

    if z!=0:
        x = int(pos[1]/(fx * z/1e4) + cx)
        y = int(pos[0]/(fy * z/1e4) + cy)
    else:
        x = 0
        y = 0

    return (y,x,z)

def ballDynamics(xt, dt):
    a = -0.5
    g = -9.8
    x_dot = (1+a*dt)*xt[3]
    y_dot = (1+a*dt)*xt[4] + g*dt
    z_dot = (1+a*dt)*xt[5]

    x_dd = a*xt[3]
    y_dd = a*xt[4] + g
    z_dd = a*xt[5]

    xt_dot = np.array([x_dot,y_dot,z_dot,x_dd,y_dd,z_dd])

    return xt_dot

def RungeKutta4(xt, dt):

    k1 = ballDynamics(xt, 0);
    k2 = ballDynamics(xt + k1*dt/2, dt/2)
    k3 = ballDynamics(xt + k2*dt/2, dt/2)
    k4 = ballDynamics(xt + k3*dt, dt)

    xth = xt+dt*(k1+2*k2+2*k3+k4)/6;

    return xth

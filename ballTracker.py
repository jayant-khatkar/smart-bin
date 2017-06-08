import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

ball_kernel  = np.ones((5,5),np.float32)/25
outer_kernel = np.ones((25,25),np.float32)/(2*25*4-2**2*4)
outer_kernel[2:23,2:23] = 0
greenLower = (29, 86, 6)
greenLower = (29, 126, 86)
greenUpper = (64, 255, 255)


def SearchForBall(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.dilate(mask, None, iterations=2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

	# only proceed if at least one contour was found
    if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)

		# only proceed if the radius meets a minimum size
        if radius > 3:
            return ((x, y), radius)
        else:
            return ((None,None),None)
    else:
        return ((None,None),None)


def getInitialState(pos,pos_last, dt):

    x_hat = np.array([  pos[1],
                        pos[0],
                        pos[2],
                        -(pos[1] - pos_last[1])*dt,
                        (pos[0] - pos_last[0])*dt,
                        (pos[2] - pos_last[2])*dt])

    return x_hat


def predict_pixel(x_hat, timeSinceFound):
    x_new = RungeKutta4(x_hat, timeSinceFound)
    pos = (x_new[1],x_new[0], x_new[2])
    pos = getPixel(pos)
    return pos


def KalmanUpdate(x_hatprev, Pk, yt, dt):

    A = np.matrix([[1,0,0,dt,0,0],
                   [0,1,0,0,dt,0],
                   [0,0,1,0,0,dt],
                   [0,0,0,1,0,0],
                   [0,0,0,0,1,0],
                   [0,0,0,0,0,1]])

    C = np.matrix([[1,0,0,0,0,0],[0,1,0,0,0,0],[0,0,1,0,0,0]])

    Q = np.ones((6,6))*1e-6
    R = np.matrix([[1,0,0],[0,1,0],[0,0,1]])

    #prediction stage
    x_hat_predicted = RungeKutta4(x_hatprev, dt)
    P_k_predicted   = np.matmul(np.matmul(A,Pk),A.T) + Q

    #Update Stage
    frac = (np.matmul(np.matmul(C,P_k_predicted),C.T)+ R)
    Kk = np.matmul(np.matmul(P_k_predicted, C.T),frac.I);
    print(Kk.shape)
    print(yt.shape)
    print((np.matmul(C,x_hat_predicted.T).shape))
    x_hat = x_hat_predicted + np.matmul(Kk,(yt - np.matmul(C,x_hat_predicted.T)));
    Pk = np.matmul((np.eye(6)-np.matmul(Kk,C)),P_k_predicted);
    print(x_hat)
    print(C*x_hat_predicted.T)
    return x_hat, Pk


def getCoordinates(pos):

    cx = 254.746398
    cy = 200.459396
    fx = 366.051208
    fy = 366.051208

    z = pos[2]*1e-3
    x = (pos[1] - cx) * z / fx
    y = (pos[0] - cy) * z / fy

    coordinates = (y,x,z)
    return coordinates

def getPixel(pos):
    cx = 254.746398
    cy = 200.459396
    fx = 366.051208
    fy = 366.051208

    z = pos[2]

    if z!=0:
        x = int(pos[1])*fx/(z + cx)
        y = int(pos[0])*fy/(z + cy)
    else:
        x = 0
        y = 0

    return (y,x)

def ballDynamics(xt, dt):
    a = -0.0
    g = -9.8
    x_dot = -(1+a*dt)*xt[3]
    y_dot = (1+a*dt)*xt[4] #+ g*dt
    z_dot = (1+a*dt)*xt[5]

    x_dd = -a*xt[3]
    y_dd = a*xt[4] #- g
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

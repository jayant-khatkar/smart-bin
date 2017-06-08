# coding: utf-8

#
import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel
from ballTracker    import *
try:
    from pylibfreenect2 import OpenCLPacketPipeline
    pipeline = OpenCLPacketPipeline()
except:
    from pylibfreenect2 import CpuPacketPipeline
    pipeline = CpuPacketPipeline()

# Create and set logger (displays info on screen)
logger = createConsoleLogger(LoggerLevel.Warning)
setGlobalLogger(logger)

fn = Freenect2()
num_devices = fn.enumerateDevices()
if num_devices == 0:
    print("No device connected!")
    sys.exit(1)

serial = fn.getDeviceSerialNumber(0)
device = fn.openDevice(serial, pipeline=pipeline)

listener = SyncMultiFrameListener(FrameType.Color |  FrameType.Ir | FrameType.Depth)
# FrameType.Color | FrameType.Ir | FrameType.Depth)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

device.start()

# NOTE: must be called after device.start()
registration = Registration(device.getIrCameraParams(),
                            device.getColorCameraParams())
print('-----------------------')
print(device.getIrCameraParams().cx)
print(device.getIrCameraParams().cy)
print(device.getIrCameraParams().fx)
print(device.getIrCameraParams().fy)
print('-----------------------')
undistorted = Frame(512, 424, 4)
registered = Frame(512, 424, 4)

# Optional parameters for registration
# set True if you need
need_bigdepth = False
need_color_depth_map = False

bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
color_depth_map = Frame(424, 512,4) \
    if need_color_depth_map else None

# Get the first frame
frames = listener.waitForNewFrame()
l_depth= frames["depth"]
l_dep_arr = l_depth.asarray()
l_time = l_depth.timestamp
pos_last = (0,0,0)
listener.release(frames)

# initialise variables
ballSeen = 0
kernel = np.ones((3,3),np.float32)/8
Pk = np.eye(6)
kernel[1,1] = 0
pos_prev = (0,0,0)
greenLower = (29, 86, 6)
greenLower = (29, 126, 86)
greenUpper = (64, 255, 255)
pos=(0,0,0)
while True:

    # Get the latest data from the kinect
    frames = listener.waitForNewFrame()
    color = frames["color"]
    # ir = frames["ir"]
    depth= frames["depth"]
    registration.apply(color, depth, undistorted, registered)

    # Time since last frame
    dt = (depth.timestamp - l_time)/1e3

    analyse_this = registered.asarray(np.uint8)



	# only proceed if at least one contour was found
    ((x, y), radius) = SearchForBall(analyse_this)
    if x is not None:
        pos = getCoordinates((int(x), int(y), depth.asarray()[int(y),int(x)]))


    # If we dont know the position of the ball
    # If we dont know the position of the ball
    # If we dont know the position of the ball
    # If we dont know the position of the ball
    # If we dont know the position of the ball
    # If we dont know the position of the ball

        # Search frame thoroughly

    if x is not None:
        ballSeen = ballSeen + 1
        timeSinceFound = 0

        # If we see the ball two frames in a row,
        # get the initial state of the Kalman filter
        if ballSeen>=2:
           x_hat = getInitialState(pos,pos_last,dt)

    else:
        ballSeen = 0
    pos_last = pos


    if ballSeen>2:
        for timeInFuture in range(0,20):
            # Predict where the ball will be
            future_pos = predict_pixel(x_hat, timeInFuture/10)
            cv2.circle(analyse_this, future_pos, 5, (0, 0, 255), -1)
        '''
            x_hat, Pk = KalmanUpdate(x_hat, Pk)
            timeSinceFound = 0

        # Otherwise, keep going for 0.5s before giving up
        else:
            timeSinceFound = timeSinceFound + dt
            if timeSinceFound >500: #haven't seen ball for 0.5 second
                ballSeen=0    #then consider the ball lost
        '''
    # cv2.imshow("ir", ir.asarray() / 65535.)
    # cv2.imshow("depth", depth / 4500.)

    if x is not None:
        cv2.circle(analyse_this, (int(x), int(y)), int(radius),(0, 255, 255), 2)

    cv2.imshow("depth", analyse_this)


    l_time = depth.timestamp
    l_dep_arr = analyse_this



    key = cv2.waitKey(delay=1)
    listener.release(frames)
    if key == ord('q'):
        device.stop()
        device.close()
        break

device.stop()
device.close()

sys.exit(0)

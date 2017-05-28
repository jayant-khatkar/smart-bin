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
logger = createConsoleLogger(LoggerLevel.Debug)
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
while True:

    # Get the latest data from the kinect
    frames = listener.waitForNewFrame()
    color = frames["color"]
    # ir = frames["ir"]
    depth= frames["depth"]
    registration.apply(color, depth, undistorted, registered)

    # Time since last frame
    dt = depth.timestamp - l_time
    '''
    # If we dont know the position of the ball
    if ballSeen < 2:

        # Search frame thoroughly
        found, pos = SearchForBall(depth.asarray(), l_dep_arr)

        if found:
            ballSeen = ballSeen + 1
            timeSinceFound = 0

            # If we see the ball two frames in a row,
            # get the initial state of the Kalman filter
            if ballSeen==2:
                x_hat = getInitialState(pos,pos_last)

        else:
            ballSeen = 0
        pos_last = pos

    else:
        # Predict where the ball will be
        predicted_pos = KalmanPredict(x_hat, timeSinceFound)

        # Search in the predicted region only
        found, pos = SearchRegion(predicted_pos)

        # If we found a reasonable match, update the Kalman state
        if found:
            x_hat, Pk = KalmanUpdate(x_hat, Pk)
            timeSinceFound = 0

        # Otherwise, keep going for 0.5s before giving up
        else:
            timeSinceFound = timeSinceFound + dt
            if timeSinceFound >500: #haven't seen ball for 0.5 second
                ballSeen=0    #then consider the ball lost
    '''
    # max_pos = np.argmax(diff)
    # max_val = np.max(diff)
    # x_pos = max_pos%512
    # y_pos = int(np.floor(max_pos/512))
    #draw circle
    img = (depth.asarray()/2**4).astype('uint8')
    # img = cv2.medianBlur(img,5)

    #circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,100,param1=50,param2=15,minRadius=0,maxRadius=15)
    found, pos = SearchForBall(depth.asarray(), l_dep_arr)
    #x_hat = getInitialState(pos,pos_last)
    pos_last = pos
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    # draw the outer circle
    cv2.circle(img,(pos[0],pos[1]),10,(0,255,0),2)
    # draw the center of the circle
    #cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)


    #disp_image = registered.asarray(np.uint8)
    # print(max_val)
    # if max_val>10000:
        # cv2.circle(disp_image, (x_pos,y_pos), 10, 255, thickness=3, lineType=8, shift=0)
    # cv2.imshow("ir", ir.asarray() / 65535.)
    # cv2.imshow("depth", depth / 4500.)
    # cv2.imshow("depth2", diff)
    # cv2.imshow("color", cv2.resize(color.asarray(),
    #                               (int(1920 / 3), int(1080 / 3))))
    cv2.imshow("registered", img)

    # if need_bigdepth:
#        cv2.imshow("bigdepth", cv2.resize(bigdepth.asarray(np.float32),
#                                          (int(1920 / 3), int(1082 / 3))))
#    if need_color_depth_map:
#        cv2.imshow("color_depth_map", color_depth_map.reshape(424, 512))

    l_time = depth.timestamp
    l_dep_arr = depth.asarray()



    key = cv2.waitKey(delay=1)
    listener.release(frames)
    if key == ord('q'):
        device.stop()
        device.close()
        break

device.stop()
device.close()

sys.exit(0)

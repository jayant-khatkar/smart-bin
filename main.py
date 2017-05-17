# coding: utf-8

#
import numpy as np
import cv2
import sys
from pylibfreenect2 import Freenect2, SyncMultiFrameListener
from pylibfreenect2 import FrameType, Registration, Frame
from pylibfreenect2 import createConsoleLogger, setGlobalLogger
from pylibfreenect2 import LoggerLevel

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

listener = SyncMultiFrameListener(FrameType.Color | FrameType.Depth)
# FrameType.Color | FrameType.Ir | FrameType.Depth)

# Register listeners
device.setColorFrameListener(listener)
device.setIrAndDepthFrameListener(listener)

device.start()

# NOTE: must be called after device.start()
# registration = Registration(device.getIrCameraParams(),device.getColorCameraParams())

# undistorted = Frame(512, 424, 4)
# registered = Frame(512, 424, 4)

# Optional parameters for registration
# set True if you need
need_bigdepth = False
need_color_depth_map = False

bigdepth = Frame(1920, 1082, 4) if need_bigdepth else None
color_depth_map = np.zeros((424, 512),  np.int32).ravel() \
    if need_color_depth_map else None

#huncher = cv2.createBackgroundSubtractorMOG2()
start = True
while True:
    frames = listener.waitForNewFrame()

    #color = frames["color"].asarray()
    #####ir = frames["ir"]
    depth= frames["depth"]
    dep_arr = depth.asarray()
    if start:
        start=False
        last_depth= depth
        ldep_arr = last_depth.asarray()
    # registration.apply(color, depth, undistorted, registered,
#                       bigdepth=bigdepth,
#                       color_depth_map=color_depth_map)
    #masked = huncher.apply(depth.asarray() / 4500.)

    diff = (ldep_arr-dep_arr)*(dep_arr>0)*(ldep_arr>0)
    diff = diff*(diff>300)
    diff2 = cv2.boxFilter(diff, -1, (10,10), anchor=(-1,-1), normalize=False)
    max_pos = np.argmax(diff2)
    max_val = np.max(diff2)
    x_pos = max_pos%512
    y_pos = int(np.floor(max_pos/512))
    #draw circle
    print(max_val)
    if max_val>5000:
        cv2.circle(diff, (x_pos,y_pos), 10, 255, thickness=3, lineType=8, shift=0)
    # cv2.imshow("ir", ir.asarray() / 65535.)
    #cv2.imshow("depth", depth / 4500.)
    cv2.imshow("depth2", diff)
    #cv2.imshow("color", cv2.resize(color.asarray(),
    #                               (int(1920 / 3), int(1080 / 3))))
    # cv2.imshow("registered", registered.asarray(np.uint8))

    # if need_bigdepth:
#        cv2.imshow("bigdepth", cv2.resize(bigdepth.asarray(np.float32),
#                                          (int(1920 / 3), int(1082 / 3))))
#    if need_color_depth_map:
#        cv2.imshow("color_depth_map", color_depth_map.reshape(424, 512))
    last_depth= depth
    ldep_arr = last_depth.asarray()
    listener.release(frames)

    key = cv2.waitKey(delay=1)

    if key == ord('q'):
        device.stop()
        device.close()
        break

device.stop()
device.close()

sys.exit(0)

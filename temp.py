
#!/usr/bin/env python


'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
'''

import time
import numpy as np
import cv2 as cv

from multiprocessing.pool import ThreadPool
from collections import deque

from processing import process_frame

# from common import clock, draw_str, StatValue
# import video


def main():
    import sys

    try:
        fn = sys.argv[1]
    except:
        fn = 0

    cap = cv.VideoCapture(0)

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    ################################
    # set up neural network
    classNames=[]
    classFile='coco.names'
    with open(classFile,'rt') as f:
        classNames= f.read().rstrip('\n').split('\n')

    #pretrained dnn model
    configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
    weightsPath = 'frozen_inference_graph.pb'

    #pre set parameters
    net = cv.dnn_DetectionModel(weightsPath,configPath)
    net.setInputSize(320,320)
    net.setInputScale(1.0/127.5)
    net.setInputMean((127.5,127.5,127.5))
    net.setInputSwapRB(True)
    # thres=0.6
    # nms_threshold=0.2   #(lower,more suppress)
    ################################


    # cap = video.create_capture(fn)


    # def process_frame(frame, t0):
    #     # some intensive computation...
    #     # frame = cv.medianBlur(frame, 19)
    #     frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)        
    #     return frame, t0

    threadn = cv.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)
    pending = deque()

    # latency = StatValue()
    # frame_interval = StatValue()
    last_frame_time = time.time_ns()
    while True:
        while len(pending) > 0 and pending[0].ready():
            res, t0 = pending.popleft().get()
            # latency.update(clock() - t0)
            # draw_str(res, (20, 20), "threaded      :  " + str(threaded_mode))
            # draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value*1000))
            # draw_str(res, (20, 60), "frame interval :  %.1f ms" % (frame_interval.value*1000))

            cv.imshow('threaded video', res)
        if len(pending) < threadn:
            _ret, frame = cap.read()
            t = time.time_ns()
            # frame_interval.update(t - last_frame_time)
            last_frame_time = t
            task = pool.apply_async(process_frame, (frame.copy(), t, net, classNames))
            pending.append(task)
        ch = cv.waitKey(1)
        if ch == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()

#  This code from this example https://github.com/opencv/opencv/blob/master/samples/python/video_threaded.py
# https://stackoverflow.com/questions/47260597/python-async-io-image-processing
# https://stackoverflow.com/questions/12474182/asynchronously-read-and-process-an-image-in-python?rq=3


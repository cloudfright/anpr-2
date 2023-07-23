# opencv threading tutorial
# https://github.com/opencv/opencv/blob/master/samples/python/video_threaded.py


from threading import Thread
import cv2, time
from collections import deque
import logging

# apdapted from  https://github.com/PyImageSearch/imutils/blob/master/imutils/video/webcamvideostream.py
class VideoStream(object):
    def __init__(self, queue, src=0):
        self.capture = cv2.VideoCapture(src)
        self.frame_queue = queue
        # Start the thread to read frames from the video stream

        logging.info("width: %s", self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        logging.info("height: %s", self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        logging.info("fps: %s", self.capture.get(cv2.CAP_PROP_FPS))

        self.thread = Thread(target=self.update, args=())
        self.thread.daemon = True
        self.thread.start()

    def update(self):
        # Read the next frame from the stream in a different thread
        while True:
            if self.capture.isOpened():
                (self.status, self.frame) = self.capture.read()
                self.frame_queue.append(self.frame)
            time.sleep(.01)

    def release(self):
        self.capture.release()



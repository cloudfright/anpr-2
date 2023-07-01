import cv2, time
from collections import deque
import logging
from capture import VideoStream

def show_frame():
    # take a frame off the queue
    if len(frame_queue) > 0:
        frame = frame_queue.popleft()
        cv2.imshow('frame', frame)
          
    key = cv2.waitKey(1)
    if key == ord('q'):
        video_stream_widget.release()
        cv2.destroyAllWindows()
        exit(1)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    frame_queue = deque()
    video_stream_widget = VideoStream(frame_queue)

    while True:
        try:
            show_frame()
        except AttributeError:
            pass


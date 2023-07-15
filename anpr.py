import cv2, time
from collections import deque
import logging
from multiprocessing import Process, Manager, Queue
from detect import ObjectDetector
from multiprocessing.pool import ThreadPool
from platereader import PlateReader
from capture import VideoStream
import datetime

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)
    
    prev_frame_time = 0
    new_frame_time = 0

    # create a thread pool to do the ocr processing (leave somme headroom)
    pool = ThreadPool(processes = int(cv2.getNumberOfCPUs() / 2 ))

    detector = ObjectDetector()
    plate_reader = PlateReader()
    frame_queue = deque()

    try:
        # start the video stream
        video_stream = VideoStream(frame_queue, 0)
    except:
        logging.critical("Cannot start video stream")
        exit()

    movement_count = 0
    ocr_queue = deque() 

    while True:
        try:

            if (len(frame_queue) > 0):
                frame = frame_queue.popleft()
                
                # drop a frame to keep up with the video stream
                if (len(frame_queue) > 0):
                    frame = frame_queue.popleft()

                filename = detector.detect_objects(frame)

                if filename:
                    # motion detected 
                    movement_count += 1
                    ocr_queue.append(filename)
                else:
                    if (movement_count > 0):
                        movement_count -= 1
                    else:    
                        # motion ended                   
                        if len(ocr_queue):
                            logging.debug("motion ended")
                            ocr_list_to_process = []
                            while (len(ocr_queue)):
                                ocr_list_to_process.append(ocr_queue.popleft())
                            result = pool.apply_async(plate_reader.read_plate, args=([ocr_list_to_process]))
   

                new_frame_time = time.time()
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)  
                fps = str(fps)
  
                # cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                # cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                # cap.release()
                video_stream.release()
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            pass

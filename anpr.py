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
   

                # new_frame_time = time.time()
                # fps = 1/(new_frame_time-prev_frame_time)
                # prev_frame_time = new_frame_time
                # fps = int(fps)  
                # fps = str(fps)
  
                # cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                # cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                video_stream.release()
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            pass


"""
import schedule
import time

def task():
    print("Scheduled task is running...")

# Schedule the task to run every 5 seconds
schedule.every(5).seconds.do(task)

# Schedule the task to run every day at 10:00 AM
schedule.every().day.at("10:00").do(task)

# Run the scheduled task indefinitely
while True:
    schedule.run_pending()
    time.sleep(1)





import os

folder_path = "/path/to/folder"

# Get a list of all files in the folder
file_list = os.listdir(folder_path)

# Iterate over the file list and delete each file
for file_name in file_list:
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

print("All files in the folder have been deleted.")

"""
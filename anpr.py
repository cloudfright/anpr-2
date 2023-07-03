import cv2, time
from collections import deque
import logging
from multiprocessing import Process, Manager, Queue
from detect import ObjectDetector
from multiprocessing.pool import ThreadPool
from platereader import PlateReader
from capture import VideoStream


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    prev_frame_time = 0
    new_frame_time = 0

    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    # logging.info("width: %s", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # logging.info("height: %s", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # logging.info("fps: %s", cap.get(cv2.CAP_PROP_FPS))
    
    # if not cap.isOpened():
    #     logging.critical("Cannot open camera")
    #     exit()

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
            # status, frame = cap.read()

            if (len(frame_queue) > 0):
                frame = frame_queue.popleft()
                
                # drop a frame to keep up with the video stream
                if (len(frame_queue) > 0):
                    frame = frame_queue.popleft()

                filename = detector.detect_objects(frame)
    
                if filename:
                    # motion detected 
                    movement_count += 1
                    logging.debug("motion detected")
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
                # print(fps)

                # print(len(frame_queue))
                cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                # cap.release()
                video_stream.release()
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            pass


# OPENMP error on mac https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
# export KMP_DUPLICATE_LIB_OK=TRUE
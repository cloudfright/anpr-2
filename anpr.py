import cv2, time
from collections import deque
import logging
from multiprocessing import Process, Manager, Queue
from detect import ObjectDetector
from multiprocessing.pool import ThreadPool
from platereader import PlateReader


def test_process(files_to_process):
    logging.info(f"test process {files_to_process}")
    time.sleep(3)

if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)

    prev_frame_time = 0
    new_frame_time = 0

    cap = cv2.VideoCapture(0)

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)


    logging.info("width: %s", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    logging.info("height: %s", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    logging.info("fps: %s", cap.get(cv2.CAP_PROP_FPS))
    
    if not cap.isOpened():
        logging.critical("Cannot open camera")
        exit()

    threadn = cv2.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)

    detector = ObjectDetector()
    plate_reader = PlateReader()

    while True:
        try:
            status, frame = cap.read()
            files = detector.detect_objects(frame)
     
            if (len(files) > 0):
                result = pool.apply_async(plate_reader.read_plate, args=([files]))

            new_frame_time = time.time()
            fps = 1/(new_frame_time-prev_frame_time)
            prev_frame_time = new_frame_time
            fps = int(fps)  
            fps = str(fps)
            # print(fps)

            cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
            cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                cap.release()
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            pass


# OPENMP error on mac https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
# export KMP_DUPLICATE_LIB_OK=TRUE
import cv2
import logging
import time
import datetime
from paddleocr import PaddleOCR
from persistence import EventPersistence
from collections import Counter
import json
import os

class PlateReader(object):
    
    def __init__(self):        
        self.reader = PaddleOCR(use_angle_cls=True, show_log=False, lang='en') # need to run only once to download and load model into memory

    def read_plate(self,filenames):

        event_db = EventPersistence()

        logging.debug(f"Plate READER - numfiles to read {len(filenames)}")  
        results = []
        for filename in filenames:
            result = self.reader.ocr(filename, cls=False)

            if len(result) > 0 and len(result[0]) > 0:
                for idx in range(len(result)):
                    res = result[idx]
                    text, confidence = res[0][1]
                    if (confidence > 0.75):
                        # logging.debug(f"OCR result: {text} - {confidence}")
                        results.append((datetime.datetime.now().timestamp(), filename, text, confidence))


        if (len(results) > 0):
            logging.debug(f"------------------------------------")
            # sort the results by confidence. descending
            results.sort(key=lambda tup: tup[3], reverse=True)
            
            for result in results:
                logging.debug(f"OCR result: {result}")

            top_result = results[0]
            timestamp = top_result[0]
            img_filename_capture = top_result[1]
            img_filename_archive = f"./images/archive/{os.path.basename(img_filename_capture)}"
            
            try:
                # archive the image with the highest ocr confidence
                img_src = cv2.imread(img_filename_capture)
                cv2.imwrite(img_filename_archive, img_src)
            except:
                logging.error(f"Error writing image to archive: {img_filename_archive}")

            # make a list of all the text recognised and count the number of instances of each
            ocr_text = [item[2] for item in results]
            ocr_text_count = Counter(ocr_text)  
            ocr_readings = json.dumps(ocr_text_count)

            logging.debug(f"OCR timestamp: {timestamp}")
            logging.debug(f"OCR filename: {img_filename_archive}")
            logging.debug(f"OCR readings: {ocr_readings}")

            try:
                event_db.record_event(timestamp, img_filename_archive, ocr_readings)
            except:
                logging.error(f"Error recording event to database")    

        

         

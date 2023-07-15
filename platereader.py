import cv2
import logging
import time
import datetime
from paddleocr import PaddleOCR


class PlateReader(object):
    
    def __init__(self):        
        self.reader = PaddleOCR(use_angle_cls=True, show_log=False, lang='en') # need to run only once to download and load model into memory
        
    def read_plate(self,filenames):

      logging.debug(f"Plate READER - numfiles to read {len(filenames)}")  
      results = []
      for filename in filenames:
        result = self.reader.ocr(filename, cls=False)

        if len(result) > 0 and len(result[0]) > 0:
          for idx in range(len(result)):
            res = result[idx]
            text, confidence = res[0][1]
            results.append((datetime.datetime.now(), filename, text, confidence))

      # sort by confidence
      results.sort(key=lambda tup: tup[3], reverse=True)
      logging.debug(f"------------------------------------")
      for result in results:
        logging.debug(f"OCR result: {result}")   
      
      return results
         

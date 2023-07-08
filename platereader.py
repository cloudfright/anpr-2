import cv2
import logging
import time
import easyocr
import datetime
from paddleocr import PaddleOCR


class PlateReader(object):
    
    USE_PADDLE_OCR = True

    def __init__(self):
        
        if PlateReader.USE_PADDLE_OCR:
            self.reader = PaddleOCR(use_angle_cls=True, show_log=False, lang='en') # need to run only once to download and load model into memory
        else:             
            self.reader = easyocr.Reader(['en'], gpu=False)
            self.allowed_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        

    def read_plate(self,filenames):
      # mono_frame = cv2.cvtColor(frame , cv2.COLOR_RGB2GRAY)
      # processed_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)
      #   processed_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      #   # processed_img = cv2.resize(processed_img, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
      # # thr = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
      #   thr = cv2.adaptiveThreshold(processed_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 4)
      #   processed_img = cv2.bitwise_not(thr)
      # cv2.imshow('for ocr', processed_img)

  

      logging.debug(f"Plate READER - numfiles to read {len(filenames)}")
      # logging.debug(f"Plate READER - {filenames}")

  
      results = []
      if PlateReader.USE_PADDLE_OCR:
        # img_path = "./" + filename
        for filename in filenames:

          logging.debug(f"reading - {filename}")
          result = self.reader.ocr(filename, cls=True)
          logging.debug(f"result: {result}")

          if len(result) > 0 and len(result[0]) > 0:
            for idx in range(len(result)):
              res = result[idx]
              # print (res)
              results.append((datetime.datetime.now(), "filename", res[1][0], res[1][1]))

        results.sort(key=lambda tup: tup[3], reverse=True)
        for result in results:
          # print(result)
          logging.debug(f"Plate READER - OCR results: {results}")   
      else:
        for filename in filenames:
          # logging.debug(f"Plate READER - Reading plate from {filename}")
          frame = cv2.imread(filename)
          if frame is None:
            logging.error(f"Plate READER - Could not read file {filename}")

          result = self.reader.readtext(frame, allowlist=self.allowed_chars)
          # logging.debug(f"Plate READER - OCR result: {result}")

          for (bbox, text, prob) in result:
            results.append((datetime.datetime.now(), filename, text, prob))
 
         
    def cleanup_text(self,text):
	    # strip out non-ASCII text 
	    return "".join([c if ord(c) < 128 else "" for c in text]).strip()
  
import cv2
import logging
import time
import easyocr
import datetime


class PlateReader(object):
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=True)
        pass        
    

   
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

      logging.info(f"Plate READER - Reading plate -  files: {filenames}")     

      for filename in filenames:
        logging.debug(f"Plate READER - Reading plate from {filename}")
        frame = cv2.imread(filename)
        if frame is None:
          logging.error(f"Plate READER - Could not read file {filename}")
        result = self.reader.readtext(frame)
        logging.debug(f"Plate READER - OCR result: {result}")

        for (bbox, text, prob) in result:
          if (float(prob) > 0.3):
            logging.info(f"OCR = {self.cleanup_text(text)} prob:{prob} time:{datetime.datetime.now.strftime('%Y-%m-%d %H:%M:%S')}")
          else:
            logging.info("not confident enough to read plate")
         
    def cleanup_text(self,text):
	    # strip out non-ASCII text 
	    return "".join([c if ord(c) < 128 else "" for c in text]).strip()
  
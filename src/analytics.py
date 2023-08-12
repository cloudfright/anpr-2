import sqlite3
import logging
import json
import re


class Analytics(object):
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)

    
    def get_best_plate(self, ocr_readings):

        """
        Given a dictionary of OCR readings from an event, along the frequency of each plate, perform error correction return the most probable plate
        INPUT: a dictiopnary of OCR readings 
        OUTPUT: a tuple of dateime and the the most likely plate 
        """

        # create a dictionary of the plates and their counts
        try:
            plates = json.loads(ocr_readings)
        except Exception as e:
            logging.critical(f"Error loading json - {e}")
            return None
        
        # sort plate readings by frequency, descending
        sorted_plates = sorted(plates.items(), key=lambda x: x[1], reverse=True)
        # logging.debug(f"Sorted OCR readings: {sorted_ocr_readings}")

        for plate in sorted_plates:
            cleaned_plate = self._cleanPlate(plate[0])

            if self._isValidPlate(cleaned_plate):   #return the first valid plate
                return cleaned_plate

        return None
    

    def _cleanPlate(self, plate):

        """
        we should optimise for post-2001 plates as they are the most common

         post 2001 plates have 2 letters followed by 2 numbers followed by 3 letters
         I, Q or Z should not appear in local memory tags identifiers (the first two letters)
        Q marks are still issued 
         Z is allowed as a random letter

        the two numbers are sometimes mistaken for letters, so we need to do some error correction
        if the third or fourth character is a letter, then we need to convert it back to the most likely numbers
        e.g. 1 = I, 0 = O, 6 = G, 11 = U
        """

        cleaned_plate = plate.replace(" ", "")

        # clean the region identifier in characters third and fourth characters
        if len(cleaned_plate) >= 4:
            for i in range(2, 4):
                if cleaned_plate[i].isalpha():
                    if cleaned_plate[i] == "I":
                        cleaned_plate = f"{cleaned_plate[:i]}1{cleaned_plate[i+1:]}"    # replace I with 1
                    elif cleaned_plate[i] == "O":
                        cleaned_plate = f"{cleaned_plate[:i]}0{cleaned_plate[i+1:]}"    # replace O with 0
                    elif cleaned_plate[i] == "G":
                        cleaned_plate = f"{cleaned_plate[:i]}6{cleaned_plate[i+1:]}"    # replace G with 6
                    elif cleaned_plate[i] == "S":
                        cleaned_plate = f"{cleaned_plate[:i]}5{cleaned_plate[i+1:]}"    # replace S with 5 
                    elif cleaned_plate[i] == "U":
                        cleaned_plate = f"{cleaned_plate[:i]}1{cleaned_plate[i+1:]}"    # replace U with 11
                        cleaned_plate = f"{cleaned_plate[:i+1]}1{cleaned_plate[i+1:]}"

        # TODO clean last three characters - should have no numbers on modern plates

        return cleaned_plate

    def _isValidPlate(self, plate):
        # https://gist.github.com/danielrbradley/7567269 - matches modern, dateless and Irish plates, and diplomatic plates
        plate_pattern = r'(^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$)|(^[A-Z][0-9]{1,3}[A-Z]{3}$)|(^[A-Z]{3}[0-9]{1,3}[A-Z]$)|(^[0-9]{1,4}[A-Z]{1,2}$)|(^[0-9]{1,3}[A-Z]{1,3}$)|(^[A-Z]{1,2}[0-9]{1,4}$)|(^[A-Z]{1,3}[0-9]{1,3}$)|(^[A-Z]{1,3}[0-9]{1,4}$)|(^[0-9]{3}[DX]{1}[0-9]{3}$)'
        return bool(re.match(plate_pattern, plate))

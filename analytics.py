import sqlite3
import logging
import datetime
import json
import re

from persistence import EventPersistence

class Analytics(object):
    def __init__(self):
        self.eventsDB = EventPersistence()
        logging.getLogger().setLevel(logging.DEBUG)

    def getEventsInLast24Hours(self):
        # get the current time minus 24 hours
        start_ts = datetime.datetime.now() - datetime.timedelta(hours=24)        
        start_ts = start_ts.timestamp()
        end_ts = datetime.datetime.now().timestamp()
        return self.eventsDB.get_events(start_ts, end_ts)

    def getEventsInLast7Days(self):
        # get the current time minus 7 days
        start_ts = datetime.datetime.now() - datetime.timedelta(days=7)
        start_ts = start_ts.timestamp()
        end_ts = datetime.datetime.now().timestamp()
        return self.eventsDB.get_events(start_ts, end_ts)
    
    def getEventsInLast30Days(self):
        # get the current time minus 30 days
        start_ts = datetime.datetime.now() - datetime.timedelta(days=30)
        start_ts = start_ts.timestamp()
        end_ts = datetime.datetime.now().timestamp()
        return self.eventsDB.get_events(start_ts, end_ts)
    
    def getBestPlate(self, event):

        # create a dictionary of the plates and their counts
        try:
            ocr_readings = json.loads(event[2])
        except Exception as e:
            logging.critical(f"Error loading json - {e}")
            return None
        
        # sort plate readings by frequency, descending
        sorted_ocr_readings = sorted(ocr_readings.items(), key=lambda x: x[1], reverse=True)
        # logging.debug(f"Sorted OCR readings: {sorted_ocr_readings}")

        for plate in sorted_ocr_readings:
            if self._isValidPlate(plate[0]):
                # logging.debug(f"*** VALID plate : {plate[0]} ***")
                return plate[0]

        # if we get here, we haven't found a valid plate, so return all the ocr readings for this event
        # logging.debug(f"No valid plate found ocr readings are {event[2]}")
        return event[2]
    
    def _isValidPlate(self, plate):
        plate = plate.replace(" ", "")
 
        """
        Need to do some error correction on the plate - most common errors are:
        U = 11
        O = 0
        I = 1
        G = 6   

        if the plate fails the regex, try replacing the above characters with their numeric equivalents
        """


        # https://gist.github.com/danielrbradley/7567269 - matches modern, dateless and Irish plates, and diplomatic plates
        plate_pattern = r'(^[A-Z]{2}[0-9]{2}\s?[A-Z]{3}$)|(^[A-Z][0-9]{1,3}[A-Z]{3}$)|(^[A-Z]{3}[0-9]{1,3}[A-Z]$)|(^[0-9]{1,4}[A-Z]{1,2}$)|(^[0-9]{1,3}[A-Z]{1,3}$)|(^[A-Z]{1,2}[0-9]{1,4}$)|(^[A-Z]{1,3}[0-9]{1,3}$)|(^[A-Z]{1,3}[0-9]{1,4}$)|(^[0-9]{3}[DX]{1}[0-9]{3}$)'
        return bool(re.match(plate_pattern, plate))

analytics = Analytics()
events = analytics.getEventsInLast7Days()
for event in events:
    plate = analytics.getBestPlate(event)
    eventDateTime = datetime.datetime.fromtimestamp(event[0]/1000.0)
    logging.debug(f"{eventDateTime}: {plate}")

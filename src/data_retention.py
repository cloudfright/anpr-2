import os
import schedule
import logging
from datetime import datetime, timedelta

class DataRetentionPolicy(object):

    CAPTURED_FILES_DIR = "./images/capture"
    CAPTURED_IMAGES_RETENTION_DAYS = 2
    ARCHIVED_FILES_DIR = "./images/archive"
    ARCHIVED_IMAGES_RETENTION_DAYS = 30

    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)
        logging.info("Data retention policy scheduler initialized.")
        schedule.every().day.at("10:00").do(self.__cleanup_images)
       
    def __cleanup_images(self):
        logging.info("Checking for images to delete...")
        self._delete_files_older_than(DataRetentionPolicy.CAPTURED_FILES_DIR, DataRetentionPolicy.CAPTURED_IMAGES_RETENTION_DAYS) 
        self._delete_files_older_than(DataRetentionPolicy.ARCHIVED_FILES_DIR, DataRetentionPolicy.ARCHIVED_IMAGES_RETENTION_DAYS) 


    def _delete_files_older_than(self, folder_path, num_days):
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                last_modified = os.path.getmtime(file_path)
                retention_period = datetime.now() - timedelta(days=num_days) 
                if (last_modified < retention_period.timestamp()): 
                    logging.info(f"Deleting {file_path}") 
                    try:
                        os.remove(file_path)
                    except Exception as e:
                        logging.error(f"Error deleting {file_path}: {e}")
                
    def run_data_retention_policy(self):
        schedule.run_pending()
  
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
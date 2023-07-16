# ANPR with anomaly detection 

Using this repo as a starting point..
https://github.com/HarshitDolu/Object-Detection-using-COCO-dataset

1. Capture video input
2. Perform basic object detection using the COCO dataset
3. If movement is detected with an object bounding box and the object is a car, truck or motocycle, write an image to disk
4. OCR the image to extract the number plate or text on the vehicle
5. Write the events to a database
6. Perform anomaly detection on the number plates 
7. Make the results available via a web interface

## Installation
 
- Install Anaconda - python 3.10.4
- Create a new environment - conda create -n <env_name> 
- Activate the environment - conda activate <env_name>
- Intall pip - conda -c conda install pip
- Install paddlepaddle - pip install paddlepaddle or on MacOS M1 - you'll need to follow [these instructions](https://www.paddlepaddle.org.cn/install/quick? docurl=/documentation/docs/en/install/pip/macos-pip_en.html) to install paddlepaddle
- pip install paddleocr this installs an older version of opencv (4.6) which lacks some of the DNN performance improvements since 4.7
- pip install opencv-python --upgrade
- pip install opencv-contrib-python --upgrade

The opencv updrade doesn't appear to hurt paddleocr and the DNN performance improvements are worth it.
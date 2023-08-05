# Introduction

This is a project built on a Rasberry Pi 4 hardware, running a 64-bit Bullseye image. 
Project goals:
- Provide a learning experience covering Python, machine learning, computer vision and AI edge copmuting
- Build a home surveillance tool to capture anomalous number plates
- Focus on privacy: inference and peristentence are on-device, no cloud contact, no unneccessary processing of data

Hardware:
- Rasberry PI 4, 4GB RAM
- Rasberry PI global shutter camera with a 16mm lens (will depend on your field of view)
- Coral AI TPU




## Installation
 
TODO: containerise this, but for now the installation process is cumberome and fragile.

1. Install Raspberry PI OS 64-but, Bullseye. I'm using out-of-the-box Python 3.9.2, but ideally use something like [Pyenv](https://github.com/pyenv/pyenv).
2. Install paddlepaddle using the instructions [here](https://github.com/Qengineering/Paddle-Raspberry-Pi) I chose paddlepaddle-2.4.2-cp39-cp39-linux_aarch64.whl.
3. Install paddleocr using ```pip install paddleocr```. I'm using 2.7.0 at the time of writing. Note you need to downgrade protobuf to 3.20.0 using ```pip install protobuf==3.20.0```.
4. Install Picamera2 using ```sudo apt install -y python3-picamera2``` and you can access these libraries in Python using ```Python -m venv --system-site-packages anpr```
5. Install sqlite with ```sudo apt-get install sqlite3```
6. Reinstall opencv. Paddle OCR required opencv 4.6.0, but that misses out on some new performance improvments. I installed 4.8 using Lindevs [pre-built wheel](https://lindevs.com/install-precompiled-opencv-on-raspberry-pi/) with no side effects.

## How it works

Video is captured via the Pi camera. Basic object detection is performed using OpenCVs DNN (this is currently done on the CPU). If movement is detected and is a car, truck or motocycle, write an image to disk. Form a que of image paths to be processed. In a seperate process, OCR the images to extract the number plate or text on the vehicle. Summarise the OCR results based on confidence and frequency, then write the OCR details to a sqlite database. 

IN PROGRESS:
- Build an API onto the data to get a frequency analysis of plates in a given time period

TODO: 
- Object detection / infernence using Coral TPU
- Anomaly detection of plates based around frequency, length of visit and time of day

## Notes
 - Make sure you have a good PSU for the Pi, I opted for the official Rasberry PI 5.1v, 3A PSU, but before I chose this I had many problems with corrupt SD cards due to underpowwered PSUs.
 - The global shutter camera is great for getting images with no blurring, but the resolution is quite low, you may need to compensate with longer focal length lenses to get closer to the number plate text.
 - Why paddleocr? It currently outperforms Tesseract and EasyOCR.


## Hat tips
There are so many great resources out there and generous people willing to share their knowledge. Here are a few that have guided me so far.
- [Pyimagesearch](https://pyimagesearch.com/) - goldmine of OpenCV information
- [Q-Engineering](https://qengineering.eu/) - advice, guides, images and wheels
- [Lindevs](https://lindevs.com/) - advice and wheels
- [HarshitDolu](https://github.com/HarshitDolu/Object-Detection-using-COCO-dataset) - for a great jumping off point








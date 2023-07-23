import datetime
import cv2
import numpy as np

# MJPG 15fps@3264 x 2448, 30fps@1080P; YUY2 15fps@720P, 20fps@640 x 480
# on a Mac, the backend is CAP_AVFOUNDATION and only 30fps@1080P seems to work (seettings make no difference)
cap=cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# setting camera parameters
# https://docs.opencv.org/4.x/d4/d15/group__videoio__flags__base.html#ggaeb8dd9c89c10a5c63c139bf7c4f5704dab26d2ba37086662261148e9fe93eecad

# cap.set(cv2.CAP_PROP_FRAME_WIDTH,1920)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT,1080)

print("width:",cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print("height:",cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print("fps:",cap.get(cv2.CAP_PROP_FPS))

classNames=[]
classFile='coco.names'
with open(classFile,'rt') as f:
    classNames= f.read().rstrip('\n').split('\n')

#pretrained dnn model
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

#pre set parameters
net = cv2.dnn_DetectionModel(weightsPath,configPath)
net.setInputSize(320,320)
net.setInputScale(1.0/127.5)
net.setInputMean((127.5,127.5,127.5))
net.setInputSwapRB(True)
thres=0.5
nms_threshold=0.2   #(lower,more suppress)

# Maintain accumulation of thresholded differences.
image_acc = None  

# Keep track of previous iteration's timestamp.
tstamp_prev = None  

# alpha value for weighted average
alpha = 0.5
objectsToDetect = ["car", "truck", "motorcycle"]

#detection
while True:
    _,img=cap.read()
    
    if img is None:
        break

    # original_img = img.copy()

    # Convert to grayscale and equalize.
    # grayscale_img= cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # grayscale_img = cv2.equalizeHist(grayscale_img)
    # img = cv2.merge((grayscale_img,grayscale_img,grayscale_img))

  # Initalize accumulation if so indicated.
    if image_acc is None:
        image_acc = np.empty(np.shape(img))

    # Compute difference.
    image_diff = cv2.absdiff(image_acc.astype(img.dtype),img)

    cv2.imshow("diff",image_diff)

    # Accumulate.
    cv2.accumulateWeighted(img,image_acc,alpha)

    classIds, confs, bbox = net.detect(img,confThreshold=thres)

    bbox=list(bbox) #list
    confs= list(np.array(confs).reshape(1,-1)[0])
    confs=list(map(float,confs))  # class 'float'

    # non max suppression
    indices=cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)

    for i in indices:
        box=bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
            
        cv2.rectangle(img,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
        
        objClass = classNames[classIds[i] - 1]
        # show the bounding box and label, and conditional probability on the output image
        text = "{}: {:.4f}".format(objClass, confs[i]) 

        cv2.putText(img, text, (box[0] + 10, box[1] + 30),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

        # Extract the region of interest
        roi = image_diff[y:y+h, x:x+w]

        # Calculate the average pixel value or mean intensity
        average_brightness = cv2.mean(roi)[0]

        if (average_brightness > 10 and objClass in objectsToDetect):
            now = datetime.datetime.now()
            # cv2.imwrite("images-to-label/%s.jpg" % now.strftime("%Y-%m-%d-%H-%M-%S-%f"), img)
            # print("Movement: %s, Index: %d, class %s, brightness %d" % (datetime.datetime.now(), i, text, average_brightness))

    cv2.imshow("output",img)
    cv2.waitKey(1)

# 
import cv2
import numpy as np

cap=cv2.VideoCapture(0)
cap.set(3,640)
cap.set(4,480)



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

#detection
while True:
    success,img=cap.read()
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
        
        # show the bounding box and label, and conditional probability on the output image
        text = "{}: {:.4f}".format(classNames[classIds[i] - 1], confs[i]) 

        cv2.putText(img, text, (box[0] + 10, box[1] + 30),
                       cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

    cv2.imshow("output",img)
    cv2.waitKey(1)

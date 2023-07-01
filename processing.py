import datetime
import cv2
import numpy as np
  
thres=0.6
nms_threshold=0.2   #(lower,more suppress)

def process_frame(frame, t0, net, classNames):
    # some intensive computation...
    # frame = cv.medianBlur(frame, 19)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    # invert the image
    # frame = cv2.bitwise_not(frame)    


    classIds, confs, bbox = net.detect(frame,confThreshold=thres)

    bbox=list(bbox) #list
    confs= list(np.array(confs).reshape(1,-1)[0])
    confs=list(map(float,confs))  # class 'float'

    # non max suppression
    indices=cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)

    for i in indices:
        box=bbox[i]
        x,y,w,h = box[0],box[1],box[2],box[3]
            
    #     cv2.rectangle(frame,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
        objClass = classNames[classIds[i] - 1]
        print(f"{objClass} detected at {datetime.datetime.now()} with confidence {confs[i]}")
    return frame, t0
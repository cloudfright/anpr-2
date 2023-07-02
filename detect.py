import datetime
import cv2
import numpy as np
import logging


class ObjectDetector(object):
    def __init__(self):
        self.classNames=[]
        self.classFile='coco.names'
        with open(self.classFile,'rt') as f:
            self.classNames= f.read().rstrip('\n').split('\n')

        #pretrained dnn model
        self.configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
        self.weightsPath = 'frozen_inference_graph.pb'

        #pre set parameters
        self.net = cv2.dnn_DetectionModel(self.weightsPath,self.configPath)
        self.net.setInputSize(320,320)
        # self.net.setInputSize(160,160)
        # self.net.setInputSize(64,64)

        self.net.setInputScale(1.0/127.5)
        self.net.setInputMean((127.5,127.5,127.5))
        self.net.setInputSwapRB(True)
        self.thres=0.6
        self.nms_threshold=0.2

        # self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        # self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)


        self.objectsToDetect = ['car','truck','motorcycle','bus']
        self.alpha = 0.5
        self.image_acc = None  

    
    def detect_objects(self,frame):

        if self.image_acc is None:
            self.image_acc = np.empty(np.shape(frame))
        
        # Compute difference.
        image_diff = cv2.absdiff(self.image_acc.astype(frame.dtype),frame)

        classIds, confs, bbox = self.net.detect(frame,confThreshold=self.thres)

        bbox=list(bbox)
        confs= list(np.array(confs).reshape(1,-1)[0])
        confs=list(map(float,confs))  # class 'float'

        # non max suppression
        indices=cv2.dnn.NMSBoxes(bbox,confs,self.thres,self.nms_threshold)
        
        # cv2.imshow("diff",image_diff)

         # Accumulate.
        cv2.accumulateWeighted(frame,self.image_acc,self.alpha)

        files = list()
        for i in indices:
            box=bbox[i]
            x,y,w,h = box[0],box[1],box[2],box[3]
            
            objClass = self.classNames[classIds[i] - 1]
            text = "{}: {:.4f}".format(objClass, confs[i]) 

            cv2.rectangle(frame,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
            # cv2.putText(frame, text, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            
            # Calculate the average pixel value or mean intensity
            roi = image_diff[y:y+h,x:x+w]
            average_brightness = cv2.mean(roi)[0]

            if (average_brightness > 10 and objClass in self.objectsToDetect):
                now = datetime.datetime.now()
                object_frame = frame[y:y+h,x:x+w]
                filename = "images/capture/%s.jpg" % now.strftime("%Y-%m-%d-%H-%M-%S-%f")
                files.append(filename)
                cv2.imwrite(filename, object_frame)
                logging.debug("Movement: %s, Index: %d, class %s, brightness %d" % (datetime.datetime.now(), i, text, average_brightness))

        return tuple(files)

# thres=0.6
# nms_threshold=0.2   #(lower,more suppress)

# def process_frame(frame, t0, net, classNames):
#     # some intensive computation...
#     # frame = cv.medianBlur(frame, 19)
#     # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
#     # invert the image
#     # frame = cv2.bitwise_not(frame)    


#     classIds, confs, bbox = net.detect(frame,confThreshold=thres)

#     bbox=list(bbox) #list
#     confs= list(np.array(confs).reshape(1,-1)[0])
#     confs=list(map(float,confs))  # class 'float'

#     # non max suppression
#     indices=cv2.dnn.NMSBoxes(bbox,confs,thres,nms_threshold)

#     for i in indices:
#         box=bbox[i]
#         x,y,w,h = box[0],box[1],box[2],box[3]
            
#     #     cv2.rectangle(frame,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
#         objClass = classNames[classIds[i] - 1]
#         print(f"{objClass} detected at {datetime.datetime.now()} with confidence {confs[i]}")
#     return frame, t0
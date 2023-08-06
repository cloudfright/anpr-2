
from datetime import datetime
import cv2
import numpy as np
import logging
from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils import edgetpu
from pycoral.utils import dataset


class TpuObjectDetector(object):

    DETECT_THRESHOLD = 0.5

    def __init__(self):
    
        self.interpreter = edgetpu.make_interpreter('./data/model/mobilenet_ssd_v2_coco_quant_postprocess_edgetpu.tflite')
        self.interpreter.allocate_tensors()
        self.labels = dataset.read_label_file('./data/model/coco_labels.txt') 
        self.alpha = 0.5
        self.image_acc = None 
        self.objectsToDetect = ['car','truck','motorcycle','bus']

    def detect_objects(self,frame): 
    
        input_frame = cv2.resize(frame, common.input_size(self.interpreter))

        if self.image_acc is None:
            self.image_acc = np.empty(np.shape(frame))

        # Compute difference.
        image_diff = cv2.absdiff(self.image_acc.astype(frame.dtype),frame)

        # Accumulate.
        cv2.accumulateWeighted(frame, self.image_acc, self.alpha)

        common.set_input(self.interpreter, input_frame)
        self.interpreter.invoke()
        objects = detect.get_objects(self.interpreter, score_threshold=TpuObjectDetector.DETECT_THRESHOLD, image_scale=(0.468, 0.625))
        
        filename = None
        for obj in objects:
            x,y,w,h = obj.bbox.xmin, obj.bbox.ymin, obj.bbox.width, obj.bbox.height
            classId = int(obj.id)
            label = self.labels.get(classId, ["unknown"])
            # logging.debug("Object detected: %s, %s %f" % (label, bbox, obj.score))

            roi = image_diff[y:y+h,x:x+w]
            average_brightness = cv2.mean(roi)[0]

            if (average_brightness > 10 and label in self.objectsToDetect):
                now = datetime.now()
                object_frame = frame[y:y+h,x:x+w]
                filename = "./images/capture/%s.jpg" % now.strftime("%Y-%m-%d-%H-%M-%S-%f")
                cv2.imwrite(filename, object_frame)
                logging.debug("Movement: %s, class %s, brightness %d" % (datetime.now(), label, average_brightness))

        return filename
    



        # bbox=list(bbox)
        # confs= list(np.array(confs).reshape(1,-1)[0])
        # confs=list(map(float,confs))  # class 'float'

        # # non max suppression
        # indices=cv2.dnn.NMSBoxes(bbox,confs,self.thres,self.nms_threshold)

        #  # Accumulate.
        # cv2.accumulateWeighted(frame,self.image_acc,self.alpha)

        # filename = None
        # for i in indices:
        #     box=bbox[i]
        #     x,y,w,h = box[0],box[1],box[2],box[3]
            
        #     objClass = self.classNames[classIds[i] - 1]
        #     text = "{}: {:.4f}".format(objClass, confs[i]) 

        #     # cv2.rectangle(frame,(x,y),(x+w,h+y), color=(0, 255, 0), thickness=1)
        #     # cv2.putText(frame, text, (box[0] + 10, box[1] + 30), cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
            
        #     # Calculate the average pixel value or mean intensity
        #     roi = image_diff[y:y+h,x:x+w]
        #     average_brightness = cv2.mean(roi)[0]

        #     if (average_brightness > 10 and objClass in self.objectsToDetect):
        #         now = datetime.now()
        #         object_frame = frame[y:y+h,x:x+w]
        #         filename = "./images/capture/%s.jpg" % now.strftime("%Y-%m-%d-%H-%M-%S-%f")
        #         cv2.imwrite(filename, object_frame)
        #         # logging.debug("Movement: %s, Index: %d, class %s, brightness %d" % (datetime.now(), i, text, average_brightness))

        # return filename
    
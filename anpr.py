import cv2, time
from collections import deque
import logging
from multiprocessing import Process, Manager, Queue
from detect import ObjectDetector
from multiprocessing.pool import ThreadPool
from platereader import PlateReader
from capture import VideoStream
import datetime

"""
Paddle notes

pip install paddleocr
need to install paddlepaddle with the instructions here:
https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/en/install/pip/macos-pip_en.html


Command line values 

Exception: not found any img file in ./images/capture/
(paddle) bendyer@Office anpr-2 % 
paddleocr --image_dir ./images/capture/ --lang en
[2023/07/08 14:00:59] ppocr DEBUG: Namespace(help='==SUPPRESS==', use_gpu=False, use_xpu=False, use_npu=False, ir_optim=True, use_tensorrt=False, min_subgraph_size=15, precision='fp32', gpu_mem=500, image_dir='./images/capture/', page_num=0, det_algorithm='DB', det_model_dir='/Users/bendyer/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer', det_limit_side_len=960, det_limit_type='max', det_box_type='quad', det_db_thresh=0.3, det_db_box_thresh=0.6, det_db_unclip_ratio=1.5, max_batch_size=10, use_dilation=False, det_db_score_mode='fast', det_east_score_thresh=0.8, det_east_cover_thresh=0.1, det_east_nms_thresh=0.2, det_sast_score_thresh=0.5, det_sast_nms_thresh=0.2, det_pse_thresh=0, det_pse_box_thresh=0.85, det_pse_min_area=16, det_pse_scale=1, scales=[8, 16, 32], alpha=1.0, beta=1.0, fourier_degree=5, rec_algorithm='SVTR_LCNet', rec_model_dir='/Users/bendyer/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer', rec_image_inverse=True, rec_image_shape='3, 48, 320', rec_batch_num=6, max_text_length=25, rec_char_dict_path='/Users/bendyer/opt/anaconda3/envs/paddle/lib/python3.10/site-packages/paddleocr/ppocr/utils/en_dict.txt', use_space_char=True, vis_font_path='./doc/fonts/simfang.ttf', drop_score=0.5, e2e_algorithm='PGNet', e2e_model_dir=None, e2e_limit_side_len=768, e2e_limit_type='max', e2e_pgnet_score_thresh=0.5, e2e_char_dict_path='./ppocr/utils/ic15_dict.txt', e2e_pgnet_valid_set='totaltext', e2e_pgnet_mode='fast', use_angle_cls=False, cls_model_dir='/Users/bendyer/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer', cls_image_shape='3, 48, 192', label_list=['0', '180'], cls_batch_num=6, cls_thresh=0.9, enable_mkldnn=False, cpu_threads=10, use_pdserving=False, warmup=False, sr_model_dir=None, sr_image_shape='3, 32, 128', sr_batch_num=1, draw_img_save_dir='./inference_results', save_crop_res=False, crop_res_save_dir='./output', use_mp=False, total_process_num=1, process_id=0, benchmark=False, save_log_path='./log_output/', show_log=True, use_onnx=False, output='./output', table_max_len=488, table_algorithm='TableAttn', table_model_dir=None, merge_no_span_structure=True, table_char_dict_path=None, layout_model_dir=None, layout_dict_path=None, layout_score_threshold=0.5, layout_nms_threshold=0.5, kie_algorithm='LayoutXLM', ser_model_dir=None, re_model_dir=None, use_visual_backbone=True, ser_dict_path='../train_data/XFUND/class_list_xfun.txt', ocr_order_method=None, mode='structure', image_orientation=False, layout=True, table=True, ocr=True, recovery=False, use_pdf2docx_api=False, lang='en', det=True, rec=True, type='ocr', ocr_version='PP-OCRv3', structure_version='PP-StructureV2')

Programmtic values


(paddle) bendyer@Office anpr-2 % /Users/bendyer/opt/anaconda3/envs/paddle/bin/python /Users/bendyer/Documents/Dev/src/anpr-2/anpr.py
[2023/07/08 14:09:24] ppocr DEBUG: Namespace(help='==SUPPRESS==', use_gpu=False, use_xpu=False, use_npu=False, ir_optim=True, use_tensorrt=False, min_subgraph_size=15, precision='fp32', gpu_mem=500, image_dir=None, page_num=0, det_algorithm='DB', det_model_dir='/Users/bendyer/.paddleocr/whl/det/en/en_PP-OCRv3_det_infer', det_limit_side_len=960, det_limit_type='max', det_box_type='quad', det_db_thresh=0.3, det_db_box_thresh=0.6, det_db_unclip_ratio=1.5, max_batch_size=10, use_dilation=False, det_db_score_mode='fast', det_east_score_thresh=0.8, det_east_cover_thresh=0.1, det_east_nms_thresh=0.2, det_sast_score_thresh=0.5, det_sast_nms_thresh=0.2, det_pse_thresh=0, det_pse_box_thresh=0.85, det_pse_min_area=16, det_pse_scale=1, scales=[8, 16, 32], alpha=1.0, beta=1.0, fourier_degree=5, rec_algorithm='SVTR_LCNet', rec_model_dir='/Users/bendyer/.paddleocr/whl/rec/en/en_PP-OCRv3_rec_infer', rec_image_inverse=True, rec_image_shape='3, 48, 320', rec_batch_num=6, max_text_length=25, rec_char_dict_path='/Users/bendyer/opt/anaconda3/envs/paddle/lib/python3.10/site-packages/paddleocr/ppocr/utils/en_dict.txt', use_space_char=True, vis_font_path='./doc/fonts/simfang.ttf', drop_score=0.5, e2e_algorithm='PGNet', e2e_model_dir=None, e2e_limit_side_len=768, e2e_limit_type='max', e2e_pgnet_score_thresh=0.5, e2e_char_dict_path='./ppocr/utils/ic15_dict.txt', e2e_pgnet_valid_set='totaltext', e2e_pgnet_mode='fast', use_angle_cls=True, cls_model_dir='/Users/bendyer/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer', cls_image_shape='3, 48, 192', label_list=['0', '180'], cls_batch_num=6, cls_thresh=0.9, enable_mkldnn=False, cpu_threads=10, use_pdserving=False, warmup=False, sr_model_dir=None, sr_image_shape='3, 32, 128', sr_batch_num=1, draw_img_save_dir='./inference_results', save_crop_res=False, crop_res_save_dir='./output', use_mp=False, total_process_num=1, process_id=0, benchmark=False, save_log_path='./log_output/', show_log=True, use_onnx=False, output='./output', table_max_len=488, table_algorithm='TableAttn', table_model_dir=None, merge_no_span_structure=True, table_char_dict_path=None, layout_model_dir=None, layout_dict_path=None, layout_score_threshold=0.5, layout_nms_threshold=0.5, kie_algorithm='LayoutXLM', ser_model_dir=None, re_model_dir=None, use_visual_backbone=True, ser_dict_path='../train_data/XFUND/class_list_xfun.txt', ocr_order_method=None, mode='structure', image_orientation=False, layout=True, table=True, ocr=True, recovery=False, use_pdf2docx_api=False, lang='en', det=True, rec=True, type='ocr', ocr_version='PP-OCRv3', structure_version='PP-StructureV2')



"""

if __name__ == '__main__':

    logging.getLogger().setLevel(logging.DEBUG)
    
    prev_frame_time = 0
    new_frame_time = 0

    # cap = cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 800)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 600)
    # logging.info("width: %s", cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    # logging.info("height: %s", cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    # logging.info("fps: %s", cap.get(cv2.CAP_PROP_FPS))
    
    # if not cap.isOpened():
    #     logging.critical("Cannot open camera")
    #     exit()

    # create a thread pool to do the ocr processing (leave somme headroom)
    pool = ThreadPool(processes = int(cv2.getNumberOfCPUs() / 2 ))

    detector = ObjectDetector()
    plate_reader = PlateReader()
    frame_queue = deque()

    try:
        # start the video stream
        video_stream = VideoStream(frame_queue, 0)
    except:
        logging.critical("Cannot start video stream")
        exit()

    movement_count = 0
    ocr_queue = deque() 

    while True:
        try:
            # status, frame = cap.read()

            if (len(frame_queue) > 0):
                frame = frame_queue.popleft()
                
                # drop a frame to keep up with the video stream
                if (len(frame_queue) > 0):
                    frame = frame_queue.popleft()

                filename = detector.detect_objects(frame)


                # # test recording frames for blurring
                # now = datetime.datetime.now()
                # filename = "images/capture/%s.jpg" % now.strftime("%Y-%m-%d-%H-%M-%S-%f")
                # cv2.imwrite(filename, frame)

                if filename:
                    # motion detected 
                    movement_count += 1
                    full_filename = f"./{filename}"
                    logging.debug("motion detected")
                    ocr_queue.append(full_filename)
                else:
                    if (movement_count > 0):
                        movement_count -= 1
                    else:    
                        # motion ended                   
                        if len(ocr_queue):
                            logging.debug("motion ended")
                            ocr_list_to_process = []
                            while (len(ocr_queue)):
                                logging.debug(f"ocr_queue len {len(ocr_queue)}")
                                ocr_list_to_process.append(ocr_queue.popleft())
                            result = pool.apply_async(plate_reader.read_plate, args=([ocr_list_to_process]))
                            # result = plate_reader.read_plate(ocr_list_to_process)


                new_frame_time = time.time()
                fps = 1/(new_frame_time-prev_frame_time)
                prev_frame_time = new_frame_time
                fps = int(fps)  
                fps = str(fps)
                # print(fps)

                # print(len(frame_queue))
                # cv2.putText(frame, fps, (7, 70), cv2.FONT_HERSHEY_SIMPLEX, 3, (100, 255, 0), 3, cv2.LINE_AA)
                # cv2.imshow('frame', frame)

            key = cv2.waitKey(1)
            if key == ord('q'):
                # cap.release()
                video_stream.release()
                cv2.destroyAllWindows()
                exit(1)

        except AttributeError:
            pass


# OPENMP error on mac https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
# export KMP_DUPLICATE_LIB_OK=TRUE
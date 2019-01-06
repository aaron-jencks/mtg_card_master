#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=C0103
# pylint: disable=E1101

import sys
import time
import numpy as np
import tensorflow as tf
import cv2

from utils.models import label_map_util
from utils import visualization_utils_color as vis_util
from utils.models.model_util import TensorflowFaceDetector

# Path to frozen detection graph. This is the actual model that is used for the object detection.
PATH_TO_CKPT = './card_identifier/model/current/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = './card_identifier/labelmap.pbtxt'

NUM_CLASSES = 2

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print ("usage:%s (cameraID | filename) Detect faces\
 in the video example:%s 0"%(sys.argv[0], sys.argv[0]))
        exit(1)

    try:
    	camID = int(sys.argv[1])
    except:
    	camID = sys.argv[1]
    
    tDetector = TensorflowFaceDetector(PATH_TO_CKPT)

    cap = cv2.VideoCapture(camID)
    windowNotSet = True
    while True:
        ret, image = cap.read()
        if ret == 0:
            break

        [h, w] = image.shape[:2]
        #print (h, w)
        image = cv2.flip(image, 1)

        (boxes, scores, classes, num_detections) = tDetector.run(image)

        vis_util.visualize_boxes_and_labels_on_image_array(
            image,
            np.squeeze(boxes),
            np.squeeze(classes).astype(np.int32),
            np.squeeze(scores),
            category_index,
            use_normalized_coordinates=True,
            line_thickness=4)

        if windowNotSet is True:
            cv2.namedWindow("tensorflow based (%d, %d)" % (w, h), cv2.WINDOW_NORMAL)
            windowNotSet = False

        cv2.imshow("tensorflow based (%d, %d)" % (w, h), image)
        k = cv2.waitKey(1) & 0xff
        if k == ord('q') or k == 27:
            break

    cap.release()

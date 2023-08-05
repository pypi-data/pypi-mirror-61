import time
import os
import numpy as np
import matplotlib.pyplot as plt
import cv2
from collections import Counter
import tensorflow as tf
import json

import model as modellib
import csku

import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE

def get_inference_config():
    config = csku.CSKUConfig()
    class InferenceConfig(config.__class__):
        # Run detection on one image at a time
        GPU_COUNT = 1
        IMAGES_PER_GPU = 1

    config = InferenceConfig()
    return config


def get_csku_tag(csku_product_ids):

    csku_product_ids.sort()

    csku_product_ids_to_str = [str(i) for i in csku_product_ids]
    csku_tag = '_'
    csku_tag = csku_tag.join(csku_product_ids_to_str)

    return csku_tag

def load_csku_model(MODEL_DIR, config, csku_tag):

    LOGI('[INFO] Inside load_model')

    DEVICE = "/gpu:0"

    st = time.time()
    with tf.device(DEVICE):
        model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR,
                                  config=config)
    et = time.time()
    print('[TIME] model creation time %f s' % (et - st))

    st = time.time()
    # Or, load the last model you trained
    # weights_path = model.find_last()[1]
    weights_path = os.path.join(MODEL_DIR, "mask_rcnn_" + csku_tag + ".h5")

    if(not os.path.exists(weights_path)):
        LOGE("[ERROR] %s does not exists"%weights_path)
        model = -1
        return model

    # Load weights
    print("Loading weights ", weights_path)
    model.load_weights(weights_path, by_name=True)
    et = time.time()
    print('[TIME] model weight load time %f s' % (et - st))

    return model


def load_all_csku_models(pd_config_path, models_path, config):
    models = {}

    with open(pd_config_path) as config_buffer:
        pd_config = json.load(config_buffer)

    st = time.time()
    for model_no in pd_config.keys():

        if(pd_config[model_no]["algo"] != 2):
            continue

        LOGI("Loading model %s details" % model_no)

        models[model_no] = {}

        product_ids = pd_config[model_no]['product_ids']

        models[model_no]['product_ids'] = product_ids

        csku_tag = get_csku_tag(product_ids)
        csku_model = load_csku_model(models_path, config, csku_tag)

        models[model_no]['model'] = csku_model

    et = time.time()
    LOGI('[TIME] Product differentiation models loading time is %d seconds' % (et - st))

    return models


def get_model_products_id_mapping(csku_product_ids):
    model_products_id_mapping = ['BG']

    for product_id in csku_product_ids:
        model_products_id_mapping.append(str(product_id))

    return model_products_id_mapping


def get_frames_from_txn_video(txn_video):
    st = time.time()

    algo_tot_frames = 50

    frames = []

    txn_video_data = cv2.VideoCapture(txn_video)
    if (not txn_video_data.isOpened()):
        LOGE('[ERROR] txn_video %s path has some issue, please check' % txn_video)
        rsz_factor = -1
        return frames

    # frame_width = txn_video_data.get(cv2.CAP_PROP_FRAME_WIDTH)
    # frame_height = txn_video_data.get(cv2.CAP_PROP_FRAME_HEIGHT)

    txn_video_data.set(cv2.CAP_PROP_POS_MSEC, 0)

    while True:
        flag, frame_bgr = txn_video_data.read()

        if not flag:
            break

        # Originial video frames
        frame = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        frames.append(frame)

    tot_frames = len(frames)
    # LOGI('[VALUE] Total frames in the video are %d' % tot_frames)

    frames_skip_step = max(int(tot_frames / algo_tot_frames), 1)
    frames_skipped = frames[0:tot_frames:frames_skip_step]

    # LOGI('[VALUE] Total frames in the video after skipping are %d' % len(frames_skipped))

    et = time.time()
    # LOGI('[TIME] Frames extraction time is %d seconds' % (et - st))

    return frames_skipped

def get_pred_product_cnts(product_instances_cnt, wght_products_cnt, model_products_id_mapping):

    # Get the count of total predicted product instances
    tot_pred_prod_cnt = len(product_instances_cnt)

    pred_product_cnts = {}

    # If there is atleast one product in the transaction video
    if(tot_pred_prod_cnt > 0):

        k = Counter(product_instances_cnt)

        # Finding 3 highest values
        top_instances = k.most_common(wght_products_cnt)
    #     print(top_instances)

        # If wght_products_cnt is greater than tot predicted instance counts.
        # Then we are assigning the difference products as the top most product
        if (tot_pred_prod_cnt < wght_products_cnt):
            LOGI('[WARNING] Algorithm predicted %d products while weight product count is %d'%(tot_pred_prod_cnt, wght_products_cnt))
            instance = top_instances[0]
            class_id, _ = instance[0].split('_')
            class_id = int(class_id)
            product_id = model_products_id_mapping[class_id]
            pred_product_cnts[product_id] = wght_products_cnt - tot_pred_prod_cnt

        for instance in top_instances:
            class_id, _ = instance[0].split('_')
            class_id = int(class_id)

            product_id = model_products_id_mapping[class_id]
            if(product_id in pred_product_cnts.keys()):
                pred_product_cnts[product_id] = pred_product_cnts[product_id]+1
            else:
                pred_product_cnts[product_id] = 1
    #If there is no product in the transaction video
    else:
        LOGI('[WARNING] Algorithm did not predict any product. Assigning product as default value')
        product_id = model_products_id_mapping[1]
        pred_product_cnts[product_id] = wght_products_cnt

    return pred_product_cnts

def predict_products_in_txn(txn_video, wght_products_cnt, model, model_products_id_mapping, plot_flag=0):

    st = time.time()

    product_instances_cnt = {}

    frames = get_frames_from_txn_video(txn_video)

    for frame in frames:
        results = model.detect([frame], verbose=0)

        r = results[0]

        instance_count = np.zeros((3), dtype=int)
        for class_id in r['class_ids']:
            instance_count[class_id] = instance_count[class_id] + 1
            key_tag = str(class_id) + '_' + str(instance_count[class_id])

            if (key_tag in product_instances_cnt.keys()):
                product_instances_cnt[key_tag] = product_instances_cnt[key_tag] + 1
            else:
                product_instances_cnt[key_tag] = 1

        if (plot_flag):

            frame_products = frame.copy()
            pred_bboxs = r['rois']
            pred_classes = r['class_ids']
            for pred_ind in range(len(pred_bboxs)):
                pred_box = pred_bboxs[pred_ind]
                pred_class_id = pred_classes[pred_ind]
                thickness = 6
                if(pred_class_id == 1):
                    color = (0, 255, 0)
                elif (pred_class_id == 2):
                    color = (255, 0, 0)
                else:
                    color = (255, 255, 255)
                frame_products = cv2.rectangle(frame_products, (pred_box[1], pred_box[0]), (pred_box[3], pred_box[2]), color, thickness)

            plt.figure(figsize=(12, 8))
            plt.imshow(frame_products)
            plt.show()

            LOGI("r['class_ids'] %s" % str(r['class_ids']))

    pred_product_cnts = get_pred_product_cnts(product_instances_cnt, wght_products_cnt, model_products_id_mapping)


    if (plot_flag):
        LOGI('Product instances count: %s' % str(product_instances_cnt))
        LOGI('pred_product_cnts = %s' % (str(pred_product_cnts)))

    et = time.time()
    # LOGI('[TIME] Products prediction in a transaction time is %d seconds' % (et - st))

    return pred_product_cnts, product_instances_cnt
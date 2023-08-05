import time
import json
import os
import cv2
import numpy as np
import pickle
import matplotlib.pyplot as plt

from keras.models import load_model
from keras.applications.vgg19 import preprocess_input
from keras.models import Model

from inference_utils.utils import get_yolo_boxes
import inference_config


import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE


# With product detection model load
def load_with_product_model(config_path, models_path):

    LOGI('[INFO] %s'%config_path)
    with open(config_path) as config_buffer:
        config = json.load(config_buffer)

    #   Load the model
    os.environ['CUDA_VISIBLE_DEVICES'] = config['train']['gpus']

    st = time.time()
    infer_model = load_model(os.path.join(models_path, config['train']['saved_weights_name']))
    et = time.time()
    LOGI('[TIME] Product localization model loading time is %d seconds' % (et - st))

    return infer_model, config


# Product differentiation models load
def load_pd_models(pd_config_path, models_path):

    models = {}

    with open(pd_config_path) as config_buffer:
        pd_config = json.load(config_buffer)

    st = time.time()
    for model_no in pd_config.keys():

        if (pd_config[model_no]["algo"] != 1):
            continue

        LOGI("Loading model %s details" % model_no)
        models[model_no] = {}

        product_labels = pd_config[model_no]['product_ids']

        temp_list = [str(i) for i in product_labels]
        combination_sku_tag = '_'.join(temp_list)

        models[model_no]['product_labels'] = product_labels
        models[model_no]['sigma_multiplier'] = pd_config[model_no]['sigma_multiplier']
        # pd_model = load_model(os.path.join(models_path, pd_config[model_no]['model_name']))
        pd_model = load_model(os.path.join(models_path, combination_sku_tag + '_nn_model.h5'))
        models[model_no]['model'] = Model(inputs=pd_model.input, outputs=[pd_model.layers[-2].output, pd_model.output])


        logits_stats_pkl = os.path.join(models_path, combination_sku_tag+'_logits_stats.pkl')
        with open(logits_stats_pkl, 'rb') as f:
            logits_stats = pickle.load(f)

        models[model_no]['logits_stats'] = logits_stats

    et = time.time()
    LOGI('[TIME] Product differentiation models loading time is %d seconds' % (et - st))

    return models


def load_pd_model_with_model_no(pd_config_path, models_path, model_no):

    st = time.time()

    with open(pd_config_path) as config_buffer:
        pd_config = json.load(config_buffer)

    product_labels = pd_config[model_no]['product_ids']

    temp_list = [str(i) for i in product_labels]
    combination_sku_tag = '_'.join(temp_list)

    pd_model = load_model(os.path.join(models_path, combination_sku_tag + '_nn_model.h5'))
    debug_model = Model(inputs=pd_model.input, outputs=[pd_model.layers[-2].output, pd_model.output])

    logits_stats_pkl = os.path.join(models_path, combination_sku_tag + '_logits_stats.pkl')
    with open(logits_stats_pkl, 'rb') as f:
        logits_stats = pickle.load(f)

    sigma_multiplier = pd_config[model_no]['sigma_multiplier']
    product_labels = pd_config[model_no]['product_ids']

    et = time.time()
    LOGI('[TIME] Product differentiation model loading time is %d seconds' % (et - st))

    return debug_model, product_labels, logits_stats, sigma_multiplier, combination_sku_tag

#Gets frames and frames_rsz from the transaction video
def get_frames_from_txn_video(txn_video):

    st = time.time()

    trained_image_width = inference_config.trained_image_width
    trained_image_height = inference_config.trained_image_height

    algo_tot_frames = inference_config.algo_tot_frames

    frames = []
    frames_rsz = []
    rsz_factor = 1

    txn_video_data = cv2.VideoCapture(txn_video)
    if (not txn_video_data.isOpened()):
        LOGE('[ERROR] txn_video %s path has some issue, please check' % txn_video)
        rsz_factor = -1
        return frames, frames_rsz, rsz_factor

    frame_width = txn_video_data.get(cv2.CAP_PROP_FRAME_WIDTH)
    frame_height = txn_video_data.get(cv2.CAP_PROP_FRAME_HEIGHT)

    if (frame_width <= 320 and frame_height <= 240):
        LOGI("[INFO] No need to resize image")
    else:
        width_ratio = int(frame_width / trained_image_width)
        height_ratio = int(frame_height / trained_image_height)
        rsz_factor = min(width_ratio, height_ratio)
        rsz_frame_width = int(frame_width / rsz_factor)
        rsz_frame_height = int(frame_height / rsz_factor)
        LOGI("[INFO] Resize required from (%d X %d) to (%d X %d)" % (
            frame_width, frame_height, rsz_frame_width, rsz_frame_height))

    txn_video_data.set(cv2.CAP_PROP_POS_MSEC, 0)

    while True:
        flag, frame = txn_video_data.read()

        if not flag:
            break

        if (rsz_factor > 1):
            frame_rsz = cv2.resize(frame, (rsz_frame_width, rsz_frame_height))
            frames_rsz.append(frame_rsz)
        else:
            frames_rsz.append(frame)

        #Originial video frames
        frames.append(frame)

    tot_frames = len(frames)
    LOGI('[VALUE] Total frames in the video are %d' % tot_frames)

    frames_skip_step = max(int(tot_frames / algo_tot_frames), 1)
    frames_skipped = frames[0:len(frames):frames_skip_step]
    frames_rsz_skipped = frames_rsz[0:len(frames_rsz):frames_skip_step]

    LOGI('[VALUE] len(frames_skipped) =  %d len(frames_rsz_skipped) =  %d' % (len(frames_skipped), len(frames_rsz_skipped)))

    et = time.time()
    LOGI('[TIME] Frames extraction time is %d seconds' % (et - st))

    return frames_skipped, frames_rsz_skipped, rsz_factor


#With product frames and corresponding boxes prediction
def get_with_product_box_coords(frames_rsz, infer_model, config):

    #   Set some parameter
    net_h, net_w = 416, 416  # a multiple of 32, the smaller the faster
    obj_thresh, nms_thresh = 0.5, 0.45

    st = time.time()

    batch_boxes = get_yolo_boxes(infer_model, frames_rsz, net_h, net_w, config['model']['anchors'],
                                     obj_thresh,
                                     nms_thresh)


    et = time.time()
    LOGI('[TIME] Processing time for predicting product localization is %d seconds' % (et - st))

    return batch_boxes

def get_model_no(txn_video_product_id, pd_config):

    model_no = -1
    for model_id in pd_config.keys():
        product_ids = pd_config[model_id]['product_ids']
        for product_id in product_ids:
            product_id_str = str(product_id)
            if (product_id_str in txn_video_product_id):
                model_no = model_id

    return model_no

def get_model_no_product_names_list(product_names_list, pd_config):

    # -6 is a dummy initialization
    model_no = -6
    for product_id_in_list in product_names_list:
        product_id_str = str(product_id_in_list)
        temp_model_no = get_model_no(product_id_str, pd_config)

        # Check if dummy initialization has been over written
        if(model_no == -6):
            model_no = temp_model_no
            continue

        # Check if product ids have returned same model number or not, otherwise return -1
        if(model_no != temp_model_no):
            model_no = -1
            return model_no

    return model_no

def predict_product_id(frames, batch_boxes, product_names_list, pd_model, logits_stats, sigma_multiplier, rsz_factor, show_plot = 0):

    #show_plot = 1 --> Plot entire frame with product box and product plot
    #show_plot = 2 --> Plot only entire frame with products

    # Product resized width and height
    resize_width = inference_config.prod_resize_width
    resize_height = inference_config.prod_resize_height

    # Number of products in a combination sku
    tot_prods = len(product_names_list)

    product_cnt = np.zeros((tot_prods), dtype=np.int)
    product_actual_pred = np.zeros((tot_prods), dtype=np.float)
    # product patch actual prediction sigmoid values
    product_actual_preds = []

    product1_logit_th = min(logits_stats["u1"] + (sigma_multiplier*logits_stats["sigma1"]), 0)
    product2_logit_th = max(logits_stats["u2"] - (sigma_multiplier*logits_stats["sigma2"]), 0)

    border_thickness = 3
    if(rsz_factor > 1):
        border_thickness = border_thickness * rsz_factor

    st = time.time()
    tot_product_patches = 0
    for frame_no in range(len(frames)):
        frame = frames[frame_no]
        plot_flag = 0
        if(show_plot >= 1):
            img_pred = frame.copy()
        if(show_plot == 2):
            pred_tag = ' pred:'
        for box in batch_boxes[frame_no]:
            # label 2 indicates with product
            if (box.get_score() > 0.5 and box.get_label() == 2):
                if (rsz_factor > 1):
                    top = (box.ymin) * rsz_factor
                    bottom = (box.ymax) * rsz_factor
                    left = (box.xmin) * rsz_factor
                    right = (box.xmax) * rsz_factor
                else:
                    top = (box.ymin)
                    bottom = (box.ymax)
                    left = (box.xmin)
                    right = (box.xmax)

                crop_img = frame[top:bottom, left:right]
                if (crop_img.shape[0] < 5 or crop_img.shape[1] < 5):
                    continue
                resizeimg = cv2.resize(crop_img, (resize_width, resize_height))
                if(show_plot >=1):
                    product_rsz_img = resizeimg.copy()
                resizeimg = resizeimg[:, :, [2, 1, 0]]
                resizeimg = resizeimg.reshape(1, resize_height, resize_width, 3)
                resizeimg = preprocess_input(resizeimg)

                # yhat_actual_pred = pd_model.predict(resizeimg)
                [yhat_logit, yhat_actual_pred] = pd_model.predict(resizeimg)
                if ((yhat_logit > product1_logit_th) and (yhat_logit < product2_logit_th)):
                    continue

                yhat_actual_pred = np.asscalar(np.array(yhat_actual_pred))

                yhat = int(np.round(yhat_actual_pred))
                product_cnt[yhat] = product_cnt[yhat] + 1
                product_actual_pred[yhat] = product_actual_pred[yhat] + (yhat_actual_pred)

                product_actual_preds.append(yhat_actual_pred)

                if(show_plot == 1):
                    plt.subplot(1, 2, 1)
                    cv2.rectangle(img=img_pred, pt1=(left, top), pt2=(right, bottom), color=(0, 159, 255),
                                  thickness=border_thickness)
                    plt.imshow(cv2.cvtColor(img_pred, cv2.COLOR_BGR2RGB))
                    plt.title('frame_no: ' + str(frame_no) + ' pred:' + str(product_names_list[yhat]))
                    plt.subplot(1, 2, 2)
                    plt.imshow(cv2.cvtColor(product_rsz_img, cv2.COLOR_BGR2RGB))
                    plt.title('yhat_logit: ' + str(yhat_logit) + ' pred:' + str(product_names_list[yhat]))
                    plt.show()
                    plot_flag = 1
                if(show_plot == 2):
                    cv2.rectangle(img=img_pred, pt1=(left, top), pt2=(right, bottom), color=(0, 159, 255),
                                  thickness=border_thickness)
                    pred_tag = pred_tag+' '+str(product_names_list[yhat])

                tot_product_patches = tot_product_patches + 1

        if(show_plot >= 1 and plot_flag == 0):
            plt.imshow(cv2.cvtColor(img_pred, cv2.COLOR_BGR2RGB))
            plt.title('frame_no: ' + str(frame_no)+pred_tag)
            plt.show()

    LOGI('[VALUE] Total product patches are %d' % tot_product_patches)

    if (np.sum(product_cnt) == 0):
        pred_label = -1
        pred_prob = 0
    else:
        pred_index = np.argmax(product_cnt)
        pred_label = product_names_list[pred_index]
        pred_prob = (product_cnt[pred_index] / np.sum(product_cnt)) * 100

        for prod_index in range(tot_prods):
            if (product_cnt[prod_index] > 0):
                product_actual_pred[prod_index] = product_actual_pred[prod_index] / product_cnt[prod_index]
            else:
                product_actual_pred[prod_index] = 0

    et = time.time()
    LOGI('[TIME] Processing time for product differentiation is %d seconds' % (et - st))

    #         LOGI('[VALUE] Product patch predictions')
    #         LOGI(product_actual_preds)
    LOGI('[VALUE] product frames count %s: %d and %s: %d' % (
        product_names_list[0], product_cnt[0], product_names_list[1], product_cnt[1]))

    return pred_label, pred_prob


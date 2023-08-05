import os
import sys
import oss2
import json
import time
import ntpath
from itertools import islice

import inference_config
import algo2_inference_utils

import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE
logging.basicConfig(filename='model_updates_logs_file.log', filemode='w', format='%(name)s %(asctime)s %(message)s', level=logging.INFO)

pd_config_path = os.path.join(inference_config.models_path, 'pd_config.json')
models_path = inference_config.models_path
models_version_path = os.path.join(models_path, inference_config.model_version_file)

object_base_path = inference_config.object_base_path

print('[INFO Running download_updated_model_files.py script')


def percentage(consumed_bytes, total_bytes):
    if total_bytes:
        rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
        print('\r{0}% '.format(rate), end='')
        sys.stdout.flush()

def save_as_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f)

def download_model_from_cloud(cloud_object_path, local_path):
    LOGI('Downloading from %s'%cloud_object_path)
    LOGI('Downloading to %s'%local_path)
    bucket.get_object_to_file(cloud_object_path, local_path, progress_callback=percentage)

def download_updated_model_files(pd_config_path, models_version_path, models_path):

    LOGI('[INFO] Inside download_updated_model_files module')

    with open(pd_config_path) as config_buffer:
        pd_config = json.load(config_buffer)

    if(os.path.exists(models_version_path)):
        with open(models_version_path) as config_buffer:
            models_version = json.load(config_buffer)
    else:
        models_version = {}


    st = time.time()
    updated_models = 0
    for model_no in pd_config.keys():

        model_product_ids = pd_config[model_no]["product_ids"]
        csku_tag = algo2_inference_utils.get_csku_tag(model_product_ids)
        version = pd_config[model_no]["model_version"]


        if(csku_tag in models_version.keys()):
            if(models_version[csku_tag] == version):
                LOGI("[INFO] We already have the %s model version for %s"%(version, csku_tag))
                continue

        updated_models +=1
        LOGI('[INFO] Downloading model for %s with version %s' % (csku_tag, version))

        ver_folder = "ver"+version

        if (pd_config[model_no]["algo"] == 1):
            model_file = csku_tag + '_nn_model.h5'
            stat_file = csku_tag + '_logits_stats.pkl'

            # Download model file locally
            object_path = os.path.join(object_base_path, csku_tag, ver_folder, model_file)
            local_path = os.path.join(models_path, model_file)
            download_model_from_cloud(object_path, local_path)

            # Download statisitics file locally
            object_path = os.path.join(object_base_path, csku_tag, ver_folder, stat_file)
            local_path = os.path.join(models_path, stat_file)
            download_model_from_cloud(object_path, local_path)

        elif (pd_config[model_no]["algo"] == 2):
            model_file = "mask_rcnn_" + csku_tag + ".h5"

            # Download model file locally
            object_path = os.path.join(object_base_path, csku_tag, ver_folder, model_file)
            local_path = os.path.join(models_path, model_file)
            download_model_from_cloud(object_path, local_path)

        else:
            LOGE("[ERROR] Improper algorithm number")

        models_version[csku_tag] = version
        save_as_json(models_version_path, models_version)

    et = time.time()
    LOGI('[TIME] Time taken to download %d model files %d seconds' % (updated_models, et - st))




# Accesing storage bucket
auth = oss2. Auth('LTAI4FndnVDqYK8H9pmySzL2', 'g9sswDemaxNwDeDkl0GqzPjd6SroCM')
bucket = oss2. Bucket(auth, 'http://oss-ap-south-1.aliyuncs.com', 'kwik24-ai')


download_updated_model_files(pd_config_path, models_version_path, models_path)





import os
import time
from pathlib import Path

from keras import backend as K

from inference_utils.inference_support_fns import *


import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE


class CSKUAlgo1:

    # BB --> BigBasket 19F28 --> Year, Month and Date
    API_VERSION = 'BB_19K11'

    api_path = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(Path(api_path).parents[0], 'models')

    config_path = os.path.join(models_path, 'config.json')
    pd_config_path = os.path.join(models_path, 'pd_config.json')

    infer_model = None
    models = None
    config = None

    # Initialization will be done only in begining
    init_flag = True
    def init(self):

        st = time.time()

        LOGI('Algo1 API Version: %s' % (self.API_VERSION))
        LOGI('Model Initialization')
        K.clear_session()

        models_path = self.models_path
        config_path = self.config_path
        pd_config_path = self.pd_config_path

        infer_model, config = load_with_product_model(config_path, models_path)
        models = load_pd_models(pd_config_path, models_path)

        self.models = models
        self.infer_model = infer_model
        self.config = config
        self.init_flag = False

        et = time.time()
        LOGI('[TIME] Combination SKU init module time %d seconds' % (et - st))

    def predict(self, txn_video, model_no):

        #If init module has been not called before
        if (self.init_flag):
            # Load with and without product model, product differentiation model
            self.init()

        infer_model = self.infer_model
        models = self.models
        pd_model = models[str(model_no)]['model']
        config = self.config
        product_labels = self.models[str(model_no)]['product_labels']
        logits_stats = self.models[str(model_no)]['logits_stats']
        sigma_multiplier = self.models[str(model_no)]['sigma_multiplier']

        st = time.time()

        # Extract frames from the transaction video
        frames, frames_rsz, rsz_factor = get_frames_from_txn_video(txn_video)

        #Identify product localization
        batch_boxes = get_with_product_box_coords(frames_rsz, infer_model, config)

        #predict product label from the combination sku products list
        pred_label, pred_prob = predict_product_id(frames, batch_boxes, product_labels, pd_model, logits_stats, sigma_multiplier, rsz_factor)

        if(pred_label == -1):
            LOGI('[WARNING] Algorithm did not predict any product. Assigning product as default value')
            pred_label = product_labels[0]

        et = time.time()
        LOGI('[TIME] Combination SKU predict module time %d seconds' % (et - st))


        return pred_label, pred_prob



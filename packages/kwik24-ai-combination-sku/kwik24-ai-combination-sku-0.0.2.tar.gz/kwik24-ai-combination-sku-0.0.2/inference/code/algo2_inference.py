import os
import time
from pathlib import Path

import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE

from algo2_inference_utils import *

class CSKUAlgo2:

    # BB --> BigBasket 19F28 --> Year, Month and Date
    API_VERSION = 'BB_20A09'

    api_path = os.path.dirname(os.path.abspath(__file__))
    models_path = os.path.join(Path(api_path).parents[0], 'models')

    pd_config_path = os.path.join(models_path, 'pd_config.json')

    infer_model = None
    models = None

    # Initialization will be done only in begining
    init_flag = True
    def init(self):

        st = time.time()

        LOGI('Algo2 API Version: %s' % (self.API_VERSION))
        LOGI('Model Initialization')

        models_path = self.models_path
        pd_config_path = self.pd_config_path

        config = get_inference_config()
        models = load_all_csku_models(pd_config_path, models_path, config)


        self.models = models
        self.init_flag = False

        et = time.time()
        LOGI('[TIME] Combination SKU (Algo2) init module time %d seconds' % (et - st))

    def predict(self, txn_video, wght_products_cnt, model_no):

        st = time.time()

        #If init module has been not called before
        if (self.init_flag):
            # Load all the models of algo2
            self.init()

        models = self.models
        csku_model = models[str(model_no)]['model']

        csku_product_ids = self.models[str(model_no)]['product_ids']
        model_products_id_mapping = get_model_products_id_mapping(csku_product_ids)


        pred_product_cnts, product_instances_cnt = predict_products_in_txn(txn_video, wght_products_cnt, csku_model,
                                                                           model_products_id_mapping, plot_flag=0)

        LOGI('Product instances count: %s' % str(product_instances_cnt))
        # LOGI('pred_product_cnts = %s' % (str(pred_product_cnts)))

        et = time.time()
        LOGI('[TIME] Combination SKU predict module time %d seconds' % (et - st))

        return pred_product_cnts


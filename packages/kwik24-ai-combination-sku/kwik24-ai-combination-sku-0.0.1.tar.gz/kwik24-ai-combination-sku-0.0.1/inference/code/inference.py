#Algorithm1 support files
from algo1_inference import CSKUAlgo1

#Algorithm2 support files
from algo2_inference import CSKUAlgo2

import logging
from logging import info as LOGI
from logging import debug as LOGD
from logging import error as LOGE

class CombinationSKU:

    # This dictionary contains objetcs of the algorithms
    csku_algo_objects = None
    init_flag = True

    def init(self):

        csku_algo_objects = {}

        # Create instance of algo1
        csku_algo1 = CSKUAlgo1()

        # Create instance of algo2
        csku_algo2 = CSKUAlgo2()

        csku_algo1.init()
        csku_algo2.init()

        csku_algo_objects['algo1'] = csku_algo1
        csku_algo_objects['algo2'] = csku_algo2

        self.csku_algo_objects = csku_algo_objects
        self.init_flag = False

        pass

    def predict(self, txn_video, wght_products_cnt, model_no, algo_no):

        # If init module has been not called before
        if (self.init_flag):
            # Load all the models of algo2
            self.init()

        pred_product_cnts = {}

        csku_algo1 = self.csku_algo_objects['algo1']
        csku_algo2 = self.csku_algo_objects['algo2']

        if(algo_no == 1):
            LOGI('[INFO] Predict product using algo1')
            pred_label, pred_prob = csku_algo1.predict(txn_video, model_no)
            pred_product_cnts = {}
            pred_product_cnts[str(pred_label)] = wght_products_cnt

        elif(algo_no == 2):
            LOGI('[INFO] Predict product using algo2')
            pred_product_cnts = csku_algo2.predict(txn_video, wght_products_cnt, model_no)
        else:
            LOGE("[ERROR] %d algorithm no. is not supported. Please check" %algo_no)

        LOGI('pred_product_cnts = %s' % (str(pred_product_cnts)))

        return pred_product_cnts

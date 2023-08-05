"""
Mask R-CNN
Train on the toy Balloon dataset and implement color splash effect.

Copyright (c) 2018 Matterport, Inc.
Licensed under the MIT License (see LICENSE for details)
Written by Waleed Abdulla

------------------------------------------------------------

Usage: import the module (see Jupyter notebooks for examples), or run from
       the command line as such:

    # Train a new model starting from pre-trained COCO weights
    python3 csku.py train --dataset=/path/to/balloon/dataset --weights=coco

    # Resume training a model that you had trained earlier
    python3 csku.py train --dataset=/path/to/balloon/dataset --weights=last

    # Train a new model starting from ImageNet weights
    python3 csku.py train --dataset=/path/to/balloon/dataset --weights=imagenet

    # Apply color splash to an image
    python3 csku.py splash --weights=/path/to/weights/file.h5 --image=<URL or path to file>

    # Apply color splash to video using the last weights you trained
    python3 csku.py splash --weights=last --video=<URL or path to file>
"""

import os
import json
import numpy as np
import skimage.draw

# Import Mask RCNN
from config import Config
import utils


############################################################
#  Configurations
############################################################


class CSKUConfig(Config):
    """Configuration for training on the toy  dataset.
    Derives from the base Config class and overrides some values.
    """
    # Give the configuration a recognizable name
    NAME = "csku"

    # We use a GPU with 12GB memory, which can fit two images.
    # Adjust down if you use a smaller GPU.
    IMAGES_PER_GPU = 1

    # Number of classes (including background)
    NUM_CLASSES = 1 + 2  # Background + product1 + product2

    # Number of training steps per epoch
    STEPS_PER_EPOCH = 100

    # Skip detections with < 90% confidence
    DETECTION_MIN_CONFIDENCE = 0.9


############################################################
#  Dataset
############################################################

class CSKUDataset(utils.Dataset):

    def load_csku(self, dataset_dir, subset, csku_product_ids, csku_tag):
        """Load a subset of the Balloon dataset.
        dataset_dir: Root directory of the dataset.
        subset: Subset to load: train or val
        """
        # # Add classes. We have only one class to add.
        # self.add_class("csku", 1, "276214")
        # self.add_class("csku", 2, "100401160")

        for ind in range(len(csku_product_ids)):
            self.add_class("csku", ind+1, str(csku_product_ids[ind]))

        annotations = json.load(open(os.path.join(os.path.dirname(dataset_dir), "meta_data", "via_"+csku_tag+"_"+subset+".json")))

        # Train or validation dataset?
        # assert subset in ["train", "val"]
        dataset_dir = os.path.join(dataset_dir, subset)


        if('_via_img_metadata' in annotations.keys()):
            annotations = annotations['_via_img_metadata']
        # annotations = json.load(open(os.path.join(dataset_dir, "via_region_data.json")))
        annotations = list(annotations.values())  # don't need the dict keys

        # The VIA tool saves images in the JSON even if they don't have any
        # annotations. Skip unannotated images.\
        # print(annotations)
        annotations = [a for a in annotations if a['regions']]


        # Add images
        for a in annotations:
            # Get the x, y coordinaets of points of the polygons that make up
            # the outline of each object instance. There are stores in the
            # shape_attributes (see json format above)
            polygons = [r['shape_attributes'] for r in a['regions']]
            polygons_ids = [r['region_attributes'] for r in a['regions']]

            # load_mask() needs the image size to convert polygons to masks.
            # Unfortunately, VIA doesn't include it in JSON, so we must read
            # the image. This is only managable since the dataset is tiny.
            image_path = os.path.join(dataset_dir, a['filename'])
            image = skimage.io.imread(image_path)
            height, width = image.shape[:2]

            self.add_image(
                "csku",
                image_id=a['filename'],  # use file name as a unique image id
                path=image_path,
                width=width, height=height,
                polygons=polygons,
                polygons_ids=polygons_ids)

    def load_mask(self, image_id):
        """Generate instance masks for an image.
       Returns:
        masks: A bool array of shape [height, width, instance count] with
            one mask per instance.
        class_ids: a 1D array of class IDs of the instance masks.
        """
        # If not a balloon dataset image, delegate to parent class.
        image_info = self.image_info[image_id]
        if image_info["source"] != "csku":
            print('[ERROR] image_info["source"] != csku')
            return super(self.__class__, self).load_mask(image_id)

        # Convert polygons to a bitmap mask of shape
        # [height, width, instance_count]
        info = self.image_info[image_id]
        mask = np.zeros([info["height"], info["width"], len(info["polygons"])],
                        dtype=np.uint8)

        ################## Santosh Added #########################
        class_names = [r['Product name'] for r in info["polygons_ids"]]

        ### Product ids mapping ###
        product_id_mapping = {}
        for class_data in self.class_info:
            product_id_mapping[class_data['name']] = class_data['id']

        #Get image corresponding product ids
        class_ids = []
        for class_name in class_names:
            class_ids.append(int(product_id_mapping[class_name]))
        ########################################################

        for i, p in enumerate(info["polygons"]):
            # Get indexes of pixels inside the polygon and set them to 1
            rr, cc = skimage.draw.polygon(p['all_points_y'], p['all_points_x'])
            mask[rr, cc, i] = 1

        # Return mask, and array of class IDs of each instance. Since we have
        # one class ID only, we return an array of 1s
        # return mask, np.ones([mask.shape[-1]], dtype=np.int32)
        return mask, np.asarray(class_ids, dtype=np.int32)

    def image_reference(self, image_id):
        """Return the path of the image."""
        info = self.image_info[image_id]
        if info["source"] == "csku":
            return info["path"]
        else:
            super(self.__class__, self).image_reference(image_id)

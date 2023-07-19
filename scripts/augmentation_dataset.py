import copy
import uuid
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import cv2
from scripts.utils import *

def process_aug(images):
    augmented_images = []
    augmentations = augmentations = [
        iaa.Fliplr(0.5),
        iaa.Flipud(0.2), 
        iaa.Crop(percent=(0, 0.1)), 
        iaa.Sometimes(0.5, iaa.GaussianBlur(sigma=(0, 0.5))),
        iaa.LinearContrast((0.75, 1.5)),
        iaa.AdditiveGaussianNoise(loc=0, scale=(0.0, 0.05*255), per_channel=0.5),
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-25, 25),
            shear=(-8, 8)
        ),
        iaa.LinearContrast((0.5, 2.0), per_channel=0.5),
        iaa.Invert(0.05, per_channel=False),
        iaa.Grayscale(alpha=(0.0, 1.0))
    ]

    
    for image in images:
        augmented_images.append(image)
        new_image = copy.deepcopy(image)

        bounding_boxes = []
        
        for anno in new_image.annotations:
            a_ratio=(anno["X_MIN_A"],anno["Y_MIN_A"])
            c_ratio=(anno["X_MAX_C"],anno["Y_MAX_C"])
            
            a_pixel = convert_point_ratio_to_pixel(new_image.cv_image,a_ratio)
            c_pixel = convert_point_ratio_to_pixel(new_image.cv_image,c_ratio)

            bounding_boxes.append(BoundingBox(x1=a_pixel[0],x2=c_pixel[0],y1=a_pixel[1],y2=c_pixel[1]))

        bbs = BoundingBoxesOnImage(bounding_boxes, shape=new_image.cv_image.shape)

        for aug in augmentations:
            if new_image.cv_image.shape[-1] != 3:
                new_image.cv_image = cv2.cvtColor(new_image.cv_image, cv2.COLOR_GRAY2BGR)
            image_aug, bbs_aug = aug(image=new_image.cv_image, bounding_boxes=bbs)
            
            new_image.cv_image = image_aug
            for idx, anno in enumerate(new_image.annotations):
                bb = bbs_aug[idx]
                a_ratio = convert_pixel_to_ratio(new_image.cv_image,(bb.x1,bb.y1))
                c_ratio = convert_pixel_to_ratio(new_image.cv_image,(bb.x2,bb.y2))
                anno["X_MIN_A"] = precision(a_ratio[0])
                anno["Y_MIN_A"] = precision(a_ratio[1])
                anno["X_MAX_B"] = precision(c_ratio[0])
                anno["Y_MIN_B"] = precision(a_ratio[1])
                anno["X_MAX_C"] = precision(c_ratio[0])
                anno["Y_MAX_C"] = precision(c_ratio[1])
                anno["X_MIN_D"] = precision(a_ratio[0])
                anno["Y_MAX_D"] = precision(c_ratio[1])
            
            new_image.basename = "{0}_{1}".format(aug.name,uuid.uuid4())
            augmented_images.append(copy.deepcopy(new_image))
    
    return augmented_images
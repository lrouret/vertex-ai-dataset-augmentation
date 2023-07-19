import copy
import uuid
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import cv2

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

        bbs = BoundingBoxesOnImage([
            BoundingBox(
                min(float(anno["X_MIN_A"]), float(anno["X_MIN_D"]), float(anno["X_MAX_B"]), float(anno["X_MAX_C"])), 
                min(float(anno["Y_MIN_A"]), float(anno["Y_MIN_B"]), float(anno["Y_MAX_C"]), float(anno["Y_MAX_D"])), 
                max(float(anno["X_MIN_A"]), float(anno["X_MIN_D"]), float(anno["X_MAX_B"]), float(anno["X_MAX_C"])), 
                max(float(anno["Y_MIN_A"]), float(anno["Y_MIN_B"]), float(anno["Y_MAX_C"]), float(anno["Y_MAX_D"]))
            ) for anno in new_image.annotations
        ], shape=new_image.cv_image.shape)


        for aug in augmentations:
            if new_image.cv_image.shape[-1] != 3:
                new_image.cv_image = cv2.cvtColor(new_image.cv_image, cv2.COLOR_GRAY2BGR)
            image_aug, bbs_aug = aug(image=new_image.cv_image, bounding_boxes=bbs)
            
            new_image.cv_image = image_aug
            for idx, anno in enumerate(new_image.annotations):
                bb = bbs_aug[idx]
                anno["X_MIN_A"] = bb.x1
                anno["Y_MIN_A"] = bb.y1
                anno["X_MAX_B"] = bb.x1
                anno["Y_MIN_B"] = bb.y2
                anno["X_MAX_C"] = bb.x2
                anno["Y_MAX_C"] = bb.y2
                anno["X_MIN_D"] = bb.x2
                anno["Y_MAX_D"] = bb.y1
            
            new_image.basename = "{0}_{1}".format(aug.name,uuid.uuid4())
            augmented_images.append(copy.deepcopy(new_image))
    
    return augmented_images
import copy
import uuid
from imgaug import augmenters as iaa
from imgaug.augmentables.bbs import BoundingBox, BoundingBoxesOnImage
import cv2
from scripts.utils import *

def is_valid_bbox(bbox):
    # Teste si la bounding box est valide (représente un rectangle)
    return bbox.is_fully_within_image(bbox.shape)

def process_aug(images):
    augmented_images = []
    augmentations = [
        iaa.Flipud(0.5), 
        iaa.Crop(percent=(0, 0.1)), 
        iaa.Affine(
            scale={"x": (0.8, 1.2), "y": (0.8, 1.2)},
            translate_percent={"x": (-0.2, 0.2), "y": (-0.2, 0.2)},
            rotate=(-9, 9),
            shear=(-5, 5)
        ),
        iaa.Invert(0.25, per_channel=False),
    ]

    for image in images:
        temp_image = copy.deepcopy(image)
        
        if temp_image.cv_image.shape[-1] != 3:
            temp_image.cv_image = cv2.cvtColor(temp_image.cv_image, cv2.COLOR_GRAY2BGR)
            
        image_aug = temp_image
        
        for aug in augmentations:
            # On crée une nouvelle image
            new_image = copy.deepcopy(image_aug)
            new_image.basename = str(uuid.uuid4())
            
            # On récupére les box de l'image précedente
            initial_bbs = define_bounding_boxes_from_annotation(new_image)
            
            #On effectue l'augmentation sur l'ancienne image
            cv_image_aug, bbs_aug = aug(image=new_image.cv_image, bounding_boxes=initial_bbs)
            # Si toutes les bounding boxes sont valides, on ajoute l'image augmentée

            #Il faut maintenant maj les valeurs des annotations dans l'objet Image
            new_image.update_annotations_from_bbs(bbs_aug)
            
            #MaJ l'image en elle même
            new_image.cv_image = cv_image_aug
            
            #display(new_image)
            
            #On effectue un dernière copie pour éviter toute réference
            final_copy=copy.deepcopy(new_image)
            
            image_aug=final_copy # Image utilisé à la prochaine itération
            augmented_images.append(final_copy)


    return augmented_images


# POUR CHAQUE images
#     COPIER image
#     POUR CHAQUE augmentation
#         COPIER image
#         RECUPERER box
#         APPLIQUER aug
#         POUR CHAQUE box DE image 
#             MAJ box
import argparse
import os
from scripts.augmentation_dataset import process_aug
from scripts.newob import *
from scripts.utils import *
from scripts.preprocessing_dataset import process_preproc
import csv
import time 
import cv2

DEFAULT_SOURCE_DT_NAME = "source_ds"

OUTPUT_PREPOC_DT = "preproc_ds"
OUTPUT_AUGM_DT = "aug_ds"

IMAGES_FOLDER_NAME = "images"
ANNOTATION_FILE = "local_annotations.csv"

# A changer en fonction des évolutions de VERTEX AI
ANNOTATION_HEADER= ["IMAGE_URI","LABEL","X_MIN_A","Y_MIN_A","X_MAX_B","Y_MIN_B","X_MAX_C","Y_MAX_C","X_MIN_D","Y_MAX_D"]

disable_verification = False
force_delete_output_file = True

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input-dataset", type=str, default=DEFAULT_SOURCE_DT_NAME,help="Chemin du dossier du dataset source")
parser.add_argument("-nc","--no-check", type=bool, default=disable_verification,help="Désactiver l'existence du dataset source")
parser.add_argument("-fc","--force-delete", type=bool, default=force_delete_output_file,help="Suppression des dossiers de sortie")
parser.add_argument("-b","--bucket", type=str, default="",help="url du bucket")

args = parser.parse_args()

SOURCE_DATASET = args.input_dataset
disable_verification = args.no_check
force_delete_output_file = args.force_delete
bucket_url=args.bucket


ANNOTATION_FILE_PATH="{0}/{1}".format(SOURCE_DATASET,ANNOTATION_FILE)
print("\n------- Vérification du dataset -------")

if not disable_verification:
    # Vérifier que le dataset et les steps sont valides
    if not os.path.exists(SOURCE_DATASET) or not IMAGES_FOLDER_NAME in get_all_folder_name_in_folder(SOURCE_DATASET) and os.path.exists(ANNOTATION_FILE_PATH):
        print("⚠️ Le dataset n'existe pas")
        exit()
    else:
        print("✅ Dataset trouvé")
        

    if force_delete_and_create_folder:
        print("❗ Les données existantes sont écrasées (MODE FORCE ACTIVE).")
        force_delete_and_create_folder("./{0}".format(OUTPUT_PREPOC_DT),IMAGES_FOLDER_NAME)
        force_delete_and_create_folder("./{0}".format(OUTPUT_AUGM_DT),IMAGES_FOLDER_NAME)
    else:
        create_or_delete_folder("./{0}".format(OUTPUT_PREPOC_DT),IMAGES_FOLDER_NAME)
        create_or_delete_folder("./{0}".format(OUTPUT_AUGM_DT),IMAGES_FOLDER_NAME)

# Read annotation file
annotations = []
isFirstRow = True
with open(ANNOTATION_FILE_PATH, 'r') as file:
    reader = csv.DictReader(
        file, fieldnames=ANNOTATION_HEADER)
    for row in reader:
        # La premier ligne est le header
        if isFirstRow:
            isFirstRow = False
        else:
            annotations.append(row)

# Chargement de toutes les images
print("\n------- CHARGEMENT DES IMAGES ET ANNOTATIONS -------")
images = []
IMAGES_PATH = "{0}/{1}".format(SOURCE_DATASET,IMAGES_FOLDER_NAME)
for _, _, files in os.walk(IMAGES_PATH):
    for image_file in files:
        image_annotations = list(filter(lambda item : item["IMAGE_URI"] == image_file,annotations))
        filename_splitted = image_file.split(".")
        filename = '.'.join(filename_splitted[:-1])
        extension = filename_splitted[-1]
        cv_image = cv2.imread("{0}/{1}".format(IMAGES_PATH,image_file))
        
        image = Image(cv_image,filename,extension,image_annotations)
        
        images.append(image)
print("✅ {0} images et {1} annotations!".format(len(images),len(annotations)))

init_image = len(images)
def export_dataset(images, OUPUT):
    # Récupérer toutes les annotations et images
    annotations_to_save = []
    for image in images:
        if not len(bucket_url) == 0 and OUPUT == OUTPUT_AUGM_DT:
            for annot in image.annotations:
                annot["IMAGE_URI"] = "{0}/{1}".format(bucket_url,annot["IMAGE_URI"])
        
        annotations_to_save.extend(image.annotations)
        
        new_image_path = "{0}/{1}/{2}.{3}".format(OUPUT,IMAGES_FOLDER_NAME,image.basename,image.extension)

        cv2.imwrite(
            new_image_path,
            image.cv_image,
        )
        
    new_annotations_file = "{0}/{1}".format(OUPUT,ANNOTATION_FILE)
    
    
    
    with open(new_annotations_file, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=ANNOTATION_HEADER)
        dict_writer.writeheader()
        dict_writer.writerows(annotations_to_save)

print("\n------- PREPROCESSING -------")

print("🔨 Début de préprocesse des images...")

start_time = time.time()

prepoc_images = process_preproc(images)
export_dataset(images,OUTPUT_PREPOC_DT)

print("✅ PREPROCESSING, ⏳ Temps d'exécution : {} secondes".format(str(round(time.time() - start_time, 2))))

print("\n------- DATA AUGMENTATION -------")

print("🔨 Début de l'augmentation des images...")

start_time = time.time()

images_aug = process_aug(prepoc_images)
export_dataset(images_aug,OUTPUT_AUGM_DT)

print("✅ PREPROCESSING, ⏳ Temps d'exécution : {} secondes".format(str(round(time.time() - start_time, 2))))

print("\n------- BILAN -------")
print("🏁 Commencé avec {0} finit avec {1} ".format(init_image,len(images_aug)))

print("\n📃 INPUT:\n{0}".format(os.path.abspath(SOURCE_DATASET)))
print("\n📈 OUTPUT:\nPrétraitement: \n{0}\n\nAugmentation:\n{1}".format(os.path.abspath(OUTPUT_PREPOC_DT),os.path.abspath(OUTPUT_AUGM_DT)))
print("\n------- FIN -------")




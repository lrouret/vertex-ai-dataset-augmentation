import os
import shutil

def get_all_folder_name_in_folder(folder_path):
    folder_names = []
    for _, folders, _ in os.walk(folder_path):
        for folder in folders:
            folder_names.append(folder)
    return folder_names

def force_delete_and_create_folder(folder,image_folder_name):
    if not os.path.exists(folder):
        os.mkdir(folder)
        return
    shutil.rmtree(folder)
    os.mkdir(folder)
    os.mkdir("{}/{}".format(folder,image_folder_name))
    
def create_or_delete_folder(folder,image_folder_name):
    if not os.path.exists(folder):
        os.mkdir(folder)
        os.mkdir("{}/{}".format(folder,image_folder_name))
    else:
        print("❓ Le {1} de sortie existe déjà. Voulez-vous écraser ce dossier ? (y/n) [y]: ".format(folder))
        answer = input("▶️   ")
        if answer == "y" or answer == "Y" or answer == "":
            print("❗ Les données existantes sont écrasées.")
            shutil.rmtree(folder)
            os.mkdir(folder)
            os.mkdir("{}/{}".format(folder,image_folder_name))
        elif answer == "n":
            print("❕ Les données existantes ne seront pas écrasées.")
        else:
            print("❗ Réponse invalide. Arrêt du script.")
            exit()
            
def convert_point_ratio_to_pixel(image,point):
    img_shape = image.shape
    if len(img_shape) == 3:
        (height, width, _) = image.shape
    elif len(img_shape) == 2:
        (height, width) = image.shape
    else:
        print("Trop de couches pour cette image")
        exit()
    return (float(point[0])*width,float(point[1])*height)

def convert_pixel_to_ratio(image,point):
    img_shape = image.shape
    if len(img_shape) == 3:
        (height, width, _) = image.shape
    elif len(img_shape) == 2:
        (height, width) = image.shape
    else:
        print("Trop de couches pour cette image")
        exit()
    return (float(point[0])/width,float(point[1])/height)
    
def precision(value):
    if value < 0.00001:
        return 0
    elif value > 1.0:
        return 1.0
    else:
        return value

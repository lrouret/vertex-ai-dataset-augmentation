import os
import shutil
import cv2
import copy

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
        
    x_point = int(float(point[0])*width)
    y_point = int(float(point[1])*height)
    
    x_point = max(0, min(x_point, width-1))
    y_point = max(0, min(y_point, height-1))
    
    return (x_point,y_point)

def convert_pixel_to_ratio(image,point):
    img_shape = image.shape
    if len(img_shape) == 3:
        (height, width, _) = image.shape
    elif len(img_shape) == 2:
        (height, width) = image.shape
    else:
        print("Trop de couches pour cette image")
        exit()
        
    x_point = float(point[0])/width
    y_point = float(point[1])/height
    
    x_point = max(0.00001, min(x_point, 0.9999999))
    y_point = max(0.00001, min(y_point, 0.9999999))
    
    return (x_point,y_point)
    
    
def display(image):
    
    new_image = copy.deepcopy(image)
    
    if len(new_image.annotations) == 0:
        return
    
    for annotation in new_image.annotations:
        # Convert normalized coordinates back to pixel values
        print("======")
        print("X_MIN_A:{}".format(annotation['X_MIN_A']))
        print("Y_MIN_A:{}".format(annotation['Y_MIN_A']))
        print("X_MAX_C:{}".format(annotation['X_MAX_C']))
        print("Y_MAX_C:{}".format(annotation['Y_MAX_C']))
        a = convert_point_ratio_to_pixel(new_image.cv_image,(annotation['X_MIN_A'], annotation['Y_MIN_A']))
        c = convert_point_ratio_to_pixel(new_image.cv_image,(annotation['X_MAX_C'], annotation['Y_MAX_C']))

        # Draw rectangle on the image
        cv2.rectangle(new_image.cv_image, a, c, (0, 255, 0), 2)

    # Display the image
    cv2.imshow('Image with annotations', new_image.cv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

import cv2

def grayscale(opencv_img):
    return cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)

def auto_adjust_contrast(opencv_img):
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    return clahe.apply(opencv_img)

def process_preproc(images):
    for image in images:
        temp_img = grayscale(image.cv_image)
        temp_img = auto_adjust_contrast(temp_img)
        image.cv_image = temp_img
    return images





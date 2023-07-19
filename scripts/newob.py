class Image:
    def __init__(self, cv_image, basename, extension,annotations):
        self.cv_image = cv_image 
        self.basename = basename 
        self.extension = extension 
        self.annotations = annotations



from scripts.utils import *

class Image:
    def __init__(self, cv_image, basename, extension,annotations):
        self.cv_image = cv_image 
        self.basename = basename 
        self.extension = extension 
        self.annotations = annotations
        
    def update_annotations_from_bbs(self,bbs):
        for idx, anno in enumerate(self.annotations):
                bb = bbs[idx]
                # Vertex AI prend des ratio avec 4 points
                a_ratio = convert_pixel_to_ratio(self.cv_image,(bb.x1,bb.y1))
                b_ratio = convert_pixel_to_ratio(self.cv_image,(bb.x1,bb.y2))
                c_ratio = convert_pixel_to_ratio(self.cv_image,(bb.x2,bb.y2))
                d_ratio = convert_pixel_to_ratio(self.cv_image,(bb.x2,bb.y1))
                
                anno["IMAGE_URI"] = "{0}.{1}".format(self.basename,self.extension)
                anno["X_MIN_A"] = a_ratio[0]
                anno["Y_MIN_A"] = a_ratio[1]
                anno["X_MAX_B"] = b_ratio[0]
                anno["Y_MIN_B"] = b_ratio[1]
                anno["X_MAX_C"] = c_ratio[0]
                anno["Y_MAX_C"] = c_ratio[1]
                anno["X_MIN_D"] = d_ratio[0]
                anno["Y_MAX_D"] = d_ratio[1]



import base64
import cv2
import numpy as np


class processImg():
    def __init__(self):
        '''
        process initiarize method
        ex) read table file, setting, initiarize
        '''
        pass

    def readb64(self, base64_string):
        img = base64.b64decode(base64_string)
        npimg = np.fromstring(img, dtype=np.uint8)
        cv_img = cv2.imdecode(npimg, 1)
        return cv_img

    def writeb64(self, cv_img):
        retval, buffer = cv2.imencode('.jpg', cv_img)
        base64_img = base64.b64encode(buffer)
        return base64_img

    def do(self, in_img_base64, setting):
        # sample
        in_img_cv = self.read64(in_img_base64)
        out_img_cv, result = self.yourMethod(in_img_cv, setting)
        out_img_base64 = self.write64(out_img_cv)
        return out_img_base64, result

    def yourMethod(self, in_img_cv, setting):
        '''
        please write thid method
        as you like
        '''
        h, w = in_img_cv.shape[0, 1]
        gray_img_cv = cv2.cvtColor(in_img_cv, cv2.COLOR_BGR2GRAY)
        result = {'color': 'gray',
                  'size': [w, h]}
        return gray_img_cv, result

import base64
from io import BytesIO
import numpy as np
import datetime
from PIL import Image
import cv2


class processImg():
    def __init__(self):
        '''
        process initiarize method
        ex) read table file, setting, initiarize
        '''
        pass

    def yourMethod(self, in_img, setting):
        '''
        please write thid method
        as you like
        image input and output is numpy array
        '''
        # face mask app setting
        CASCADE_PATH = "sample/haarcascade_frontalface_default.xml"
        mask = cv2.imread("sample/shirotan.jpg")

        h, w = in_img.shape[:2]
        img = in_img.copy()
        cascade = cv2.CascadeClassifier(CASCADE_PATH)
        facerect = cascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=1, minSize=(10, 10))
        num_face = len(facerect)
        if num_face > 0:
            for rect in facerect:
                resize_mask = cv2.resize(mask, tuple(rect[2:4]))
                img[rect[1]:(rect[1]+rect[3]), rect[0]:(rect[0]+rect[2])] = resize_mask
        result = {'mask': 'shirotan',
                  'num_face': num_face,
                  'size': [w, h]}
        '''
        # this is sample
        pilImg = Image.fromarray(in_img)
        gray_pilImg = pilImg.convert('L')
        result = {'color': 'gray',
                  'size': [w, h]}
        '''
        return np.asarray(img), result


    def readb64(self, base64_string):
        im = Image.open(BytesIO(base64.b64decode(base64_string)))
        im.save('uploads/' + self.timestamp + '.png', format='PNG')
        return np.asarray(im)

    def writeb64(self, img):
        pilImg = Image.fromarray(img)
        pilImg.save('outputs/' + self.timestamp + '.png', format='PNG')

        buffered = BytesIO()
        pilImg.save(buffered, format="PNG")
        base64_img = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return base64_img

    def do(self, in_img_base64, setting):
        # get timestamp
        now = datetime.datetime.now()
        self.timestamp = "{0:%Y%m%d-%H%M%S}".format(now)

        in_img = self.readb64(in_img_base64)
        out_img, result = self.yourMethod(in_img, setting)
        out_img_base64 = self.writeb64(out_img)
        return out_img_base64, result


import base64
from io import BytesIO
import numpy as np
import datetime
from PIL import Image


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
        # this is sample
        h, w = in_img.shape[:2]
        pilImg = Image.fromarray(in_img)
        gray_pilImg = pilImg.convert('L')
        result = {'color': 'gray',
                  'size': [w, h]}
        return np.asarray(gray_pilImg), result

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
        self.timestamp = "{0:%Y%m%d-%H%M%S}_".format(now)

        in_img = self.readb64(in_img_base64)
        out_img, result = self.yourMethod(in_img, setting)
        out_img_base64 = self.writeb64(out_img)
        return out_img_base64, result


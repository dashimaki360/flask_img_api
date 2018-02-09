from skimage import io
from skimage.color import rgb2gray


class processImg():
    def __init__(self):
        pass

    def do(self, in_img_path, out_img_path):
        im = io.imread(in_img_path)
        gray = rgb2gray(im)
        io.imsave(out_img_path, gray)
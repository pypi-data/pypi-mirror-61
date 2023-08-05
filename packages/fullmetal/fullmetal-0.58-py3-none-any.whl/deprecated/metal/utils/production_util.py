import resource
import sys
import urllib.request
import PIL
from PIL import Image
from metal.utils.data_manipulation import normalize
import dill
from autograd.parameter import Parameter
import random
import cv2
import os
import scipy.ndimage as ndi

import numpy as np
import scipy
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.ndimage import rotate

sns.set(color_codes=True)

print('resource limit ',resource.getrlimit(resource.RLIMIT_STACK))
print('recursion limit ',sys.getrecursionlimit())


def save_model(filename,model, max_rec=100000):
    max_rec = max_rec
    sys.setrecursionlimit(max_rec)
    with open(filename+'.pkl', 'wb') as file:
        dill.dump(model.layers, file)

def load_model(filename):
    with open(filename+'.pkl', 'rb') as file:
        layers = dill.load(file)
    return layers

def fetch_img(url,shape,invert=False):
    I = Image.open(urllib.request.urlopen(url)).convert('L')
    I = np.asarray(I.resize((shape[-1],shape[-2]), PIL.Image.LANCZOS)).reshape(*shape)
    if invert:
        I = np.invert(I)
    I = normalize(I)
    return I

def _forward_pass(X, training=True, model_name=None):
    """ Calculate the output of the NN """
    layers_ = load_model(model_name)
    layer_output = Parameter(X,False)
    for layer in layers_:
        layer_output = layer.forward_pass(layer_output, training)
    return layer_output

#resize batch
#example: img_tran(X_train,8)
def imgs_trans(imgs_in,size):
    factor = size/imgs_in.shape[1]
    imgs_out = ndi.zoom(imgs_in, (1, factor, factor, 1), order=2)
    print(imgs_out.shape)
    return imgs_out

def create_training_data(img_size=50, classes=[], data_dir="", color=None):
    #classses is the name of each folder in downloads
    #data_dir is path to downloads
    #img_size for WxH

    if color == 'gray':
        color = cv2.IMREAD_GRAYSCALE
    elif color == 'gray_to_rgb':
        color = cv.CV_GRAY2RGB
    elif color == None:
        color = cv2.COLOR_BGR2RGB

        # TODO: add more opitons

    training_data = []
    for class_ in classes:
        path = os.path.join(data_dir, class_)
        class_num = classes.index(class_)
        for img in os.listdir(path):
            try:
                img_array = cv2.imread(os.path.join(path,img), color)
                new_array = cv2.resize(img_array,(img_size,img_size)) #bug need to fix channels
                training_data.append([new_array,class_num])
            except Exception  as e:
                pass
    random.shuffle(training_data)
    imgs = []
    labs = []
    for img, lab in training_data:
        imgs.append(img)
        labs.append(lab)
    #imgs = np.array(imgs).reshape(-1, img_size,img_size)
    self.imgs = imgs
    self.labels = labels
    return self.imgs, self.labs

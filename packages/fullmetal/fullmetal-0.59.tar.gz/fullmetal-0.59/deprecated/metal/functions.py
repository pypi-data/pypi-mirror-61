import numpy as np
from autograd.dependency import Dependency
import math
from deprecated.metal.utils.layer_data_manipulations import determine_padding, get_im2col_indices

"""
Utility file for defining functions or a classes that will forward prop and backward prop within metal.
"""

class IMG2COL(object):
    """docstring for IMG2COL."""

    def __init__(self, images, filter_shape, stride, output_shape='same'):
        super(IMG2COL, self).__init__()
        self.type = type(images)
        self.images = images
        self.filter_shape = filter_shape
        self.stride = stride
        self.output_shape = output_shape
        self.images_shape = images.shape


    def image_to_column(self):
        depends_on: List[Dependency] = []
        filter_height, filter_width = self.filter_shape

        pad_h, pad_w = determine_padding(self.filter_shape, self.output_shape)

        # Add padding to the image
        images_padded = np.pad(self.images.data, ((0, 0), (0, 0), pad_h, pad_w), mode='constant')

        # Calculate the indices where the dot products are to be applied between weights
        # and the image
        k, i, j = get_im2col_indices(self.images_shape, self.filter_shape, (pad_h, pad_w), self.stride)

        # Get content from image at those indices
        cols = images_padded[:, k, i, j]
        channels = self.images_shape[1]
        # Reshape content into column shape
        cols = cols.transpose(1, 2, 0).reshape(filter_height * filter_width * channels, -1)

        requires_grad=self.images.requires_grad
        if self.images.requires_grad:
            depends_on.append(Dependency(self.images, self.column_to_image))
        return self.type(data=cols,requires_grad=requires_grad,depends_on=depends_on)

    def column_to_image(self, grad):
        batch_size, channels, height, width = self.images_shape
        pad_h, pad_w = determine_padding(self.filter_shape, self.output_shape)
        height_padded = height + np.sum(pad_h)
        width_padded = width + np.sum(pad_w)
        images_padded = np.zeros((batch_size, channels, height_padded, width_padded))

        # Calculate the indices where the dot products are applied between weights
        # and the image
        k, i, j = get_im2col_indices(self.images_shape, self.filter_shape, (pad_h, pad_w), self.stride)

        cols = grad.reshape(channels * np.prod(self.filter_shape), -1, batch_size)
        cols = cols.transpose(2, 0, 1)
        # Add column content to the images at the indices
        np.add.at(images_padded, (slice(None), k, i, j), cols)

        # Return image without padding
        return images_padded[:, :, pad_h[0]:height+pad_h[0], pad_w[0]:width+pad_w[0]]

class Trans(object):
    """docstring for Trans."""

    def __init__(self, t, axis_f, axis_b):
        super(Trans, self).__init__()
        self.type = type(t)
        self.t = t
        self.axis_f = axis_f
        self.axis_b = axis_b

    def trans(self):
        data = self.t.data.transpose(*self.axis_f)
        requires_grad = self.t.requires_grad
        depends_on: List[Dependency] = []
        if requires_grad:
            depends_on.append(Dependency(self.t, self.Trans_grad))
        return self.type(data=data,requires_grad=requires_grad,depends_on=depends_on)

    def Trans_grad(self,grad):
        return grad.transpose(*self.axis_b)

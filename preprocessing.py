import cv2
import numpy as np
import skimage.transform as imgtf


############ Constants ############


# Factor in between steering unit and degree
STEERING_FACTOR = 25


############ Functions ############


# Adds additional dimension to gray scale images (for neural nets)
def add_gray_dimension(images):
    return images[..., np.newaxis]


# Drops additional dimension in gray scale images (for image display/processing)
def drop_gray_dimension(images):
    return images.reshape(images.shape[:-1])


# Calculates adjusted steering angle base on camera delta and steering distance
def adjust_steering_by_angle(steering, view_angle):
    steering2 = steering + view_angle / STEERING_FACTOR
    return max(-1.0, min(steering2, 1.0))


# Calculates adjusted steering angle base on camera delta and steering distance
def adjust_steering_by_offset(steering, view_offset, steering_distance=1.0):
    alpha = steering * STEERING_FACTOR
    b = np.tan(np.radians(alpha)) * steering_distance + view_offset
    alpha2 = np.degrees(np.arctan(-b) / steering_distance)
    steering2 = alpha2 / STEERING_FACTOR
    return max(-1.0, min(steering2, 1.0))


# Loads image from disk as RGB
def load(image_filename):
    image = cv2.imread("{}".format(image_filename))
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


# Flips image horizontally
def flip_horizontal(image):
    image = cv2.flip(image, 1)
    return image


# Shear
def shear(image, angle):
    a = angle / 180 * np.pi
    transform = imgtf.AffineTransform(matrix=np.array([[1, np.sin(a), -image.shape[0] * np.sin(a)], [0, 1, 0], [0, 0, 1]]))
    return imgtf.warp(image, transform, mode='edge')


# Rotate
def rotate(image, angle):
    return imgtf.rotate(image, -angle/2, center=(image.shape[0], image.shape[1]/2), mode='edge')


# Pre-processes an image by cropping, scaling and YUV conversion
def preprocess(image):
    image = cv2.resize(image, (64, 160))
    image = image[73:image.shape[0] - 23, 0:image.shape[1]]
    image = image.astype(np.float32)
    image_min = np.min(image)
    image_max = np.max(image)
    image = (image - image_min) / (image_max - image_min) - 0.5
    return image
# Importing libraries
from PIL import Image
import os
import numpy as np
import tensorflow as tf

# Path to the directory containing images
iris_directory = r'Data/iris'  # Replace this with your image directory

# Define the desired size for the resized images
desired_size = (64, 64)  # Replace with your desired dimensions

# List all files in the directory
file_list = os.listdir(iris_directory)

# Initialize an empty list to store image arrays
image_arrays = []

# Iterate through each file in the directory
for filename in file_list:
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        # Open the image file
        image_path = os.path.join(iris_directory, filename)

        img = tf.keras.preprocessing.image.load_img(image_path, target_size=desired_size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)

        image_arrays.append(img_array)

label = []

for x in range(len(image_arrays)):
    label.append([1, 0])

other_directory = r'Data/other flower'  # Replace this with your image directory

# Define the desired size for the resized images
desired_size = (64, 64)  # Replace with your desired dimensions

# List all files in the directory
file_list = os.listdir(other_directory)

# Iterate through each file in the directory
for filename in file_list:
    if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg'):
        # Open the image file
        image_path = os.path.join(other_directory, filename)

        img = tf.keras.preprocessing.image.load_img(image_path, target_size=desired_size)
        img_array = tf.keras.preprocessing.image.img_to_array(img)

        image_arrays.append(img_array)

for x in range(len(label), len(image_arrays)):
    label.append([0, 1])

# Convert the list of image arrays to a single NumPy array
image_arrays = np.array(image_arrays)

indices = np.arange(len(label))
np.random.shuffle(indices)
shuffle_images = []
shuffle_label = []
for x in range(0, len(indices)):
    shuffle_label.append(label[indices[x]])
    shuffle_images.append(image_arrays[indices[x]])

shuffle_images = np.array(shuffle_images)
print(shuffle_images.shape, len(shuffle_label))

n = shuffle_images.shape[0]

train_images = np.array(shuffle_images[0:n // 10 * 8])
train_labels = np.array(shuffle_label[0:n // 10 * 8])

test_images = np.array(shuffle_images[n // 10 * 8:])
test_labels = np.array(shuffle_label[n // 10 * 8:])

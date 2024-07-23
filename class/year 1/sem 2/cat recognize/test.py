import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models


def load_images_and_labels(the_input_folder):
    the_images = []
    the_labels = []
    for i in range(len(the_input_folder)):
        for j in range(the_input_folder[i][1]):
            image_path = os.path.join(the_input_folder[i][0], f"resized_{j + 1}.jpg")

            # 读取图像
            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(256, 256))
            img_array = tf.keras.preprocessing.image.img_to_array(img)/255
            the_images.append(img_array)

            the_labels.append(the_input_folder[i][2])
    the_labels = to_categorical(the_labels, len(set(the_labels)))
    return np.array(the_images), np.array(the_labels)


def create_model():
    model = tf.keras.Sequential([
        # Add Convolutional layers
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(256, 256, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Flatten layer to transition from convolutional layers to dense layers
        tf.keras.layers.Flatten(),

        # Dense layers
        tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        # Output layer
        tf.keras.layers.Dense(2, activation='softmax')
    ])

    return model


def inception_module(x, filters):
    # 1x1 convolution
    conv1x1_1 = layers.Conv2D(filters[0], (1, 1), padding='same', activation='relu')(x)

    # 1x1 convolution followed by 3x3 convolution
    conv1x1_2 = layers.Conv2D(filters[1], (1, 1), padding='same', activation='relu')(x)
    conv3x3 = layers.Conv2D(filters[2], (3, 3), padding='same', activation='relu')(conv1x1_2)

    # 1x1 convolution followed by 5x5 convolution
    conv1x1_3 = layers.Conv2D(filters[3], (1, 1), padding='same', activation='relu')(x)
    conv5x5 = layers.Conv2D(filters[4], (5, 5), padding='same', activation='relu')(conv1x1_3)

    # 3x3 max pooling followed by 1x1 convolution
    maxpool = layers.MaxPooling2D((3, 3), strides=(1, 1), padding='same')(x)
    conv1x1_4 = layers.Conv2D(filters[5], (1, 1), padding='same', activation='relu')(maxpool)

    # Concatenate all the branches
    inception = layers.concatenate([conv1x1_1, conv3x3, conv5x5, conv1x1_4], axis=-1)
    return inception

def google_net(input_shape, num_classes):
    input_layer = layers.Input(shape=input_shape)

    # Initial Convolutional Layer
    x = layers.Conv2D(64, (7, 7), strides=(2, 2), padding='same', activation='relu')(input_layer)
    x = layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)

    # Inception Modules
    x = inception_module(x, [64, 128, 128, 32, 32, 32])
    x = inception_module(x, [128, 192, 192, 64, 64, 64])
    x = layers.MaxPooling2D((3, 3), strides=(2, 2), padding='same')(x)

    # You can add more Inception modules based on the original architecture

    # Global Average Pooling
    x = layers.GlobalAveragePooling2D()(x)

    # Fully Connected Layer
    x = layers.Dense(1024, activation='relu')(x)

    # Output Layer
    output_layer = layers.Dense(num_classes, activation='softmax')(x)

    model = models.Model(inputs=input_layer, outputs=output_layer)
    return model


input_folder = [
    ["processed/cat/training", 490, 1],
    ["processed/something else/training", 245, 0],
    ["processed/animal/training", 245, 0]
]

images, labels = load_images_and_labels(input_folder)

train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2,
                                                                      random_state=42)
train_dataset = tf.data.Dataset.from_tensor_slices((train_images, train_labels)).batch(batch_size=64)
test_dataset = tf.data.Dataset.from_tensor_slices((val_images, val_labels)).batch(batch_size=64)
model = google_net((256, 256, 3),2)
learning_rate = 0.001
optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
model.compile(optimizer=optimizer,
              loss="categorical_crossentropy",
              metrics=['accuracy'])
history = model.fit(train_dataset, epochs=20, validation_data=test_dataset)

model.save('my_model.h5')
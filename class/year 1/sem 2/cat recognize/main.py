import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split


def load_images_and_labels(input_folder):
    images = []
    labels = []
    for i in range(len(input_folder)):
        for j in range(input_folder[i][1]):
            image_path = os.path.join(input_folder[i][0], f"resized_{j + 1}.jpg")

            img = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
            img_array = tf.keras.preprocessing.image.img_to_array(img)
            images.append(img_array)

            if input_folder[i][2] == 1:
                k = 1
            else:
                k = 0
            labels.append(k)
    print(len(set(labels)))
    labels = to_categorical(labels, len(set(labels)))

    print(labels)
    return np.array(images), np.array(labels)


class Inception(tf.keras.Model):
    def __init__(self, c1, c2, c3, c4):
        super().__init__()
        self.p1_1 = tf.keras.layers.Conv2D(c1, 1, activation='relu')
        self.p2_1 = tf.keras.layers.Conv2D(c2[0], 1, activation='relu')
        self.p2_2 = tf.keras.layers.Conv2D(c2[1], 3, padding='same',
                                           activation='relu')
        self.p3_1 = tf.keras.layers.Conv2D(c3[0], 1, activation='relu')
        self.p3_2 = tf.keras.layers.Conv2D(c3[1], 5, padding='same',
                                           activation='relu')
        self.p4_1 = tf.keras.layers.MaxPool2D(3, 1, padding='same')
        self.p4_2 = tf.keras.layers.Conv2D(c4, 1, activation='relu')

    def call(self, x):
        p1 = self.p1_1(x)
        p2 = self.p2_2(self.p2_1(x))
        p3 = self.p3_2(self.p3_1(x))
        p4 = self.p4_2(self.p4_1(x))
        return tf.keras.layers.Concatenate()([p1, p2, p3, p4])


def create_model():
    model = tf.keras.Sequential([
        # Add Convolutional layers
        tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 3)),
        tf.keras.layers.MaxPooling2D((2, 2)),

        tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
        tf.keras.layers.MaxPooling2D((2, 2)),

        # Flatten layer to transition from convolutional layers to dense layers
        tf.keras.layers.Flatten(),

        # Dense layers
        tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(0.01)),
        tf.keras.layers.Dropout(0.5),
        # Output layer
        tf.keras.layers.Dense(2, activation='softmax')
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    return model


def b1():
    return tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(64, 7, strides=2, padding='same',
                               activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same')])


def b2():
    return tf.keras.Sequential([
        tf.keras.layers.Conv2D(64, 1, activation='relu'),
        tf.keras.layers.Conv2D(192, 3, padding='same', activation='relu'),
        tf.keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same')])


def b3():
    return tf.keras.models.Sequential([
        Inception(64, (96, 128), (16, 32), 32),
        Inception(128, (128, 192), (32, 96), 64),
        tf.keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same')])


def b4():
    return tf.keras.Sequential([
        Inception(192, (96, 208), (16, 48), 64),
        Inception(160, (112, 224), (24, 64), 64),
        Inception(128, (128, 256), (24, 64), 64),
        Inception(112, (144, 288), (32, 64), 64),
        Inception(256, (160, 320), (32, 128), 128),
        tf.keras.layers.MaxPool2D(pool_size=3, strides=2, padding='same')])


def b5():
    return tf.keras.Sequential([
        Inception(256, (160, 320), (32, 128), 128),
        Inception(384, (192, 384), (48, 128), 128),
        tf.keras.layers.GlobalAvgPool2D(),
        tf.keras.layers.Flatten()
    ])


def creat_model_2():
    return tf.keras.Sequential([b1(), b2(), b3(), b4(), b5(),
                                tf.keras.layers.Dense(2)])


def data_generator(images, labels, batch_size):
    print("hi")
    while True:
        indices = np.arange(len(images))
        np.random.shuffle(indices)

        for i in range(0, len(indices), batch_size):
            batch_indices = indices[i:i + batch_size]
            batch_images = images[batch_indices]
            batch_labels = labels[batch_indices]
            batch_images = batch_images / 255.0

            batch_labels_one_hot = to_categorical(batch_labels, len(set(labels)))
            print(len(set(labels)))
            print(batch_labels_one_hot)
            yield batch_images, batch_labels_one_hot


if __name__ == "__main__":
    batch_size = 16
    input_folder = [
        ["processed/cat/training", 250, 1],
        ["processed/something else/training", 250, 0],
    ]

    images, labels = load_images_and_labels(input_folder)

    train_images, val_images, train_labels, val_labels = train_test_split(images, labels, test_size=0.2,
                                                                          random_state=42)

    # model = Sequential([
    #     layers.Rescaling(1. / 255, input_shape=(256, 256, 3)),
    #     layers.Conv2D(16, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(32, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Conv2D(64, 3, padding='same', activation='relu'),
    #     layers.MaxPooling2D(),
    #     layers.Flatten(),
    #     layers.Dense(128, activation='relu'),
    #     layers.Dense(2)
    # ])
    print(train_images.shape)
    model = creat_model_2()
    learning_rate = 0.001  # Adjust the value based on your problem
    optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)
    model.compile(optimizer=optimizer,
                  loss="categorical_crossentropy",
                  metrics=['accuracy'])
    history = model.fit(train_images, train_labels, epochs=10,
                        validation_data=(val_images, val_labels))

    # model.fit(train_generator, steps_per_epoch=len(train_images) // batch_size, epochs=20,
    #           validation_data=val_generator, validation_steps=len(val_images) // batch_size)

    model.save('my_model.h5')

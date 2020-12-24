import cv2
import numpy as np
from keras_squeezenet import SqueezeNet
from keras.optimizers import Adam
from keras.utils import np_utils
from keras.layers import Activation, Dropout, Convolution2D, GlobalAveragePooling2D
from keras.models import Sequential
import tensorflow as tf
import os

IMG_SAVE_PATH = '1'

CLASS_MAP = {
    "paper": 0,
    "scissors": 1,
    "rock": 2,
    "up": 3,
    "left": 4,
    "right": 5,
    "down": 6,
    "none": 7
}

NUM_CLASSES = len(CLASS_MAP)

def mapper(val):
    return CLASS_MAP[val]

def get_model():
    model = Sequential([
        SqueezeNet(input_shape=(227, 227, 3), include_top=False),
        Dropout(0.5),
        Convolution2D(NUM_CLASSES, (1, 1), padding='valid'),
        Activation('relu'),
        GlobalAveragePooling2D(),
        Activation('softmax')
    ])
    return model

# load imag
dataset = []
for directory in os.listdir(IMG_SAVE_PATH):
    path = os.path.join(IMG_SAVE_PATH, directory)
    if not os.path.isdir(path):
        continue
    for item in os.listdir(path):
        # to make sure no hidden files get in our way
        if item.startswith("."):
            continue
        img = cv2.imread(os.path.join(path, item))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (227, 227))
        dataset.append([img, directory])

data, labels = zip(*dataset)
labels = list(map(mapper, labels))

# one hot encoding
labels = np_utils.to_categorical(labels)

# 模型配置
model = get_model()
model.compile(
    optimizer=Adam(lr=0.0001),
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# 訓練
model.fit(np.array(data), np.array(labels), epochs=10)

# 儲存模型
model.save("play.h5")

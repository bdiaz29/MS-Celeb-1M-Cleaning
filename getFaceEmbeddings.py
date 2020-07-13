import cv2
import glob
from random import randint
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import Sequential
import os
import pandas as pd

def prepare(img):
    img = cv2.resize(img, (160, 160))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    face_pixels = img.astype('float32')
    mean, std = face_pixels.mean(), face_pixels.std()
    face_pixels = (face_pixels - mean) / std
    # face_pixels=np.expand_dims(face_pixels,axis=0)
    return face_pixels


face_net = tf.keras.models.load_model("E:/machine learning/saved models/facenet_keras.h5")
face_net.compile(
    optimizer='adam',
    loss="binary_crossentropy",
    metrics=['accuracy']
)

folder_list = glob.glob("G:/machine learning/Celeb 1M cleaned no relabeling/*/")
for i in range(len(folder_list)):
    print(str(i), str(i/(len(folder_list)-1)))
    opened_folder = folder_list[i]
    if os.path.exists(opened_folder + "vec.npy"):
        continue
    file_list = glob.glob(opened_folder + "*.jpg")
    images = []
    for j in range(len(file_list)):
        img = cv2.imread(file_list[j])
        img = prepare(img)
        images += [img]
    images = np.array(images)
    vec = face_net.predict(images)
    folder = os.path.basename(os.path.normpath(opened_folder))
    np.save(opened_folder + "vec.npy", vec)
    np.save(opened_folder + "file_list.npy", file_list)

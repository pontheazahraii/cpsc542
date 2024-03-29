# -*- coding: utf-8 -*-
"""CPSC542_Assignment1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1KgpRyi1se2EYY-7LE8N-v5xILteZ_G3w

# CPSC 542 Assignment 1
## Objective
1. Prove the classification task requires a deep learning solution
2. Develop a pipeline that is capable of preprocessing, augmentation, training, prediction, and validation, and uses a CNN-based DNN for classification

## Imports
"""

import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow.keras as kb
import matplotlib.pyplot as plt

"""## Random Forest"""

from keras.datasets import cifar10

# Loading Data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Examining Data Shape
print('TRAIN DATA SHAPE')
print('X_train: ' , X_train.shape)
print('y_train: ' , y_train.shape)

print('TEST DATA SHAPE')
print('X_test: ' , X_test.shape)
print('y_test: ' , y_test.shape)

# Reshape Data
reshape = X_train.shape[1] * X_train.shape[2] * X_train.shape[3]

X_train = X_train.reshape((X_train.shape[0], reshape))
X_test = X_test.reshape((X_test.shape[0], reshape))

# Normalize Data
X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train /= 255
X_test /= 255

# Check input shape
print('X_train: ', X_train.shape)
print('X_test: ', X_test.shape)

from sklearn.ensemble import RandomForestClassifier

# Create model
rf = RandomForestClassifier(n_estimators=10)
rf.fit(X_train, y_train)

# Predictions
y_pred_train = rf.predict(X_train)
y_pred_test = rf. predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay

# Metrics
print('Training Data')
print(classification_report(y_train, y_pred_train))
cm_train = confusion_matrix(y_train, y_pred_train)
disp_train = ConfusionMatrixDisplay(confusion_matrix=cm_train)
disp_train.plot()
plt.show()
plt.savefig('rf_train.png')

print('Testing Data')
print(classification_report(y_test, y_pred_test))
cm_test = confusion_matrix(y_test, y_pred_test)
disp_test = ConfusionMatrixDisplay(confusion_matrix=cm_test)
disp_test.plot()
plt.show()
plt.savefig('rf_test.png')

"""## CNN Model

### Preprocessing
"""

from keras.datasets import cifar10

# Loading Data
(X_train, y_train), (X_test, y_test) = cifar10.load_data()

# Examining Data Shape
print('TRAIN DATA SHAPE')
print('X_train: ' , X_train.shape)
print('y_train: ' , y_train.shape)

print('TEST DATA SHAPE')
print('X_test: ' , X_test.shape)
print('y_test: ' , y_test.shape)

# Plotting Data
classes = ['airplane' ,'automobile', 'bird', 'cat', 'deer',
           'dog', 'frog', 'horse', 'ship', 'truck']

print('Y VALUES\n')
for i in range(9):
  img = X_train[i]
  plt.subplot(330+1+i)
  plt.imshow(img)
  print(classes[y_train[i][0]])

print('\nX VALUES')
plt.show()
plt.savefig('examine.png')

# Preparing Data

# Scale images to the [0,1] range
X_train = X_train.astype('float32') / 255
X_test = X_test.astype('float32') / 255

# Create Validation Set
(X_train, X_val) = X_train[5000:], X_train[:5000]
(y_train, y_val) = y_train[5000:], y_train[:5000]

# Check input shape
print('X_train shape: ' , X_train.shape)
print('X_test shape: ' , X_test.shape)
print('X_val shape: ', X_val.shape)

# One-hot encode labels
y_train = kb.utils.to_categorical(y_train, 10)
y_test = kb.utils.to_categorical(y_test, 10)
y_val = kb.utils.to_categorical(y_val, 10)

"""### Augmentation"""

from keras.preprocessing.image import ImageDataGenerator

# Image Generator
datagen = ImageDataGenerator(
    width_shift_range=0.2,
    height_shift_range=0.2,
    horizontal_flip=True,
    vertical_flip=True
)

datagen.fit(X_train)

# Visualize Augmentation
X_train_sub = X_train[:10]

# Original Training Data
plt.figure(figsize=(20,2))
for i in range(10):
  plt.subplot(1, 10, i+1)
  plt.imshow(X_train_sub[i])
plt.suptitle('Original Training Images', fontsize=15)
plt.show()
plt.savefig('original.png')

# Augmented Data
plt.figure(figsize=(20,2))
for X_batch in datagen.flow(X_train_sub, batch_size=12):
  for i in range(10):
    plt.subplot(1, 10, i+1)
    plt.imshow(X_batch[i])
  plt.suptitle('Augmented Images', fontsize=15)
  plt.show()
  plt.savefig('augment.png')
  break

"""### Model"""

from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten, BatchNormalization

model = kb.Sequential()
model.add(Conv2D(filters=32, kernel_size=3, padding='same', activation='relu',
                 input_shape=(32, 32, 3)))
model.add(Conv2D(filters=64, kernel_size=3, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.4))
model.add(MaxPooling2D())
model.add(Conv2D(filters=32, kernel_size=3, padding='same', activation='relu'))
model.add(Conv2D(filters=16, kernel_size=3, padding='same', activation='relu'))
model.add(Conv2D(filters=8, kernel_size=3, padding='same', activation='relu'))
model.add(BatchNormalization())
model.add(Dropout(0.3))
model.add(MaxPooling2D())
model.add(Conv2D(filters=4, kernel_size=3, padding='same', activation='relu'))
model.add(Conv2D(filters=2, kernel_size=3, padding='same', activation='relu'))
model.add(Conv2D(filters=1, kernel_size=3, padding='same', activation='relu'))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(64, activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(16, activation='relu'))
model.add(Dropout(0.1))
model.add(Dense(10, activation='softmax'))

print(model.summary())

from keras.optimizers import RMSprop

# compile model
model.compile(loss='categorical_crossentropy', optimizer='rmsprop',
              metrics=['accuracy'])

"""### Training and Validation"""

# train model
history = model.fit(X_train, y_train, batch_size=50, epochs=100,
                    validation_data=(X_val, y_val))

# look at model history
print(history.history)

# Plot Loss
f, ax = plt.subplots(1, 2, figsize=(12,3))
ax[0].plot(history.history['loss'], label='Loss', color='r')
ax[0].plot(history.history['val_loss'], label='Validation', color='b')
ax[0].set_title('Loss')
ax[0].set_xlabel('Epoch')
ax[0].set_ylabel('Loss')
ax[0].legend()

# Accuracy
ax[1].plot(history.history['accuracy'], label='Accuracy', color='r')
ax[1].plot(history.history['val_accuracy'], label='Validation', color='b')
ax[1].set_title('Accuracy')
ax[1].set_xlabel('Epoch')
ax[1].set_ylabel('Accuracy')
ax[1].legend()

plt.tight_layout()
plt.show()
plt.savefig('model.png')

"""### Prediction"""

# evaluate data
results = model.evaluate(X_test, y_test, batch_size=100)
print('Test Loss, Test Accuracy: ' , results)

# Generate predictions
y_pred_train = model.predict(X_train)
y_pred_test = model.predict(X_test)

# Metrics
fig = plt.figure(figsize=(20, 8))
for i, idx in enumerate(np.random.choice(X_train.shape[0], size=32, replace=False)):
    ax = fig.add_subplot(4, 8, i + 1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(X_train[idx]))
    pred_idx = np.argmax(y_pred_train[idx])
    true_idx = np.argmax(y_train[idx])
    ax.set_title("{} ({})".format(classes[pred_idx], classes[true_idx]),
                 color=("green" if pred_idx == true_idx else "red"))
plt.show()
plt.savefig('cnn_train.png')

fig = plt.figure(figsize=(20, 8))
for i, idx in enumerate(np.random.choice(X_test.shape[0], size=32, replace=False)):
    ax = fig.add_subplot(4, 8, i + 1, xticks=[], yticks=[])
    ax.imshow(np.squeeze(X_test[idx]))
    pred_idx = np.argmax(y_pred_test[idx])
    true_idx = np.argmax(y_test[idx])
    ax.set_title("{} ({})".format(classes[pred_idx], classes[true_idx]),
                 color=("green" if pred_idx == true_idx else "red"))
plt.show()
plt.savefig('cnn_test.png')
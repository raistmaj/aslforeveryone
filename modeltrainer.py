import os
os.add_dll_directory("C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA/v11.7/bin")
import numpy as np
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import Dense, Input, Dropout,Flatten, Conv2D
from tensorflow.keras.layers import BatchNormalization, Activation, MaxPooling2D
from tensorflow.keras.models import Model, Sequential
from tensorflow.keras.optimizers import Adam
import tensorflow as tf



print("Tensorflow version:", tf.__version__)

image_folder="data/bw"

# load the different models
image_size = 256 # make it small so the model doesn't explode
batch_size = 64

# train it
# Consider mirroring because of the camera
datagen_ts = ImageDataGenerator(horizontal_flip=True)
ts_generator = datagen_ts.flow_from_directory(image_folder + '/train', target_size=(image_size, image_size),color_mode='grayscale', batch_size=batch_size, class_mode='categorical', shuffle=True)

datagen_validation = ImageDataGenerator(horizontal_flip=True)
validation_generator = datagen_validation.flow_from_directory(image_folder + '/test', target_size=(image_size, image_size),color_mode='grayscale', batch_size=batch_size, class_mode='categorical', shuffle=True)

# Use convnet as model https://en.wikipedia.org/wiki/Convolutional_neural_network
model = Sequential()

# Layer 1
model.add(Conv2D(32,(3,3),padding='same',input_shape=(image_size,image_size,1)))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# Layer 2
model.add(Conv2D(64,(5,5),padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# Layer 3
model.add(Conv2D(128,(4,4),padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# Layer 4
model.add(Conv2D(128,(4,4),padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

# enough layers
model.add(Flatten())

# Connet layers
# Adding a fully connected layer
model.add(Dense(units=64))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(units=128, activation='relu'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(units=26, activation='softmax'))

optimizer=Adam(lr=0.0005)
model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
model.summary()

model.fit_generator(
    ts_generator, 
    steps_per_epoch=ts_generator.n//ts_generator.batch_size,
    epochs=120,
    validation_data=validation_generator,
    validation_steps=validation_generator.n//validation_generator.batch_size)

# save the model
model_json = model.to_json()
with open('model/model.json', "w") as json_file:
    json_file.write(model_json)

model.save_weights('model/model-weights.h5')
# Save status if we want to refit
model.save('model/model-full', save_format='tf')

# to load
# load_model = tf.keras.models.load_model('')
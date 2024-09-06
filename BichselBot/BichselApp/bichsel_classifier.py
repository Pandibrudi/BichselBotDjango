import os
import glob
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
from keras.layers import MaxPooling2D, Conv2D, MaxPooling2D, Activation, Dropout, Flatten, Dense, Input
from keras.models import Sequential
from django.conf import settings
from django.http import HttpResponse
from keras.utils import img_to_array, load_img
from keras import backend as K
import numpy as np

# Definiere Bildgrößen und Eingabeform
img_width, img_height = 180, 180

if K.image_data_format() == 'channels_first':
    input_shape = (3, img_width, img_height)
else:
    input_shape = (img_width, img_height, 3)

# Erstelle das Modell
model = Sequential()
model.add(Input(shape=input_shape))
model.add(Conv2D(32, (2, 2), input_shape=input_shape))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(32, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Conv2D(64, (2, 2)))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))

model.add(Flatten())
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(1))
model.add(Activation('sigmoid'))

# Kompiliere das Modell
model.compile(loss='binary_crossentropy',
              optimizer='rmsprop',
              metrics=['accuracy'])

# Lade die Gewichte
model.load_weights('BichselApp/bichsel_model.h5')

def prepare_image(image_path):
    # Bild laden
    img = load_img(image_path, target_size=(img_width, img_height))
    # Bild in ein Array umwandeln
    img_array = img_to_array(img)
    # Normalisierung wie beim Training
    img_array = img_array / 255.0
    # Bild in das erwartete Eingabeformat konvertieren (Batch)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array


def ask_bichsel(image_path):

    filename = os.path.basename(image_path)
    print(filename)
    # Bild vorbereiten
    img = prepare_image(image_path)
    
    # Vorhersage treffen
    prediction = model.predict(img)
    
    # Rückgabe je nach Vorhersage
    if prediction[0][0] > 0.5:
        return f"Zu '{filename}' sage ich 'Tisch'."
    else:
        return f"Zu '{filename}' sage ich 'Stuhl'."


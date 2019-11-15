import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image

from pydub import AudioSegment
from pydub.silence import split_on_silence

import numpy as np
import os

import utils

CLASS_NAME = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h',
    8: 'i',
    9: 'j',
    10: 'k',
    11: 'l',
    12: 'm',
    13: 'n',
    14: 'o',
    15: 'p',
    16: 'q',
    17: 'r',
    18: 's',
    19: 't',
    20: 'u',
    21: 'v',
    22: 'w',
    23: 'x',
    24: 'y',
    25: 'z'
}

class Model:
    def __init__(self, n_alpha=26, weight='weight/weight.h5'):
        super().__init__()

        self.n_alpha = n_alpha
        self.model = None
        self.weight = os.path.abspath(weight)

        self.audio_path = os.path.abspath('audio')
        # self.wav_audio_path = os.path.abspath('wav_audio')
        self.audio_split_path = os.path.abspath('split_audio')
        self.specgram_split_path = os.path.abspath('split_specgram')

        return self._create()

    def _create(self):
        model = tf.keras.Sequential()

        model.add(layers.Conv2D(64, (3,3), activation='relu', input_shape=(150, 150, 3)))
        model.add(layers.MaxPooling2D(2,2))

        model.add(layers.Conv2D(64, (3,3), activation='relu'))
        model.add(layers.MaxPooling2D(2,2))

        model.add(layers.Conv2D(128, (3,3), activation='relu'))
        model.add(layers.MaxPooling2D(2,2))

        model.add(layers.Conv2D(128, (3,3), activation='relu'))
        model.add(layers.MaxPooling2D(2,2))

        model.add(layers.Flatten())
        model.add(layers.Dropout(0.5))

        # FC layer
        model.add(layers.Dense(512, activation='relu'))
        model.add(layers.Dense(self.n_alpha, activation='softmax'))

        model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

        model.load_weights(self.weight)

        self.model = model
        return self.model

    def _preprocess(self, filename):
        """
            filename: filename.m4a

            return spectogram file path.
        """
        audio_file = os.path.join(self.audio_path, filename)
        audio = AudioSegment.from_file(audio_file, "mp4")

        average_loudness = audio.dBFS
        chunks = split_on_silence(
            audio, 
            min_silence_len = 100, 
            silence_thresh = average_loudness - 10, 
            keep_silence = 100
        )

        specgram_file_paths = []

        n_chunks = len(chunks)
        for i in range(n_chunks):
            spec_file_name = "%s_chunk%d.png" %(filename[:-4], i)
            output_path = os.path.join(self.specgram_split_path, spec_file_name)
            utils.plot_spectogram(chunks[i], chunks[i].frame_rate, output_path)

            specgram_file_paths.append(output_path)

        return specgram_file_paths

    def predict(self, filename):
        """
            filename: filename.m4a
        """
        specgram_file_paths = self._preprocess(filename)

        images = np.empty([0, 150, 150, 3])
        for specgram_img in specgram_file_paths:
            temp = image.load_img(specgram_img, target_size=(150, 150))
            x = image.img_to_array(temp)
            x = np.expand_dims(x, axis=0)
            
            images = np.vstack((images, x))

        model_results = self.model.predict(images)
        result = ''.join([CLASS_NAME[np.argmax(model_result)] for model_result in model_results])

        return result

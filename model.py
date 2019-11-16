import tensorflow as tf
from tensorflow.keras import layers
from tensorflow.keras.preprocessing import image

from pydub import AudioSegment
from pydub.silence import split_on_silence

from scipy import signal
from scipy.io import wavfile

import numpy as np
import os

import utils

CLASS_NAME = {
    0: 'l',
    1: 'k',
    2: 'g',
    3: 'm',
    4: 'i',
    5: 'n',
    6: 'v',
    7: 's',
    8: 'e',
    9: 'u',
    10: 'q',
    11: 'r',
    12: 'p',
    13: 'w',
    14: 'y',
    15: 'j',
    16: 'c',
    17: 't',
    18: 'b',
    19: 'x',
    20: 'a',
    21: 'f',
    22: 'o',
    23: 'z',
    24: 'h',
    25: 'd'
}

class Model:
    def __init__(self, n_alpha=26, weight='weight/weight.h5'):
        super().__init__()

        self.n_alpha = n_alpha
        self.weight = weight

        self.audio_path = os.path.abspath('audio')
        self.wav_audio_path = os.path.abspath('wav_audio')
        self.audio_split_path = os.path.abspath('split_audio')
        self.specgram_split_path = os.path.abspath('split_specgram')

        self.model = self._create()


    # def __new__(cls, n_alpha=26, weight='weight/weight.h5'):
    #     return super(Model, cls).__init__(n_alpha, weight)

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
        audio = AudioSegment.from_file(audio_file, "m4a")

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
            wav_file_name = "%s_chunk%d.wav" %(filename.split('/')[-1][:-4], i)
            wav_output_path = os.path.join(self.wav_audio_path, wav_file_name)
            chunks[i].export(wav_output_path, "wav")
            
            sample_rate, samples = wavfile.read(wav_output_path)

            spec_file_name = "%s_chunk%d.png" %(filename.split('/')[-1][:-4], i)
            output_path = os.path.join(self.specgram_split_path, spec_file_name)
            utils.plot_spectogram(samples, sample_rate, output_path)

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

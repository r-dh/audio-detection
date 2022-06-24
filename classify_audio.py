import streamlit as st
from pydub import AudioSegment
import tensorflow as tf
import numpy as np
import io 

from tensorflow.keras import layers
from tensorflow.keras import models

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
          instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper


@singleton
class ClassifyAudio:
  def __init__(self):
    self.model = tf.keras.models.load_model('model/audio_model') # hardcoded
    self.classes = np.genfromtxt("classes.txt", dtype='str')     # hardcoded

  def _get_spectrogram(self, waveform):
    # Zero-padding for an audio waveform with less than 16,000 samples.
    input_len = 16000
    waveform = waveform[:input_len]
    zero_padding = tf.zeros(
        [16000] - tf.shape(waveform),
        dtype=tf.float32)
    # Cast the waveform tensors' dtype to float32.
    waveform = tf.cast(waveform, dtype=tf.float32)
    # Concatenate the waveform with `zero_padding`, which ensures all audio
    # clips are of the same length.
    equal_length = tf.concat([waveform, zero_padding], 0)
    # Convert the waveform to a spectrogram via a STFT.
    spectrogram = tf.signal.stft(
        equal_length, frame_length=255, frame_step=128)
    # Obtain the magnitude of the STFT.
    spectrogram = tf.abs(spectrogram)
    # Add a `channels` dimension, so that the spectrogram can be used
    # as image-like input data with convolution layers (which expect
    # shape (`batch_size`, `height`, `width`, `channels`).
    spectrogram = spectrogram[None, ..., tf.newaxis]
    return spectrogram


  def analyse(self, filename):
    data_load_state = st.text(f"Analysing...{filename}")
    
    audio_file = tf.io.read_file(filename)
    decoded_audio, _ = tf.audio.decode_wav(contents=audio_file)

    waveform = tf.squeeze(decoded_audio, axis=-1)
    spectogram = self._get_spectrogram(waveform)

    prediction = self.model(spectogram)
    st.write("Analysis result:", prediction)
    st.write(self.classes[np.argmax(prediction, axis=1)])




st.title('Audio classification and labeling')

st.write("Upload audio track to analyse")

audio_classifier = ClassifyAudio()

uploaded_file = st.file_uploader("Choose a file", type=["wav", "mp3"])
if uploaded_file is not None:
  file_path = "./temp/" + uploaded_file.name[:-3] + "wav" # hardcoded
  filetype = uploaded_file.name[:3]
  st.audio(uploaded_file.getvalue(), format=f'audio/{filetype}')
  sound = AudioSegment.from_file(io.BytesIO(uploaded_file.getvalue()), format=filetype)
  sound = sound.set_channels(1)
  sound.export(file_path, format="wav")

  audio_classifier.analyse(str(file_path))

# radio/audio.py
import sounddevice as sd
import numpy as np

def play_audio(audio_data, sample_rate=48000):
    audio_data = np.clip(audio_data, -1, 1)
    sd.play(audio_data, samplerate=sample_rate, blocking=False)

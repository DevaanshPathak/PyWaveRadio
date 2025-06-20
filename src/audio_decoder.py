# src/audio_decoder.py

import numpy as np
import scipy.signal as signal
import sounddevice as sd

# FM demodulation using phase difference
def fm_demodulate(iq: np.ndarray, fs: int = 2_000_000):
    phase = np.angle(iq)
    diff = np.diff(phase)
    demodulated = np.unwrap(diff)
    audio = signal.resample(demodulated, int(len(demodulated) * 44100 / fs))
    return np.real(audio)

# Play audio from array
def play_audio(audio: np.ndarray):
    sd.play(audio, samplerate=44100)

# Full pipeline
def play_fm(iq_samples: np.ndarray):
    try:
        audio = fm_demodulate(iq_samples)
        play_audio(audio)
    except Exception as e:
        print(f"[FM Decoder] Error: {e}")

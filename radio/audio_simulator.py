# radio/audio_simulator.py
import numpy as np
import sounddevice as sd
import threading

def play_tone(frequency_hz=1000.0, sample_rate=44100):
    duration = 1e10  # simulate continuous tone (long duration)
    t = np.linspace(0, duration, int(sample_rate * 5), False)
    tone = 0.1 * np.sin(2 * np.pi * frequency_hz * t)

    def play():
        while True:
            sd.play(tone, samplerate=sample_rate)
            sd.wait()

    thread = threading.Thread(target=play, daemon=True)
    thread.start()

def stop_audio():
    sd.stop()

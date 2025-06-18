# src/audio_output.py
import sounddevice as sd

class AudioOutput:
    def __init__(self, sample_rate=48000):
        self.sample_rate = sample_rate

    def play(self, data):
        sd.play(data, self.sample_rate, blocking=False)

    def stop(self):
        sd.stop()

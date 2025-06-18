# src/sdr_interface.py
import numpy as np

class SDRInterface:
    def __init__(self, frequency=100e6, sample_rate=48000):
        self.sample_rate = sample_rate
        self.frequency = frequency

    def start(self):
        print(f"[Mock SDR] Starting at {self.frequency / 1e6:.2f} MHz")

    def read_samples(self, num_samples):
        # Simulate a 1kHz sine wave
        t = np.arange(num_samples) / self.sample_rate
        wave = 0.5 * np.sin(2 * np.pi * 1000 * t)
        return wave.astype(np.float32)

    def stop(self):
        print("[Mock SDR] Stopping...")

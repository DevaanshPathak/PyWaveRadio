# radio/sdr.py
import numpy as np

class SDR:
    def __init__(self, frequency=100e6, sample_rate=2.4e6, gain=40):
        self.frequency = frequency
        self.sample_rate = sample_rate
        self.gain = gain
        self.running = False

    def start(self):
        self.running = True

    def read_samples(self, num_samples=1024*16):
        # Simulate a dummy sine wave for now (mock data)
        t = np.arange(num_samples) / self.sample_rate
        iq = np.exp(2j * np.pi * 1e3 * t)  # 1 kHz tone
        return iq.astype(np.complex64)

    def stop(self):
        self.running = False

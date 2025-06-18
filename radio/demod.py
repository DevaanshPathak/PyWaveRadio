# radio/demod.py
import numpy as np

def fm_demodulate(iq_data):
    # Basic FM demodulation
    phase = np.angle(iq_data)
    diff = np.diff(phase)
    return np.concatenate(([0], diff))  # Pad first sample

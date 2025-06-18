# test_rtl.py

from src.rtl_driver import RTL_TCPDriver
import matplotlib.pyplot as plt
import numpy as np

driver = RTL_TCPDriver(freq_hz=100e6, mock=True)

samples = driver.get_samples(5)  # Get ~5 batches

# Basic waveform preview
plt.plot(np.real(samples[:500]), label="Real")
plt.plot(np.imag(samples[:500]), label="Imag")
plt.title("Waveband IQ Sample Preview")
plt.legend()
plt.show()

driver.close()

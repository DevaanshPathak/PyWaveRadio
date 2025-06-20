# spectrum_gui.py
import matplotlib.pyplot as plt
import numpy as np

def run_gui_spectrum():
    t = np.linspace(0, 1, 1024)
    y = np.sin(2 * np.pi * 10 * t) + 0.5 * np.random.randn(1024)

    Y = np.fft.fft(y)
    f = np.fft.fftfreq(len(Y), d=1/1024)

    plt.figure("Spectrum Analyzer")
    plt.plot(f[:len(f)//2], np.abs(Y[:len(Y)//2]))
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.title("Simulated Spectrum")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

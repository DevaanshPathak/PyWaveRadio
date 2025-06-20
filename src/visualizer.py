import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Global buffer to hold the latest spectrum data
latest_samples = np.zeros(1024)

def set_latest_samples(samples):
    """Update the global sample buffer (should be called from another thread)."""
    global latest_samples
    if samples is not None and len(samples) > 0:
        latest_samples = samples[:1024]

def run_gui_spectrum():
    """Launch a separate GUI window showing live FFT spectrum."""
    global latest_samples

    fig, ax = plt.subplots()
    x_data = np.fft.fftfreq(len(latest_samples), d=1/2.4e6)[:len(latest_samples)//2]
    line, = ax.plot(x_data, np.zeros_like(x_data))

    ax.set_title("Live Spectrum Analyzer")
    ax.set_xlabel("Frequency (Hz)")
    ax.set_ylabel("Magnitude")
    ax.set_ylim(0, 100)
    ax.set_xlim(0, 1.2e6)  # Adjust based on RTL-SDR sample rate

    def update(frame):
        try:
            global latest_samples
            if len(latest_samples) > 0:
                fft = np.fft.fft(latest_samples)
                magnitude = 20 * np.log10(np.abs(fft[:len(fft)//2]) + 1e-6)
                line.set_ydata(magnitude)
        except Exception as e:
            print(f"[DEBUG] Spectrum update error: {e}")
        return line,

    ani = animation.FuncAnimation(
        fig,
        update,
        interval=200,
        blit=True,
        cache_frame_data=False,
        save_count=100,
    )

    plt.tight_layout()
    plt.show()

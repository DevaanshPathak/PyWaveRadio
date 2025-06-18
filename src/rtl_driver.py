# src/rtl_driver.py

import SoapySDR
from SoapySDR import *  # SOAPY_SDR_ constants
import numpy as np

class RTL_TCPDriver:
    def __init__(self, server_ip="127.0.0.1", server_port=1234, freq_hz=100e6, sample_rate=2.1e6, mock=False):
        self.mock = mock
        self.total_samples = 0

        if self.mock:
            print("[RTL_TCPDriver] Running in mock mode — no real SDR.")
            self.buff = np.array([0]*2048, np.complex64)
            return

        self.args = dict(driver="rtltcp", rtltcp=f"{server_ip}:{server_port}")
        print(f"[RTL_TCPDriver] Connecting to {server_ip}:{server_port}")
        self.sdr = SoapySDR.Device(self.args)

        self.sdr.setSampleRate(SOAPY_SDR_RX, 0, sample_rate)
        self.sdr.setFrequency(SOAPY_SDR_RX, 0, freq_hz)

        self.rx_stream = self.sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
        self.sdr.activateStream(self.rx_stream)

        self.buff = np.array([0]*2048, np.complex64)

    def get_samples(self, num_batches=1):
        samples = []

        if self.mock:
            for _ in range(num_batches):
                mock_data = (np.random.randn(2048) + 1j*np.random.randn(2048)) * 0.1
                samples.extend(mock_data)
                self.total_samples += len(mock_data)
            return np.array(samples, dtype=np.complex64)

        for _ in range(num_batches):
            result = self.sdr.readStream(self.rx_stream, [self.buff], len(self.buff))
            if result.ret > 0:
                samples.extend(self.buff[:result.ret])
                self.total_samples += result.ret
        return np.array(samples, dtype=np.complex64)

    def close(self):
        if self.mock:
            print(f"[RTL_TCPDriver] (Mock) Closed after {self.total_samples} samples.")
            return
        print(f"[RTL_TCPDriver] Closing stream after {self.total_samples} samples.")
        self.sdr.deactivateStream(self.rx_stream)
        self.sdr.closeStream(self.rx_stream)

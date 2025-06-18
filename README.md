# 📻 PyWaveRadio TUI

**PyWaveRadio** is a Textual-based TUI (Text User Interface) SDR radio simulator that lets you tune virtual radio frequencies with a classic look and feel.

It supports real SDR input via RTL-SDR and mock data from Hack Club's Waveband server — perfect for demos, exploration, and learning!

---

## ✨ Features

- 🎛️ Frequency tuning (AM, SW, FM bands)
- 🔖 Bookmark stations
- 🔍 Frequency scanning mode
- 🎵 Audio tone simulation per frequency
- 📈 Dynamic waveform visualization (live IQ or simulated)
- 💾 Saves last frequency tuned (`config.json`)
- 💻 Fully works offline with mock data
- 🧪 Real hardware support via `RTL_TCPDriver` (optional)

---

## 🚦 How it works

- **Default mode**: Pulls **mock IQ data from Hack Club’s Waveband server** (offline, simulated)
- **Real SDR mode**: If RTL-SDR is connected and SoapySDR is installed, it uses **live IQ samples** via `rtl_tcp`

> 🔌 Auto-switches to mock data if no device is detected!

---

## 🧰 Installation

1. **Clone the repo**
    ```bash
    git clone https://github.com/yourname/pywaveradio
    cd pywaveradio
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **(Optional) Install RTL-SDR support**
    - Install [SoapySDR](https://github.com/pothosware/SoapySDR)
    - Install [SoapyRTLSDR plugin](https://github.com/pothosware/SoapyRTLSDR)
    - Connect an RTL-SDR dongle via USB

---

## ▶️ Run the App

```bash
python run_radio.py
````

Use `+` / `-` keys or buttons to change frequencies.
Use preset buttons (AM / SW / FM) to jump to bands.
Click "🔖 Save" to bookmark current frequency.

---

## 📁 Project Structure

```
PyWaveRadio/
├── run_radio.py           # Entry point
├── radio/
│   ├── tui_app.py         # TUI logic
│   ├── audio_simulator.py # Beep tone logic
│   └── rtl_driver.py      # SDR + mock IQ sample logic
├── config.json            # Stores last frequency
├── style.css              # TUI styling
└── README.md
```

---

## 💡 About Hack Club's Waveband

When no RTL-SDR device is available, PyWaveRadio uses **mock IQ samples** from **Hack Club's Waveband initiative**, simulating a believable signal pattern to visualize and tune as if using real hardware.

---

## 👤 Author

Built with ❤️ for Hack Club’s Waveband program.

> Devaansh Pathak – [GitHub](https://github.com/devaansh-pathak)

---

## 🛠 License

MIT License

# PyWaveRadio 📻

**PyWaveRadio** is a terminal-based AM/FM/Shortwave mock radio tuner built with Python and [Textual](https://textual.textualize.io/). It simulates frequency tuning, audio playback, station scanning, bookmarking, and even displays a live waveform visualizer — all without requiring an actual SDR device.

> 🚧 This project currently uses mocked audio and frequency data. Real SDR integration (e.g., via SoapySDR) is planned for later versions.

---

## 🎯 Features

- 🎛️ TUI interface for tuning and navigation
- 🎧 Frequency-based tone simulation (mock audio)
- 🔁 Scan mode with station auto-tuning
- 📌 Station bookmarking and persistence
- 📈 Waveform visualization of played tone
- 🧪 Built for Hack Club’s Solder program

---

## 🧰 Tech Stack

- **Python 3.9**
- [Textual](https://github.com/Textualize/textual)
- NumPy, SciPy
- sounddevice (for tone playback)

---

## 🚀 Getting Started

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/PyWaveRadio.git
cd PyWaveRadio
````

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
python run.py
```

---

## 🗂️ Project Structure

```
PyWaveRadio/
├── run.py                 # Entry point for the TUI app
├── requirements.txt
├── README.md
├── tui/
│   ├── app.py             # Main TUI interface
│   └── style.css          # UI styling
├── radio/
│   ├── audio_simulator.py # Plays frequency-based tones
│   ├── scan.py            # Simulates scanning stations
│   ├── bookmarks.py       # Save/load bookmarks
│   └── visualizer.py      # Waveform visualizer
└── devlogs/
    ├── day1.txt
    ├── day2.txt
    └── day3.txt
```

---

## 📻 Demo

```bash
📻 Frequency: 100.00 MHz
[➖] [➕]

~ Audio tone plays based on frequency ~
~ Waveform reacts visually in real-time ~
```

---

## 📦 Future Plans

* ✅ Add scan mode and bookmarks
* ⏳ Real SDR input via SoapySDR + RTL-SDR dongle
* ⏳ Web interface or cross-platform GUI
* ⏳ Export bookmarks and session replay

---

## 🛠️ Built By

Devaansh Pathak
Built for [Hack Club](https://hackclub.com/) Waveband program 🔩

---

## ⚠️ Disclaimer

This is a **simulation** project. It does **not** receive real radio signals — yet!

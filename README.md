# 📻 PyWaveRadio

**PyWaveRadio** is a terminal-based software-defined radio (SDR) interface with real-time waveform and spectrum visualization using RTL-SDR and a Textual TUI. It also includes a Matplotlib-powered spectrum GUI you can toggle from the terminal.

---

## 🛰️ Features

- 🎛️ TUI-based frequency tuning (AM / SW / FM bands)
- 📈 Real-time waveform and spectrum bars in terminal
- 🔖 Save and load frequency bookmarks
- 🌙 Light/Dark theme toggle
- 🔍 Auto-scan mode
- 📊 Optional external GUI spectrum viewer using Matplotlib

---

## 💻 Requirements

- Python **3.9.x** (RTL-SDR bindings require 3.9)
- RTL-SDR dongle or compatible SDR hardware
- OS: Windows, Linux, or macOS

---

## 📦 Installation

### 1. Clone the repo

```bash
git clone https://github.com/DevaanshPathak/PyWaveRadio.git
cd PyWaveRadio
````

### 2. Create a virtual environment (Python 3.9 required)

```bash
python3.9 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate  # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Install RTL-SDR driver

Install `pyrtlsdr` or `SoapySDR`-based driver compatible with your RTL-SDR dongle.

> On Windows, make sure the driver DLLs are in your PATH or project root.

---

## 🚀 Running the App

```bash
python run.py
```

Once inside the terminal UI:

* `+` / `-` or buttons: Increase/decrease frequency
* `b`: Open bookmarks menu
* `t`: Toggle light/dark theme
* `📈 GUI Spectrum`: Launch real-time Matplotlib spectrum viewer in separate window

---

## 📁 Project Structure

```
PyWaveRadio/
├── tui/
│   └── app.py              # Main TUI code
├── src/
│   ├── rtl_driver.py       # RTL-SDR driver wrapper
│   └── visualizer.py       # Spectrum GUI with matplotlib
├── run.py                  # Entry point
├── config.json             # Stores bookmarks & last state
└── requirements.txt
```

---

## ❗ Troubleshooting

### `AttributeError: 'RenderStyles' object has no attribute 'set_variables'`

You're using a newer Textual method on an older version. Use `self.styles.background = ...` instead, or upgrade Textual if possible.

### `__init__() got an unexpected keyword argument 'show_cursor'`

You're using `show_cursor=True` with an older version of `textual`. Remove that argument.

---

## 🛠️ Dependencies

```txt
textual==0.36.0
numpy
matplotlib
rtlsdr  # or SoapySDR (based on rtl_driver implementation)
```

> You can adjust this list in `requirements.txt`.

---

## 📜 License

MIT License — see `LICENSE` for details.

---

Made with ❤️ by Devaansh Pathak

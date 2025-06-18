from textual.app import App, ComposeResult
from textual.widgets import Static, Button
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events
from textual.timer import Timer

from radio.audio_simulator import play_tone, stop_audio
import json
import os
import random

CONFIG_PATH = "config.json"

def load_last_frequency() -> float:
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                data = json.load(f)
                return float(data.get("last_frequency", 100.0))
            except (json.JSONDecodeError, ValueError):
                return 100.0
    return 100.0

def save_frequency(frequency: float):
    with open(CONFIG_PATH, "w") as f:
        json.dump({"last_frequency": frequency}, f)

def get_band(frequency: float) -> str:
    if 0.5 <= frequency <= 1.6:
        return "AM"
    elif 3.0 <= frequency <= 30.0:
        return "SW"
    elif 88.0 <= frequency <= 108.0:
        return "FM"
    return "Unknown"


class FrequencyDisplay(Static):
    def update_text(self, freq_mhz: float):
        band = get_band(freq_mhz)
        self.update(f"📻 Frequency: {freq_mhz:.2f} MHz\n🎙 Band: {band}")


class WaveformDisplay(Static):
    def update_waveform(self):
        bar = ''.join(random.choice("▁▂▃▄▅▆▇█") for _ in range(40))
        self.update(f"🎵 {bar}")


class RadioApp(App):
    CSS_PATH = "style.css"
    frequency_mhz = reactive(load_last_frequency())
    bookmarks = reactive([])

    def compose(self) -> ComposeResult:
        self.freq_display = FrequencyDisplay()
        self.waveform = WaveformDisplay()
        yield Container(
            self.freq_display,
            Horizontal(
                Button("➖", id="decrease"),
                Button("➕", id="increase"),
                Button("🔖 Save", id="bookmark"),
                Button("🔍 Scan", id="scan"),
            ),
            Horizontal(
                Button("AM", id="set_am"),
                Button("SW", id="set_sw"),
                Button("FM", id="set_fm"),
            ),
            self.waveform,
        )

    def on_mount(self) -> None:
        self.freq_display.update_text(self.frequency_mhz)
        play_tone(self.frequency_mhz * 10)
        self.waveform_timer: Timer = self.set_interval(0.3, self.waveform.update_waveform)
        self.scan_timer: Timer | None = None

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id = event.button.id
        if button_id == "increase":
            if self.frequency_mhz + 0.1 <= 108.0:
                self.change_frequency(+0.1)
        elif button_id == "decrease":
            if self.frequency_mhz - 0.1 >= 0.5:
                self.change_frequency(-0.1)
        elif button_id == "set_am":
            self.set_frequency(1.0)
        elif button_id == "set_sw":
            self.set_frequency(10.0)
        elif button_id == "set_fm":
            self.set_frequency(100.0)
        elif button_id == "bookmark":
            self.bookmarks.append(round(self.frequency_mhz, 2))
            self.notify(f"🔖 Bookmarked {self.frequency_mhz:.2f} MHz")
        elif button_id == "scan":
            if self.scan_timer and self.scan_timer.running:
                self.scan_timer.stop()
                self.notify("🛑 Scan stopped.")
            else:
                self.notify("🔍 Starting scan...")
                self.scan_timer = self.set_interval(1.0, self.scan_step)

    def change_frequency(self, delta: float):
        new_freq = round(self.frequency_mhz + delta, 2)
        self.set_frequency(new_freq)

    def set_frequency(self, value: float):
        self.frequency_mhz = round(value, 2)
        self.freq_display.update_text(self.frequency_mhz)
        stop_audio()
        play_tone(self.frequency_mhz * 10)
        save_frequency(self.frequency_mhz)

    def scan_step(self):
        if self.frequency_mhz >= 108.0:
            self.scan_timer.stop()
            self.notify("✅ Scan complete.")
        else:
            self.change_frequency(+0.5)

    def on_key(self, event: events.Key) -> None:
        if event.key == "+":
            self.change_frequency(+0.1)
        elif event.key == "-":
            self.change_frequency(-0.1)

    def notify(self, message: str):
        self.waveform.update(f"🔔 {message}")

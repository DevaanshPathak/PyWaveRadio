import matplotlib
matplotlib.use("TkAgg")  # GUI backend for matplotlib to avoid crashing

from textual.app import App, ComposeResult
from textual.widgets import Static, Button, ListView, ListItem, Label
from textual.containers import Container, Horizontal
from textual.reactive import reactive
from textual import events
from textual.timer import Timer
from textual.screen import ModalScreen

from src.rtl_driver import RTL_TCPDriver
import json
import os
import random
import numpy as np
import threading
from spectrum_gui import run_gui_spectrum

CONFIG_PATH = "config.json"


def load_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError as e:
                print(f"[DEBUG] Failed to parse config: {e}")
                return {}
    return {}


def save_config(config):
    try:
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
    except Exception as e:
        print(f"[DEBUG] Failed to save config: {e}")


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
        self.update(f"🎻 Frequency: {freq_mhz:.2f} MHz\n🎧 Band: {band}")


class WaveformDisplay(Static):
    def update_waveform(self, samples=None):
        try:
            if samples is not None and len(samples) > 0:
                magnitudes = np.abs(samples[:80])
                max_val = np.max(magnitudes)
                normalized = (magnitudes / max_val) * 8 if max_val > 0 else np.zeros_like(magnitudes)
                chars = "▁▂▃▄▅▆▇█"
                bar = ''.join(chars[min(int(val), 7)] for val in normalized)
            else:
                bar = ''.join(random.choice("▁▂▃▄▅▆▇█") for _ in range(40))
            self.update(f"🎵 {bar}")
        except Exception as e:
            self.update(f"❌ Error: {e}")
            print(f"[DEBUG] Waveform error: {e}")


class SpectrumDisplay(Static):
    def update_spectrum(self, samples):
        try:
            if samples is None or len(samples) == 0:
                self.update("📉 No signal")
                return
            fft_result = np.fft.fft(np.real(samples))
            fft_magnitude = np.abs(fft_result[:80])
            max_val = np.max(fft_magnitude)
            normalized = (fft_magnitude / max_val) * 8 if max_val > 0 else np.zeros_like(fft_magnitude)
            chars = "▁▂▃▄▅▆▇█"
            bar = ''.join(chars[min(int(val), 7)] for val in normalized)
            self.update(f"📊 {bar}")
        except Exception as e:
            self.update(f"❌ FFT error: {e}")
            print(f"[DEBUG] Spectrum error: {e}")


class BookmarkScreen(ModalScreen):
    def __init__(self, bookmarks, callback):
        super().__init__()
        self.bookmarks = sorted(set(bookmarks))
        self.callback = callback

    def compose(self) -> ComposeResult:
        items = [ListItem(Label(f"{f:.2f} MHz")) for f in self.bookmarks]
        self.list_view = ListView(*items, id="bookmark-list", show_cursor=True)
        yield self.list_view

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        label = event.item.query_one(Label)
        freq_str = label.renderable.replace(" MHz", "")
        try:
            freq = float(freq_str)
            self.dismiss(freq)
        except ValueError:
            self.dismiss(None)


class RadioApp(App):
    CSS_PATH = "style.css"
    BINDINGS = [
        ("t", "toggle_theme", "Toggle Theme"),
        ("b", "open_bookmarks", "Open Bookmarks")
    ]

    frequency_mhz = reactive(100.0)
    bookmarks = reactive([])
    dark = reactive(True)

    def compose(self) -> ComposeResult:
        self.freq_display = FrequencyDisplay()
        self.waveform = WaveformDisplay()
        self.spectrum = SpectrumDisplay()
        yield Container(
            self.freq_display,
            Horizontal(
                Button("➖", id="decrease"),
                Button("➕", id="increase"),
                Button("🔖 Save", id="bookmark"),
                Button("📚 Bookmarks", id="bookmark_menu"),
                Button("🎨 Theme", id="theme_toggle"),
                Button("🔍 Scan", id="scan"),
                Button("📈 GUI Spectrum", id="open_gui_spectrum"),
            ),
            Horizontal(
                Button("AM", id="set_am"),
                Button("SW", id="set_sw"),
                Button("FM", id="set_fm"),
            ),
            self.waveform,
            self.spectrum,
        )

    def on_mount(self) -> None:
        config = load_config()
        self.frequency_mhz = float(config.get("last_frequency", 100.0))
        self.bookmarks = config.get("bookmarks", [])
        self.dark = config.get("dark", True)

        try:
            self.driver = RTL_TCPDriver(freq_hz=self.frequency_mhz * 1e6)
            self.freq_display.update_text(self.frequency_mhz)
            self.waveform_timer: Timer = self.set_interval(0.8, self.update_waveform)
            self.scan_timer: Timer | None = None
        except Exception as e:
            self.waveform.update(f"❌ Init failed: {e}")
            print(f"[DEBUG] Init failed: {e}")
            self.driver = None
            self.waveform_timer: Timer = self.set_interval(1.0, lambda: self.waveform.update_waveform())

    def update_waveform(self):
        try:
            if self.driver:
                samples = self.driver.get_samples(1)
                self.waveform.update_waveform(samples)
                self.spectrum.update_spectrum(samples)
            else:
                self.waveform.update_waveform()
                self.spectrum.update_spectrum(None)
        except Exception as e:
            print(f"[DEBUG] update_waveform error: {e}")

    def change_frequency(self, delta: float):
        self.set_frequency(round(self.frequency_mhz + delta, 2))

    def set_frequency(self, value: float):
        self.frequency_mhz = round(value, 2)
        self.freq_display.update_text(self.frequency_mhz)
        self.save_state()
        try:
            if self.driver:
                self.driver.set_frequency(self.frequency_mhz * 1e6)
        except Exception as e:
            print(f"[DEBUG] set_frequency error: {e}")

    def save_state(self):
        save_config({
            "last_frequency": self.frequency_mhz,
            "bookmarks": self.bookmarks,
            "dark": self.dark
        })

    def scan_step(self):
        if self.frequency_mhz >= 108.0:
            self.scan_timer.stop()
            self.notify("✅ Scan complete.")
        else:
            self.change_frequency(+0.5)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        try:
            button_id = event.button.id
            if button_id == "increase":
                self.change_frequency(+0.1)
            elif button_id == "decrease":
                self.change_frequency(-0.1)
            elif button_id == "set_am":
                self.set_frequency(1.0)
            elif button_id == "set_sw":
                self.set_frequency(10.0)
            elif button_id == "set_fm":
                self.set_frequency(100.0)
            elif button_id == "bookmark":
                self.bookmarks.append(round(self.frequency_mhz, 2))
                self.bookmarks = sorted(set(self.bookmarks))
                self.notify(f"🔖 Bookmarked {self.frequency_mhz:.2f} MHz")
                self.save_state()
            elif button_id == "bookmark_menu":
                self.open_bookmark_menu()
            elif button_id == "theme_toggle":
                self.action_toggle_theme()
            elif button_id == "scan":
                if self.scan_timer and self.scan_timer.running:
                    self.scan_timer.stop()
                    self.notify("🚑 Scan stopped.")
                else:
                    self.notify("🔍 Starting scan...")
                    self.scan_timer = self.set_interval(1.0, self.scan_step)
            elif button_id == "open_gui_spectrum":
                print("[DEBUG] Starting GUI spectrum thread...")
                threading.Thread(target=run_gui_spectrum, daemon=True).start()
        except Exception as e:
            print(f"[DEBUG] on_button_pressed error: {e}")

    def open_bookmark_menu(self):
        if not self.bookmarks:
            self.notify("📜 No bookmarks yet.")
            return

        def callback(freq):
            if freq:
                self.set_frequency(freq)

        self.push_screen(BookmarkScreen(self.bookmarks, callback))

    def action_toggle_theme(self):
        self.dark = not self.dark
        self.notify(f"🎨 Switched to {'dark' if self.dark else 'light'} mode")
        self.save_state()

    def action_open_bookmarks(self):
        self.open_bookmark_menu()

    def on_key(self, event: events.Key) -> None:
        if event.key == "+":
            self.change_frequency(+0.1)
        elif event.key == "-":
            self.change_frequency(-0.1)

    def notify(self, message: str):
        self.waveform.update(f"🔔 {message}")

    def on_exit(self) -> None:
        try:
            if self.driver:
                self.driver.close()
        except Exception as e:
            print(f"[DEBUG] on_exit error: {e}")

    def watch_dark(self, dark: bool) -> None:
        if dark:
            self.set_class(True, "-dark-mode")
            self.set_class(False, "-light-mode")
        else:
            self.set_class(True, "-light-mode")
            self.set_class(False, "-dark-mode")



if __name__ == "__main__":
    print("[DEBUG] Launching TUI app...")
    app = RadioApp()
    app.run()

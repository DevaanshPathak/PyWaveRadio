# run.py
from tui.app import RadioApp
from radio.audio_simulator import play_tone

if __name__ == "__main__":
    print("=== PyWaveRadio TUI ===")
    play_tone(1000)  # Simulate audio for 100 MHz (100 * 10 = 1000 Hz)
    RadioApp().run()

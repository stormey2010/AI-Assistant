from bar_main import seturl, run_app, url_setter
from PyQt5.QtCore import QTimer
import assist
import commands
import threading
import keyboard
from functions import dprint

def hotkey_listener():
    keyboard.add_hotkey('win+space', main)

def process_input(text):
    url_setter.main_window.hide_window()
    dprint("Input received from process_input:" + text)
    # Handle the input text and check for commands
    current_text = text.lower().strip().replace(".", "").replace(",", "").replace("?", "")
    
    command_found = commands.command(current_text)
    if not command_found:
        if assist.sound_playing():
            dprint("Sound is still playing.")
        else:
            response = assist.generate(current_text)
            dprint(response)
            assist.tts(response, True)
            seturl("https://jarvistts.netlify.app", response)
            QTimer.singleShot(100, lambda: url_setter.main_window.show())

def main():
    seturl("/web/bar_input.html", process_input)
    run_app()

if __name__ == '__main__':
    hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
    hotkey_thread.start()
    main()
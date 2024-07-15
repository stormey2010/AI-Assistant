import threading
import keyboard
from RealtimeSTT import AudioToTextRecorder
from functions import dprint
import assist
import commands
from config.config import *
import subprocess

#Vars
global recorder_stop


"""Bar initialize"""
def hotkey_listener():
    #Listen for the 'win+space' hotkey to show the bar, may have to change if on mac
    keyboard.add_hotkey('win+space', show_bar)

def show_bar():
    #Run the bar.py script when the hotkey is pressed.
    subprocess.run(["python", "bar.py"])

"""Main listener"""
if __name__ == '__main__':
    # Start the hotkey listener thread
    hotkey_thread = threading.Thread(target=hotkey_listener, daemon=True)
    hotkey_thread.start()

    # Initialize the speech to text
    recorder = AudioToTextRecorder(
        spinner=False, 
        model="tiny.en", 
        language="en", 
        post_speech_silence_duration=0.4, 
        silero_sensitivity=0.3
    )
    # Voice hotwords
    hot_words = [
        ASSISTANT_NAME, 
        "hey " + ASSISTANT_NAME, 
        "yo " + ASSISTANT_NAME, 
        "hello " + ASSISTANT_NAME, 
        ASSISTANT_BACKUPNAME, 
        "hey " + ASSISTANT_BACKUPNAME, 
        "yo " + ASSISTANT_BACKUPNAME, 
        "hello " + ASSISTANT_BACKUPNAME
    ]
    
    # Var
    skip_hot_word_check = False
    recorder_stop = False

    dprint("Listening")

    while True:
        current_text = recorder.text()
        dprint(current_text)
        
        # Stop the recorder if the stop flag is set
        if recorder_stop:
            recorder.stop()
            recorder_stop = False
        
        # Check if any hot words are in the current text or if skipping hot word check because of follow up
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
            if current_text:
                dprint("User: " + current_text)
                recorder.stop()
                # Try to find any commands in commands.py
                command_found = False
                for hot_word in hot_words:
                    if hot_word in current_text.lower():
                        current_text = current_text.lower().replace(hot_word + " ", "").strip().replace(".", "").replace(",", "").replace("?", "")
                        dprint(current_text)
                        command_found = commands.command(current_text)
                        break
                
                # Generate response if no command is found
                if not command_found:
                    if assist.sound_playing():
                        dprint("Sound is still playing.")
                    else:
                        response = assist.generate(current_text)
                        dprint("Ai:" + response)
                        done = assist.tts(response, False)
                        recorder.start()
                        skip_hot_word_check = "?" in response

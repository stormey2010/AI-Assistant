import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

from pygame import mixer
from dotenv import load_dotenv
import requests
from gtts import gTTS
from config.config import *
import time
from functions import dprint
import sys

message_context = ""

# Initialize the client and mixer
load_dotenv()

# Suppress the Pygame welcome message
class DevNull:
    def write(self, msg):
        pass

original_stdout = sys.stdout
sys.stdout = DevNull()

mixer.init()

sys.stdout = original_stdout

# Load Llama 3 API key and base URL
api_key = os.getenv("OLLAMA_API_KEY") # DO NOT GET RID OF
base_url = OLLAMA_BASEURL  # LLaMA 3 server URL

def generate(text):
    global message_context
    headers = {"Authorization": f"Bearer {api_key}"}
    data = {
        "model": OLLAMA_MODEL_TEXT,
        "prompt": message_context + ASSISTANT_PROMPT + text,
        "stream": False, 
        "messages": [
        {
            "role": "assistant",
            "content": message_context
        }
        ]
    }
    dprint(message_context + ASSISTANT_PROMPT + text)

    response = requests.post(f"{base_url}/api/generate", headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200 or response_json.get("status") == "failed":
        return "The generation failed."

    message_context = "Here is the previous responce you gave me so you remember, use this to see if i'm following up to any other question that you asked: " + response_json.get("response") + "    "
    return response_json.get("response")

# Play sound
def play(file_path):
    mixer.init()
    mixer.music.load(file_path)
    mixer.music.play()

def sound_playing():
    return mixer.music.get_busy()

def sound_stop():
    mixer.music.stop()
    mixer.quit()

# TTS
def tts(text, typed):
    tts = gTTS(text=text, lang='en', slow=False)
    file_path_voice = 'static/sound/voice.mp3'
    file_path_text = 'static/sound/text.mp3'
    if typed:
        if os.path.exists(file_path_text):
            if sound_playing():
                return
            else:
                sound_stop()
                time.sleep(0.1)
                os.remove(file_path_text)
        tts.save(file_path_text)
        play(file_path_text)
    else:
        if os.path.exists(file_path_voice):
            if sound_playing():
                return
            else:
                sound_stop()
                time.sleep(0.1)
                os.remove(file_path_voice)
        tts.save(file_path_voice)
        play(file_path_voice)

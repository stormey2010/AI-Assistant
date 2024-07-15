# Import all plugins from plugins folder
from functions import dprint
import plugins.seeimages
import assist
import plugins.youtube

def command(command):
    if command == "print":
        print("Hello World!")
    elif command == "stop" or command == "never mind":
        assist.sound_stop()
    elif command == "exit" or command == "quit":
        exit()
    elif command == "what do you see" or command == "capture" or command == "take picture":
        result = plugins.seeimages.capture_and_generate()
        dprint(result)
        assist.tts(result)
    elif command.startswith("play"):
        song_name = command.replace("play", "").strip()
        result = plugins.youtube.youtube_music(song_name)
        dprint(result)
        assist.play('static/sound/music.mp3')
    else:
        return False  # Indicate that the command is invalid
    return True  # Indicate that the command was successfully parsed

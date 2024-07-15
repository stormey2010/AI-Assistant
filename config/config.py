# Import the datetime module to work with dates and times, get time and date, and format them
from datetime import datetime
current_datetime = datetime.now()
formatted_datetime = current_datetime.strftime("%Y-%m-%d %I:%M %p")

# Ollama Base URL
OLLAMA_BASEURL = ""

# Ollama Model Name for text conversation
OLLAMA_MODEL_TEXT = ""

# Ollama Model Name for image analization
OLLAMA_MODEL_IMAGE = ""

# Define the assistant's name
ASSISTANT_NAME = ""

# Define the assistant's backup name, or what it might be heard as on accident
ASSISTANT_BACKUPNAME = ""

# Define the emotions the assistant can display
ASSISTANT_EMOTIONS = []

# Define the person's name
PERSON_NAME = ""

# Define how the person prefers to be addressed
PERSON_CALL = ""

# Define the operating system the person is using
OS = ""

# Define the person's hobbies
HOBBIES = []

# Define the name of the city the person lives in
CITY_NAME = ""

# Set the debug mode (False means debugging is off)
DEBUG = False

# Define the assistant's prompt message using the defined variables
ASSISTANT_PROMPT = (
    "You are " + ASSISTANT_NAME + ". You are an AI assistant to do whatever I say. "
    "Your emotions are " + ", ".join(ASSISTANT_EMOTIONS) + ". You are here to help me with my day. "
    "My name is " + PERSON_NAME + " and I go by " + PERSON_CALL + ". I am on a " + OS + " operating system. "
    "My hobbies are " + ", ".join(HOBBIES) + ". I live in " + CITY_NAME + ". The current time and date is " + formatted_datetime + 
    ", use this if I ask for the date or time and don't say according to my systems. Only use this info if I ask for it, for example, "
    "if I say hello don't use any of these things except for assistant name and person name. When addressing me either use " + PERSON_CALL +
    " or " + PERSON_NAME + " don't use both, I repeat never use both, also don't use them all the time I'll let you choose when to address me. "
    "Also never say nice to meet you because we already know each other. Make responses short and don't use too much of anything of the above, "
    "don't use too much emotions or slang, you are just here to help me, here is my prompt: "
)


# API KEYS ---------------------------------------------------------

# Weather API Key (OpenWeatherMap)
WEATHER_API_KEY = ""

# Youtube API Key (YoutubeApi)
YOUTUBE_API_KEY = ""
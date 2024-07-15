import os
import requests
import base64
import cv2
import time
from dotenv import load_dotenv
from config.config import *

# Load environment variables from a .env file
load_dotenv()

# Get API key from environment variables
api_key = os.getenv("OLLAMA_API_KEY")
base_url = OLLAMA_BASEURL

def capture_and_generate():
    # Initialize video capture
    cap = cv2.VideoCapture(0)

    # Display camera frame for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 2:
        ret, frame = cap.read()
        cv2.imshow('Camera Frame', frame)
        cv2.waitKey(1)  # Refresh display

    # Release video capture
    cap.release()
    cv2.destroyAllWindows()

    if frame is None or frame.size == 0:
        return "Failed to capture a valid frame from the webcam."

    # Adjust brightness (optional)
    frame = cv2.convertScaleAbs(frame, alpha=1.5, beta=10)

    # Encode captured image to base64
    _, buffer = cv2.imencode('.jpg', frame)
    encoded_image = base64.b64encode(buffer).decode('utf-8')

    # Prepare data for API request
    data = {
        "model": OLLAMA_MODEL_IMAGE,
        "prompt": "What is in this picture?",
        "stream": False,
        "images": [encoded_image]
    }

    # Make API request
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(f"{base_url}/api/generate", headers=headers, json=data)
    response_json = response.json()

    if response.status_code != 200 or response_json.get("status") == "failed":
        return "The generation failed."
    return response_json.get("response", "No response")



# Voice-Connect
# Voice Connect

**Voice Connect** is a multilingual communication application supporting 22 Indian languages, including Tamil, Telugu, Hindi, English, and Malayalam. It enables real-time cross-language voice and text interaction, breaking linguistic barriers across India.

---

## Features

- **Real-time Translation**: Caller speech is automatically translated into the recipient’s preferred language text.
- **Text-to-Speech**: Recipient’s typed messages are converted into speech for seamless communication.
- **Multilingual Support**: Supports 22 Indian languages.
- **Scalable Architecture**: Backend is containerized with Docker and deployed on Google Cloud.
- **User-Friendly**: Frontend built with Java and Android Studio for smooth, robust mobile experience.

---

## Project Structure

C:\VoiceConnect
│
├── frontend/ # Android Studio project
├── main.py # Main backend application
├── fastwapi.py # API integration
├── requirements.txt # Python dependencies
├── Dockerfile # Containerization
├── audio_samples/ # Example voice files
│ ├── caller_to_receiver.wav
│ ├── receiver_to_caller.wav
│ ├── input.wav
│ ├── output.wav
│ └── temp_output.wav
├── temp_output.mp3
└── output.mp3

yaml
Copy code

---

## Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/Gautghadi-1605/Voice-Connect.git
cd Voice-Connect
Create a virtual environment (Python backend)

bash
Copy code
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux
Install dependencies

bash
Copy code
pip install -r requirements.txt
Run the backend

bash
Copy code
python main.py
Run the Android frontend

Open the frontend folder in Android Studio.

Build and run on your device/emulator.

Notes
Secrets: Do not commit your Google Cloud API keys. Use environment variables to securely load credentials locally.

Audio Samples: Pre-recorded .wav files are included for testing purposes.

Tech Stack
Frontend: Java, Android Studio

Backend: Python (Flask/FastAPI)

APIs: Google Translate API, Google Cloud libraries

Deployment: Docker, Google Cloud

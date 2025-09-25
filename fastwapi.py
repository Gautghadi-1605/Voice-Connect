# fastwapi_ws.py
import io
import json
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from google.cloud import speech, translate_v2 as translate, texttospeech

# ------------------ Setup ------------------
speech_client = speech.SpeechClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

app = FastAPI(title="Indian Nagish Translation WebSocket API")

# ------------------ Root Endpoint for Browser ------------------
@app.get("/")
async def root():
    return {"message": "Indian Nagish Translation API is running!"}

# ------------------ Helper Functions ------------------
def speech_to_text(audio_bytes: bytes, language_code: str) -> str:
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = speech_client.recognize(config=config, audio=audio)
    if not response.results:
        return ""
    return response.results[0].alternatives[0].transcript

def translate_text(text: str, target_lang: str) -> str:
    result = translate_client.translate(text, target_language=target_lang)
    return result["translatedText"]

def text_to_speech_bytes(text: str, language_code: str) -> bytes:
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
    response = tts_client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    return response.audio_content

# ------------------ WebSocket Endpoint ------------------
@app.websocket("/ws/translate")
async def websocket_translate(websocket: WebSocket):
    await websocket.accept()
    await websocket.send_text("Connected to Indian Nagish WebSocket API")

    try:
        while True:
            # Receive JSON with audio bytes and language info
            message = await websocket.receive_bytes()
            
            # Expecting client to send JSON bytes
            data_json = json.loads(message.decode("utf-8"))
            caller_lang = data_json.get("caller_lang", "en-US")
            receiver_lang = data_json.get("receiver_lang", "ta-IN")
            audio_bytes = bytes(data_json.get("audio", ""), encoding="latin1")  # or base64 decode if needed

            # Process audio
            transcript = speech_to_text(audio_bytes, caller_lang)
            if transcript:
                translated_text = translate_text(transcript, receiver_lang)
                tts_bytes = text_to_speech_bytes(translated_text, receiver_lang)
                await websocket.send_bytes(tts_bytes)
            else:
                await websocket.send_text("No speech recognized")
    except WebSocketDisconnect:
        print("Client disconnected")

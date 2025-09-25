import os
import queue
import sounddevice as sd
import numpy as np
import io
import simpleaudio as sa
from google.cloud import speech, translate_v2 as translate, texttospeech

# ------------------ Setup ------------------
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/nagesh-backend/key.json"

speech_client = speech.SpeechClient()
translate_client = translate.Client()
tts_client = texttospeech.TextToSpeechClient()

# ------------------ Audio Parameters ------------------
RATE = 16000
CHANNELS = 1
CHUNK = int(RATE / 10)  # 100ms
q = queue.Queue()

# ------------------ Functions ------------------

def record_audio(duration=10, fs=RATE):
    """Records audio from the mic."""
    print(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=CHANNELS, dtype='int16')
    sd.wait()
    audio_bytes = recording.tobytes()
    print("Recording complete!")
    return audio_bytes

def speech_to_text(audio_bytes, language_code):
    """Convert audio bytes to text using Google Speech-to-Text."""
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True
    )
    try:
        response = speech_client.recognize(config=config, audio=audio)
        if not response.results:
            return ""
        transcript = response.results[0].alternatives[0].transcript
        return transcript
    except Exception as e:
        print(f"Speech-to-Text Error: {e}")
        return ""

def translate_text(text, target_lang):
    """Translate text to the target language."""
    try:
        result = translate_client.translate(text, target_language=target_lang)
        return result["translatedText"]
    except Exception as e:
        print(f"Translation Error: {e}")
        return text

def text_to_speech_file(text, language_code, filename="output.wav"):
    """Convert text to speech and save/play as WAV file."""
    try:
        synthesis_input = texttospeech.SynthesisInput(text=text)
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code,
            ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
        response = tts_client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

        # Save audio to file
        with open(filename, "wb") as out:
            out.write(response.audio_content)

        # Play WAV
        wave_obj = sa.WaveObject.from_wave_file(filename)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    except Exception as e:
        print(f"TTS Error: {e}")

# ------------------ Main ------------------

if __name__ == "__main__":
    print("=== Real-time Translation System ===")
    caller_lang = input("Enter caller language code (e.g., 'ta-IN', 'hi-IN', 'en-US'): ").strip()
    receiver_lang = input("Enter receiver language code (e.g., 'ta-IN', 'hi-IN', 'en-US'): ").strip()

    while True:
        print("\n--- Caller Speaking ---")
        audio_bytes = record_audio(duration=10)  # <-- 10 seconds recording
        transcript = speech_to_text(audio_bytes, language_code=caller_lang)
        if transcript:
            print(f"Caller said: {transcript}")
            translated = translate_text(transcript, target_lang=receiver_lang)
            print(f"Translated for Receiver: {translated}")
            text_to_speech_file(translated, language_code=receiver_lang, filename="caller_to_receiver.wav")
        else:
            print("No speech recognized.")

        print("\n--- Receiver Typing ---")
        receiver_text = input("Receiver types text: ").strip()
        if receiver_text:
            translated_for_caller = translate_text(receiver_text, target_lang=caller_lang)
            print(f"Translated for Caller: {translated_for_caller}")
            text_to_speech_file(translated_for_caller, language_code=caller_lang, filename="receiver_to_caller.wav")






import tempfile
import os

from backend.models.load_models import load_whisper
from backend.utils.audio_utils import preprocess_audio


def speech_to_text(audio_bytes: bytes) -> str:

    whisper_model = load_whisper()

    try:
        processed_audio = preprocess_audio(audio_bytes)
    except Exception as e:
        print("Audio preprocessing failed:", e)
        return ""

    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:

        temp_audio.write(processed_audio)
        temp_audio_path = temp_audio.name

    try:

        segments, info = whisper_model.transcribe(temp_audio_path, language="en")

        print("Running Whisper transcription...")
        print("Detected language:", info.language)

        text = ""

        for segment in segments:
            print("Segment:", segment.text)
            text += segment.text

        return text.strip()

    finally:
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
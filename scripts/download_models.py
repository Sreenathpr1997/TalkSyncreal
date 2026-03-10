from faster_whisper import WhisperModel
from transformers import pipeline

print("Downloading Whisper model...")
WhisperModel("base")

print("Downloading translation model...")
pipeline(
    "translation",
    model="facebook/nllb-200-distilled-600M"
)

print("Model download complete")
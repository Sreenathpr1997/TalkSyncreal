import torch
from faster_whisper import WhisperModel
from transformers import pipeline
from backend.config import WHISPER_MODEL_SIZE

_whisper_model = None
_translator = None


def load_whisper():
    global _whisper_model

    if _whisper_model is None:
        # Force CPU for EC2
        device = "cpu"

        # Use int8 for lower RAM usage
        compute_type = "int8"

        _whisper_model = WhisperModel(
            WHISPER_MODEL_SIZE,   # recommended: "tiny" or "base"
            device=device,
            compute_type=compute_type
        )

    return _whisper_model


def load_translator():
    global _translator

    if _translator is None:
        # Always run translator on CPU
        device = -1

        _translator = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M",
            device=device
        )

    return _translator
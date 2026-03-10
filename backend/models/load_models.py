from faster_whisper import WhisperModel
from transformers import pipeline
from backend.config import WHISPER_MODEL_SIZE

_whisper_model = None
_translator = None


def load_whisper():
    global _whisper_model

    if _whisper_model is None:
        _whisper_model = WhisperModel(
            WHISPER_MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    return _whisper_model


def load_translator():
    global _translator

    if _translator is None:
        _translator = pipeline(
            "translation",
            model="facebook/nllb-200-distilled-600M",
            device=-1
        )

    return _translator
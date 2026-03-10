from gtts import gTTS
import os
import uuid

OUTPUT_DIR = "generated_audio"

# create folder if not exists
os.makedirs(OUTPUT_DIR, exist_ok=True)


def text_to_audio(text: str, language: str) -> bytes:

    if not text:
        return b""

    # language mapping
    lang_map = {
        "hindi": "hi",
        "punjabi": "pa"
    }

    lang = lang_map.get(language, "hi")

    # unique filename
    filename = f"{language}_{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # generate speech
    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    # read bytes for websocket
    with open(filepath, "rb") as f:
        audio_bytes = f.read()

    print(f"TTS generated: {filepath}")

    return audio_bytes
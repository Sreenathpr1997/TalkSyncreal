from gtts import gTTS
import uuid
import os
import boto3

s3 = boto3.client("s3")

BUCKET_NAME = "talksync-audio-storage"

OUTPUT_DIR = "generated_audio"
os.makedirs(OUTPUT_DIR, exist_ok=True)


def text_to_audio(text: str, language: str) -> bytes:

    if not text:
        return b""

    lang_map = {
        "hindi": "hi",
        "punjabi": "pa"
    }

    lang = lang_map.get(language, "hi")

    filename = f"{language}_{uuid.uuid4()}.mp3"
    filepath = os.path.join(OUTPUT_DIR, filename)

    tts = gTTS(text=text, lang=lang)
    tts.save(filepath)

    # upload to S3
    s3.upload_file(filepath, BUCKET_NAME, filename)

    print(f"Uploaded to S3: {filename}")

    with open(filepath, "rb") as f:
        audio_bytes = f.read()

    return audio_bytes
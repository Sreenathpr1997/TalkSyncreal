import numpy as np
import soundfile as sf
import io


def preprocess_audio(audio_bytes):

    audio_np = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32)

    audio_np = audio_np / 32768.0

    buffer = io.BytesIO()

    sf.write(buffer, audio_np, 16000, format="WAV")

    return buffer.getvalue()
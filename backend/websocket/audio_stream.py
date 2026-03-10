from fastapi import APIRouter, WebSocket
from starlette.websockets import WebSocketDisconnect

from backend.services.speech_service import speech_to_text
from backend.services.translation_service import translate_text
from backend.services.tts_service import text_to_audio

router = APIRouter()

BUFFER_LIMIT = 25


async def safe_send_json(websocket, data):
    try:
        await websocket.send_json(data)
    except:
        print("WebSocket already closed (json)")


async def safe_send_bytes(websocket, data):
    try:
        await websocket.send_bytes(data)
    except:
        print("WebSocket already closed (audio)")


async def process_audio(websocket, audio_bytes):

    english_text = speech_to_text(audio_bytes)

    print("Running speech recognition...")
    print("English:", english_text)

    if not english_text.strip():
        return

    if len(english_text.split()) < 3:
        print("Skipping short fragment")
        return

    print("Running translation...")

    hindi_text = translate_text(english_text, "hindi")
    punjabi_text = translate_text(english_text, "punjabi")

    print("Hindi:", hindi_text)
    print("Punjabi:", punjabi_text)

    await safe_send_json(websocket, {
        "english": english_text,
        "hindi": hindi_text,
        "punjabi": punjabi_text
    })

    hindi_audio = text_to_audio(hindi_text, "hindi")
    await safe_send_bytes(websocket, hindi_audio)

    punjabi_audio = text_to_audio(punjabi_text, "punjabi")
    await safe_send_bytes(websocket, punjabi_audio)


@router.websocket("/stream")
async def audio_stream(websocket: WebSocket):

    await websocket.accept()
    print("Client connected")

    audio_buffer = []

    try:

        while True:

            chunk = await websocket.receive_bytes()

            print("audio chunk received", len(chunk))

            audio_buffer.append(chunk)

            if len(audio_buffer) < BUFFER_LIMIT:
                continue

            combined_audio = b''.join(audio_buffer)
            audio_buffer = []

            print("Incoming audio size:", len(combined_audio))

            await process_audio(websocket, combined_audio)

    except WebSocketDisconnect:

        print("Client disconnected")

    except Exception as e:

        print("Stream error:", e)

    finally:

        # process remaining audio safely
        if audio_buffer:

            print("Processing remaining buffered audio...")

            try:
                remaining_audio = b''.join(audio_buffer)
                await process_audio(websocket, remaining_audio)
            except:
                print("Socket already closed, skipping final send")
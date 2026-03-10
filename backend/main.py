from fastapi import FastAPI
from backend.websocket.audio_stream import router as websocket_router
from backend.api.health import router as health_router

app = FastAPI(title="TalkSync Real-Time Translator")

app.include_router(websocket_router)
app.include_router(health_router)
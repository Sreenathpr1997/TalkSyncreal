TalkSync Real-Time Translation System

Install dependencies

pip install -r requirements.txt

Download models

python scripts/download_models.py

Run backend

uvicorn backend.main:app --reload

WebSocket endpoint

ws://localhost:8000/stream
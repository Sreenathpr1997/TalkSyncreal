import os

AWS_BUCKET = os.getenv("AWS_BUCKET", "talksync-artifacts")
AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

MODEL_CACHE_DIR = os.getenv("MODEL_CACHE_DIR", "./model_cache")
OUTPUT_AUDIO_DIR = os.getenv("OUTPUT_AUDIO_DIR", "./outputs")

WHISPER_MODEL_SIZE = os.getenv("WHISPER_MODEL_SIZE", "tiny")

TARGET_LANGUAGE = os.getenv("TARGET_LANGUAGE", "hin_Deva")
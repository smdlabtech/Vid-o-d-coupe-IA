import os

MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", 500))
SUPPORTED_VIDEO_FORMATS = {
    "video/mp4": [".mp4"],
    "video/webm": [".webm"],
    "video/quicktime": [".mov"],
    "video/x-msvideo": [".avi"],
    "video/x-matroska": [".mkv"],
}
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE = os.getenv("LOG_FILE", "app.log")
LOG_ROTATION = os.getenv("LOG_ROTATION", "10 MB")
LOG_RETENTION = os.getenv("LOG_RETENTION", "7 days")
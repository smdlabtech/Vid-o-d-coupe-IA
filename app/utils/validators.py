import re
from typing import TypedDict, Optional
import reflex as rx
from app.utils.config import MAX_FILE_SIZE_MB, SUPPORTED_VIDEO_FORMATS


class FileValidationResult(TypedDict):
    is_valid: bool
    message: Optional[str]


def validate_video_file(file: rx.UploadFile) -> FileValidationResult:
    if file.content_type not in SUPPORTED_VIDEO_FORMATS:
        return {
            "is_valid": False,
            "message": f"Format de fichier non supporté: {file.content_type}. Essayez {', '.join(SUPPORTED_VIDEO_FORMATS.keys())}.",
        }
    max_size_bytes = MAX_FILE_SIZE_MB * 1024 * 1024
    if file.size > max_size_bytes:
        return {
            "is_valid": False,
            "message": f"Le fichier est trop volumineux ({file.size / (1024 * 1024):.2f}MB). La taille maximale est de {MAX_FILE_SIZE_MB} MB.",
        }
    return {"is_valid": True, "message": None}


def sanitize_filename(filename: str) -> str:
    sanitized = re.sub("[^a-zA-Z0-9._-]", "", filename)
    sanitized = re.sub("\\.\\.", "", sanitized)
    if not sanitized:
        return "unnamed_file"
    return sanitized
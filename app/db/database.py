import sqlite3
from datetime import datetime
import logging
from typing import TypedDict, cast

DATABASE_URL = "video_history.db"


class Video(TypedDict):
    id: int
    filename: str
    created_at: str
    duration: float | None
    status: str
    transcription_word_count: int | None
    error_message: str | None


def get_db_connection():
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    try:
        with get_db_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS video (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL UNIQUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    duration REAL,
                    status TEXT NOT NULL,
                    transcription_word_count INTEGER,
                    error_message TEXT
                );
            """)
            conn.commit()
    except Exception as e:
        logging.exception(f"Error initializing database: {e}")
        raise


def save_video_history(
    filename: str,
    status: str,
    duration: float | None = None,
    transcription_word_count: int | None = None,
    error_message: str | None = None,
):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM video WHERE filename = ?", (filename,))
            result = cursor.fetchone()
            if result:
                video_id = result["id"]
                cursor.execute(
                    """UPDATE video 
                       SET status = ?, duration = ?, transcription_word_count = ?, error_message = ?, created_at = ?
                       WHERE id = ?""",
                    (
                        status,
                        duration,
                        transcription_word_count,
                        error_message,
                        datetime.utcnow(),
                        video_id,
                    ),
                )
            else:
                cursor.execute(
                    """INSERT INTO video (filename, status, duration, transcription_word_count, error_message, created_at) 
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    (
                        filename,
                        status,
                        duration,
                        transcription_word_count,
                        error_message,
                        datetime.utcnow(),
                    ),
                )
            conn.commit()
    except Exception as e:
        logging.exception(f"Error saving video history for {filename}: {e}")


def get_all_videos() -> list[Video]:
    try:
        with get_db_connection() as conn:
            rows = conn.execute(
                "SELECT id, filename, created_at, duration, status, transcription_word_count, error_message FROM video ORDER BY created_at DESC"
            ).fetchall()
            videos = [
                {
                    "id": row["id"],
                    "filename": row["filename"],
                    "created_at": str(row["created_at"]),
                    "duration": row["duration"],
                    "status": row["status"],
                    "transcription_word_count": row["transcription_word_count"],
                    "error_message": row["error_message"],
                }
                for row in rows
            ]
            return cast(list[Video], videos)
    except Exception as e:
        logging.exception(f"Error fetching all videos: {e}")
        return []


def delete_video_by_id(video_id: int):
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM video WHERE id = ?", (video_id,))
            result = cursor.fetchone()
            if result:
                cursor.execute("DELETE FROM video WHERE id = ?", (video_id,))
                conn.commit()
            else:
                raise FileNotFoundError(f"Video with id {video_id} not found.")
    except Exception as e:
        logging.exception(f"Error deleting video id {video_id}: {e}")
        raise
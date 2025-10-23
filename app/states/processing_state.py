import reflex as rx
from typing import TypedDict
import os
from openai import OpenAI
import logging
import subprocess
import tempfile


class Segment(TypedDict):
    start: float
    end: float
    text: str


from app.state import AppState


class ProcessingState(rx.State):
    """State for handling the video processing and transcription."""

    is_processing: bool = False
    processing_step: str = ""
    progress: int = 0
    transcript: list[Segment] = []
    video_filename: str = ""
    selected_segments: list[int] = []
    is_clipping: bool = False
    generated_clips: list[str] = []

    @rx.event
    async def on_load(self):
        video_id = self.router.page.params.get("video_id", "")
        app_state = await self.get_state(AppState)
        app_state.set_active_page("Analyse de la Vid\x01o")
        if (
            video_id
            and (self.video_filename != video_id or not self.transcript)
            and (not self.is_processing)
        ):
            yield ProcessingState.process_video(video_id)

    @rx.event(background=True)
    async def process_video(self, video_filename: str):
        async with self:
            if self.is_processing and self.video_filename == video_filename:
                yield
                return
            self.is_processing = True
            self.transcript = []
            self.selected_segments = []
            self.generated_clips = []
            self.video_filename = video_filename
            self.processing_step = "Starting..."
            self.progress = 0
            yield
        audio_path_str = ""
        try:
            video_path = rx.get_upload_dir() / video_filename
            audio_path = rx.get_upload_dir() / f"{video_filename}.mp3"
            audio_path_str = str(audio_path)
            async with self:
                self.processing_step = "Extraction de l'audio..."
                self.progress = 10
            yield
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_filename}")
            try:
                subprocess.run(
                    [
                        "ffmpeg",
                        "-i",
                        str(video_path),
                        "-vn",
                        "-acodec",
                        "mp3",
                        "-ab",
                        "192k",
                        "-ar",
                        "22050",
                        "-f",
                        "mp3",
                        audio_path_str,
                        "-y",
                    ],
                    check=True,
                    capture_output=True,
                )
            except subprocess.CalledProcessError as e:
                logging.exception(f"FFmpeg error: {e}")
                raise Exception(f"Erreur lors de l'extraction audio: {e}")
            except FileNotFoundError:
                logging.exception("FFmpeg not found")
                raise Exception("FFmpeg n'est pas installé sur le système")
            async with self:
                self.processing_step = "Transcription avec Whisper..."
                self.progress = 40
            yield
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise Exception("Clé API OpenAI non configurée")
            client = OpenAI(api_key=api_key)
            with open(audio_path_str, "rb") as audio_file:
                response = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="verbose_json",
                    timestamp_granularities=["segment"],
                )
            transcript_data = response.segments
            async with self:
                self.processing_step = "Analyse des segments..."
                self.progress = 80
                processed_segments = []
                for seg in transcript_data:
                    processed_segments.append(
                        {
                            "start": seg["start"],
                            "end": seg["end"],
                            "text": seg["text"].strip(),
                        }
                    )
                self.transcript = processed_segments
                self.progress = 100
                self.processing_step = "Traitement terminé !"
                self.is_processing = False
            yield
        except Exception as e:
            logging.exception(f"Error processing video: {e}")
            async with self:
                self.processing_step = f"Erreur: {str(e)}"
                self.is_processing = False
            yield
        finally:
            if audio_path_str and os.path.exists(audio_path_str):
                try:
                    os.remove(audio_path_str)
                except Exception as e:
                    logging.exception(f"Error cleaning up audio file: {e}")

    @rx.event
    def toggle_segment_selection(self, index: int):
        if index in self.selected_segments:
            self.selected_segments.remove(index)
        else:
            self.selected_segments.append(index)
            self.selected_segments.sort()

    @rx.event
    def select_all_segments(self):
        self.selected_segments = list(range(len(self.transcript)))

    @rx.event
    def deselect_all_segments(self):
        self.selected_segments = []

    @rx.event(background=True)
    async def create_clips(self):
        async with self:
            if not self.selected_segments or self.is_clipping:
                return
            self.is_clipping = True
            self.generated_clips = []
        yield
        try:
            video_path = rx.get_upload_dir() / self.video_filename
            video_name_without_ext = os.path.splitext(self.video_filename)[0]
            for i, segment_index in enumerate(self.selected_segments):
                segment = self.transcript[segment_index]
                start_time = segment["start"]
                end_time = segment["end"]
                output_filename = f"{video_name_without_ext}_clip_{i + 1}.mp4"
                output_path = rx.get_upload_dir() / output_filename
                try:
                    subprocess.run(
                        [
                            "ffmpeg",
                            "-i",
                            str(video_path),
                            "-ss",
                            str(start_time),
                            "-to",
                            str(end_time),
                            "-c",
                            "copy",
                            str(output_path),
                            "-y",
                        ],
                        check=True,
                        capture_output=True,
                    )
                    async with self:
                        self.generated_clips.append(output_filename)
                    yield
                except subprocess.CalledProcessError as e:
                    logging.exception(
                        f"FFmpeg error creating clip {output_filename}: {e.stderr.decode()}"
                    )
                except FileNotFoundError:
                    logging.exception("FFmpeg not found")
                    async with self:
                        self.is_clipping = False
                    raise Exception("FFmpeg n'est pas installé sur le système")
            async with self:
                self.is_clipping = False
            yield
        except Exception as e:
            logging.exception(f"Error creating clips: {e}")
            async with self:
                self.is_clipping = False
            yield
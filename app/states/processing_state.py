import reflex as rx
from typing import TypedDict
import os
from openai import OpenAI
from app.utils.logger import get_logger, log_operation
import subprocess
import time

logger = get_logger("processing")


class Segment(TypedDict):
    start: float
    end: float
    text: str


from app.state import AppState
from app.db.database import save_video_history


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
        app_state.set_active_page("Analyse de la Vidéo")
        if (
            video_id
            and (self.video_filename != video_id or not self.transcript)
            and (not self.is_processing)
        ):
            logger.info(f"on_load triggered for video: {video_id}")
            yield ProcessingState.process_video(video_id)

    @rx.event(background=True)
    async def process_video(self, video_filename: str):
        start_time = time.time()
        async with self:
            if self.is_processing and self.video_filename == video_filename:
                logger.warning(
                    f"Processing for {video_filename} already in progress. Ignoring new request."
                )
                yield
                return
            logger.info(f"Starting video processing for: {video_filename}")
            self.is_processing = True
            self.transcript = []
            self.selected_segments = []
            self.generated_clips = []
            self.video_filename = video_filename
            self.processing_step = "Initialisation..."
            self.progress = 0
            yield
        audio_path_str = ""
        try:
            video_path = rx.get_upload_dir() / video_filename
            audio_filename = f"{os.path.splitext(video_filename)[0]}.mp3"
            audio_path = rx.get_upload_dir() / audio_filename
            audio_path_str = str(audio_path)
            async with self:
                self.processing_step = "Extraction de l'audio..."
                self.progress = 10
                logger.info(
                    f"Extracting audio from {video_filename} to {audio_filename}"
                )
            yield
            if not video_path.exists():
                raise FileNotFoundError(f"Video file not found: {video_filename}")
            self._run_ffmpeg_extract(video_path, audio_path_str)
            async with self:
                self.processing_step = "Transcription avec Whisper..."
                self.progress = 40
                logger.info(f"Starting transcription for {audio_filename}")
            yield
            response = self._run_whisper_transcription(audio_path_str)
            transcript_data = response.segments
            async with self:
                self.processing_step = "Analyse des segments..."
                self.progress = 80
                logger.info("Processing transcription segments.")
                processed_segments = [
                    {
                        "start": seg["start"],
                        "end": seg["end"],
                        "text": seg["text"].strip(),
                    }
                    for seg in transcript_data
                ]
                self.transcript = processed_segments
                self.progress = 100
                self.processing_step = "Traitement terminé !"
                self.is_processing = False
                duration = time.time() - start_time
                logger.info(
                    f"Processing for {video_filename} finished in {duration:.2f} seconds."
                )
                save_video_history(
                    filename=video_filename,
                    transcription_word_count=len(response.text.split()),
                    duration=response.duration,
                    status="terminé",
                )
            yield
        except Exception as e:
            logger.exception(f"Error processing video {video_filename}: {e}")
            save_video_history(
                filename=video_filename, status="erreur", error_message=str(e)
            )
            async with self:
                self.processing_step = f"Erreur: {str(e)}"
                self.is_processing = False
            yield
        finally:
            if audio_path_str and os.path.exists(audio_path_str):
                try:
                    os.remove(audio_path_str)
                    logger.info(f"Cleaned up temporary audio file: {audio_path_str}")
                except Exception as e:
                    logger.exception(
                        f"Error cleaning up audio file {audio_path_str}: {e}"
                    )

    def _run_ffmpeg_extract(self, video_path: str, audio_path: str):
        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-i",
                    video_path,
                    "-vn",
                    "-acodec",
                    "mp3",
                    "-ab",
                    "192k",
                    "-ar",
                    "22050",
                    "-f",
                    "mp3",
                    audio_path,
                    "-y",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
        except subprocess.CalledProcessError as e:
            logger.exception(f"FFmpeg error: {e.stderr}")
            raise Exception(f"Erreur FFmpeg: {e.stderr}")
        except FileNotFoundError as e:
            logger.exception("FFmpeg not found. It must be installed on the system.")
            raise Exception(
                "FFmpeg n'est pas install&#233; sur le syst&#232;me."
            ) from e

    def _run_whisper_transcription(self, audio_path: str):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise Exception("Clé API OpenAI (OPENAI_API_KEY) non configurée.")
        client = OpenAI(api_key=api_key)
        with open(audio_path, "rb") as audio_file:
            return client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=["segment"],
            )

    @rx.event
    def toggle_segment_selection(self, index: int):
        if index in self.selected_segments:
            self.selected_segments.remove(index)
        else:
            self.selected_segments.append(index)
            self.selected_segments.sort()
        return rx.toast.info(f"Segment {index + 1} s\x92lectionn\x92.")

    @rx.event
    def select_all_segments(self):
        self.selected_segments = list(range(len(self.transcript)))
        return rx.toast.info("Tous les segments ont \x92t\x92 s\x92lectionn\x92s.")

    @rx.event
    def deselect_all_segments(self):
        self.selected_segments = []
        return rx.toast.info("Tous les segments ont \x92t\x92 d\x92s\x92lectionn\x92s.")

    @rx.event(background=True)
    async def create_clips(self):
        async with self:
            if not self.selected_segments or self.is_clipping:
                if self.is_clipping:
                    yield rx.toast.warning(
                        "La cr\x92ation de clips est d\x92j\x88 en cours."
                    )
                else:
                    yield rx.toast.warning(
                        "Veuillez s\x92lectionner au moins un segment."
                    )
                return
            self.is_clipping = True
            self.generated_clips = []
            yield rx.toast.info("D\x92but de la cr\x92ation des clips...")
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
                    raise Exception("FFmpeg n'est pas install\x92 sur le syst\x88me")
            async with self:
                self.is_clipping = False
                yield rx.toast.success(
                    f"{len(self.generated_clips)} clips cr\x92\x92s avec succ\x98s !"
                )
            yield
        except Exception as e:
            logging.exception(f"Error creating clips: {e}")
            async with self:
                self.is_clipping = False
            yield rx.toast.error(f"Erreur lors de la cr\x82ation des clips: {e}")
            yield
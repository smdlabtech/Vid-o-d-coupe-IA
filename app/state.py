import reflex as rx
import asyncio
from typing import TypedDict, Optional


class NavItem(TypedDict):
    name: str
    icon: str
    page: str


class FileInfo(TypedDict):
    name: str
    size: int
    type: str


class AppState(rx.State):
    """The main application state."""

    active_page: str = "Accueil"
    nav_items: list[NavItem] = [
        {"name": "Accueil", "icon": "home", "page": "/"},
        {"name": "Upload", "icon": "upload", "page": "/upload"},
        {"name": "Mes Vidéos", "icon": "video", "page": "/videos"},
        {"name": "Paramètres", "icon": "settings", "page": "/settings"},
    ]
    upload_progress: int = 0
    is_uploading: bool = False
    uploaded_file_info: Optional[FileInfo] = None
    processing_status: str = "idle"
    feedback_message: str = ""

    @rx.var
    def uploaded_filename(self) -> str:
        if self.uploaded_file_info is None:
            return ""
        return self.uploaded_file_info["name"]

    @rx.var
    def formatted_file_size(self) -> str:
        if self.uploaded_file_info is None:
            return ""
        size_bytes = self.uploaded_file_info["size"]
        if size_bytes == 0:
            return "0B"
        size_name = ("B", "KB", "MB", "GB", "TB")
        import math

        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"

    @rx.event
    def set_active_page(self, page_name: str):
        self.active_page = page_name

    @rx.event
    async def handle_upload(self, files: list[rx.UploadFile]):
        self.is_uploading = True
        self.processing_status = "uploading"
        self.feedback_message = "Téléchargement en cours..."
        file = files[0]
        upload_dir = rx.get_upload_dir()
        upload_dir.mkdir(parents=True, exist_ok=True)
        file_path = upload_dir / file.name
        self.upload_progress = 0
        yield
        total_size = file.size or 0
        with file_path.open("wb") as f:
            bytes_written = 0
            while True:
                chunk = await file.read(1024 * 1024)
                if not chunk:
                    break
                f.write(chunk)
                bytes_written += len(chunk)
                if total_size > 0:
                    self.upload_progress = int(bytes_written / total_size * 100)
                    yield
        self.uploaded_file_info = {
            "name": file.name,
            "size": file.size,
            "type": file.content_type,
        }
        self.is_uploading = False
        self.processing_status = "completed"
        self.feedback_message = "Téléchargement terminé avec succès !"

    @rx.event
    async def start_processing(self):
        self.processing_status = "processing"
        self.feedback_message = "Initialisation du traitement..."
        if self.uploaded_file_info is None:
            self.processing_status = "error"
            self.feedback_message = "Aucun fichier à traiter."
            return
        return rx.redirect(f"/processing/{self.uploaded_filename}")

    @rx.event
    def clear_upload(self):
        self.uploaded_file_info = None
        self.upload_progress = 0
        self.processing_status = "idle"
        self.feedback_message = ""
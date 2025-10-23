import reflex as rx
from app.db.database import get_all_videos, delete_video_by_id, Video as VideoHistory
from app.utils.logger import get_logger
from typing import cast

logger = get_logger("videos_page")


class VideosState(rx.State):
    videos: list[VideoHistory] = []
    loading: bool = True
    search_query: str = ""
    status_filter: str = "Tous"

    @rx.event
    async def fetch_videos(self):
        self.loading = True
        yield
        try:
            logger.info("Fetching video history from database.")
            self.videos = get_all_videos()
            logger.info(f"Successfully fetched {len(self.videos)} video records.")
        except Exception as e:
            logger.exception(f"Error fetching video history: {e}")
            yield rx.toast.error("Erreur lors de la récupération de l'historique.")
        finally:
            self.loading = False
            yield

    @rx.event
    async def delete_video(self, video_id: int):
        logger.info(f"Attempting to delete video with id: {video_id}")
        try:
            delete_video_by_id(video_id)
            logger.info(f"Successfully deleted video with id: {video_id}")
            yield rx.toast.success("Vid&#233;o supprim&#233;e de l'historique.")
            yield VideosState.fetch_videos
        except FileNotFoundError as e:
            logger.exception(
                f"Attempted to delete non-existent video id {video_id}: {e}"
            )
            yield rx.toast.warning(e)
        except Exception as e:
            logger.exception(f"Error deleting video id {video_id}: {e}")
            yield rx.toast.error("Erreur lors de la suppression de la vid&#233;o.")

    @rx.var
    def filtered_videos(self) -> list[VideoHistory]:
        query = self.search_query.lower()
        status = self.status_filter

        @rx.event
        def is_match(video: VideoHistory) -> bool:
            matches_search = not query or query in video["filename"].lower()
            matches_status = status == "Tous" or video["status"] == status
            return matches_search and matches_status

        return cast(list[VideoHistory], [v for v in self.videos if is_match(v)])
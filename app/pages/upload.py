import reflex as rx
from app.state import AppState


def upload_page() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AppState.uploaded_file_info,
            rx.el.div(
                rx.el.h2(
                    "Vidéo Prête pour Traitement",
                    class_name="text-2xl font-bold text-gray-800 mb-6",
                ),
                rx.el.div(
                    rx.video(
                        url=rx.get_upload_url(AppState.uploaded_filename),
                        width="100%",
                        height="auto",
                        controls=True,
                        class_name="rounded-lg mb-4",
                    ),
                    rx.el.div(
                        rx.el.h3(
                            AppState.uploaded_file_info["name"],
                            class_name="font-semibold text-lg",
                        ),
                        rx.el.p(
                            f"{AppState.formatted_file_size} - {AppState.uploaded_file_info['type']}",
                            class_name="text-sm text-gray-500",
                        ),
                        class_name="mb-6",
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Relancer l'upload",
                            on_click=AppState.clear_upload,
                            class_name="bg-gray-200 text-gray-700 px-6 py-2 rounded-lg font-semibold hover:bg-gray-300 transition-colors",
                        ),
                        rx.el.button(
                            rx.icon("sparkles", class_name="mr-2"),
                            "Lancer le Traitement",
                            on_click=AppState.start_processing,
                            class_name="bg-orange-500 text-white px-6 py-2 rounded-lg font-semibold hover:bg-orange-600 transition-colors flex items-center",
                        ),
                        class_name="flex justify-between items-center",
                    ),
                    rx.cond(
                        AppState.processing_status == "processing",
                        rx.el.div(
                            rx.spinner(class_name="text-orange-500"),
                            rx.el.p(
                                AppState.feedback_message, class_name="text-orange-600"
                            ),
                            class_name="flex items-center gap-2 mt-4",
                        ),
                        None,
                    ),
                    class_name="bg-white p-8 rounded-2xl shadow-lg border border-gray-200 max-w-2xl mx-auto",
                ),
            ),
            rx.upload.root(
                rx.el.div(
                    rx.icon(
                        "cloud_upload",
                        class_name="w-16 h-16 text-gray-400 mx-auto mb-4",
                    ),
                    rx.el.h2(
                        "Glissez-d\x92posez votre vid\x92o ici",
                        class_name="text-xl font-semibold text-gray-700",
                    ),
                    rx.el.p("ou", class_name="text-gray-500 my-2"),
                    rx.el.button(
                        "S\x92lectionner un fichier",
                        class_name="bg-orange-500 text-white px-4 py-2 rounded-lg font-semibold hover:bg-orange-600 transition-colors",
                    ),
                    rx.el.p(
                        "MP4, MOV, AVI, MKV, WebM - Max 500MB",
                        class_name="text-xs text-gray-500 mt-4",
                    ),
                    rx.cond(
                        AppState.is_uploading,
                        rx.el.div(
                            rx.el.progress(
                                value=AppState.upload_progress,
                                max=100,
                                class_name="w-full mt-4",
                            ),
                            rx.el.p(
                                f"{AppState.feedback_message} {AppState.upload_progress}%",
                                class_name="text-sm text-orange-600 mt-2",
                            ),
                            class_name="w-full max-w-sm",
                        ),
                        None,
                    ),
                    class_name="flex flex-col items-center justify-center p-12 text-center",
                ),
                id="upload_area",
                border="2px dashed #ddd",
                border_radius="16px",
                padding="2rem",
                width="100%",
                max_width="800px",
                cursor="pointer",
                bg="white",
                on_drop=AppState.handle_upload(
                    rx.upload_files(upload_id="upload_area")
                ),
                on_mount=rx.clear_selected_files("upload_area"),
            ),
        ),
        class_name="flex flex-col items-center justify-center h-full",
    )
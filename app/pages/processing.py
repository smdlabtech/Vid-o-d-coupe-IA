import reflex as rx
from app.states.processing_state import ProcessingState


def segment_card(segment: dict, index: int) -> rx.Component:
    is_selected = ProcessingState.selected_segments.contains(index)
    return rx.el.div(
        rx.el.div(
            rx.el.input(
                type="checkbox",
                checked=is_selected,
                on_change=lambda _: ProcessingState.toggle_segment_selection(index),
                class_name="h-5 w-5 rounded border-gray-300 text-orange-600 focus:ring-orange-500 cursor-pointer",
            ),
            class_name="mr-4 pt-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    f"{segment['start']:.2f}s",
                    class_name="font-mono text-sm text-orange-600 bg-orange-100 px-2 py-1 rounded",
                ),
                rx.icon("arrow-right", class_name="text-gray-400 h-4 w-4"),
                rx.el.span(
                    f"{segment['end']:.2f}s",
                    class_name="font-mono text-sm text-orange-600 bg-orange-100 px-2 py-1 rounded",
                ),
                class_name="flex items-center gap-2 mb-2",
            ),
            rx.el.p(segment["text"], class_name="text-gray-700"),
            class_name="flex-1",
        ),
        class_name=rx.cond(
            is_selected,
            "bg-orange-50 p-4 rounded-lg border border-orange-200 flex items-start gap-4 shadow-sm",
            "bg-white p-4 rounded-lg border border-gray-200 flex items-start gap-4",
        ),
    )


def processing_page() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Analyse de la Vidéo", class_name="text-3xl font-bold text-gray-800 mb-2"
        ),
        rx.el.p(ProcessingState.video_filename, class_name="text-gray-500 mb-8"),
        rx.cond(
            ProcessingState.is_processing,
            rx.el.div(
                rx.spinner(class_name="w-12 h-12 text-orange-500"),
                rx.el.p(
                    ProcessingState.processing_step,
                    class_name="text-lg text-gray-600 mt-4",
                ),
                rx.el.div(
                    rx.el.div(
                        class_name="bg-orange-500 h-2 rounded-full transition-all duration-300",
                        style={"width": f"{ProcessingState.progress.to_string()}%"},
                    ),
                    class_name="w-full bg-gray-200 rounded-full h-2 mt-4 max-w-md",
                ),
                class_name="flex flex-col items-center justify-center text-center p-12 bg-white rounded-2xl shadow-sm border",
            ),
            rx.cond(
                ProcessingState.transcript.length() > 0,
                rx.el.div(
                    rx.el.div(
                        rx.video(
                            url=rx.get_upload_url(ProcessingState.video_filename),
                            width="100%",
                            height="auto",
                            controls=True,
                            class_name="rounded-lg aspect-video",
                        ),
                        class_name="w-full lg:w-2/3 mb-8 lg:mb-0",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Transcription & Segments",
                                class_name="text-xl font-bold text-gray-800",
                            ),
                            rx.el.div(
                                rx.el.button(
                                    "Tout sélectionner",
                                    on_click=ProcessingState.select_all_segments,
                                    class_name="text-xs font-semibold text-orange-600 hover:text-orange-800",
                                    variant="ghost",
                                ),
                                rx.el.button(
                                    "Tout désélectionner",
                                    on_click=ProcessingState.deselect_all_segments,
                                    class_name="text-xs font-semibold text-gray-500 hover:text-gray-700",
                                    variant="ghost",
                                ),
                                class_name="flex gap-2",
                            ),
                            class_name="flex justify-between items-center mb-4",
                        ),
                        rx.el.div(
                            rx.foreach(ProcessingState.transcript, segment_card),
                            class_name="space-y-3 h-[400px] overflow-y-auto pr-2",
                        ),
                        rx.el.button(
                            "Générer les Clips",
                            rx.icon("scissors"),
                            on_click=ProcessingState.create_clips,
                            is_loading=ProcessingState.is_clipping,
                            disabled=ProcessingState.selected_segments.length() == 0,
                            class_name="w-full mt-4 bg-orange-500 text-white py-3 rounded-lg font-semibold hover:bg-orange-600 transition-colors flex items-center justify-center gap-2 disabled:bg-gray-300 disabled:cursor-not-allowed",
                        ),
                        rx.cond(
                            ProcessingState.generated_clips.length() > 0,
                            rx.el.div(
                                rx.el.h4(
                                    "Clips Générés",
                                    class_name="font-semibold text-gray-800 mt-6 mb-2",
                                ),
                                rx.foreach(
                                    ProcessingState.generated_clips,
                                    lambda clip: rx.el.div(
                                        rx.el.a(
                                            rx.icon(
                                                "download", class_name="mr-2 h-4 w-4"
                                            ),
                                            clip,
                                            href=rx.get_upload_url(clip),
                                            download=True,
                                            class_name="flex items-center text-sm text-blue-600 hover:underline",
                                        ),
                                        class_name="bg-gray-100 p-2 rounded-md",
                                    ),
                                ),
                                class_name="space-y-2 mt-4",
                            ),
                        ),
                        class_name="w-full lg:w-1/3",
                    ),
                    class_name="flex flex-col lg:flex-row gap-8",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "flag_triangle_right",
                            class_name="w-16 h-16 text-red-400 mb-4",
                        ),
                        rx.el.h3(
                            "Erreur de Traitement",
                            class_name="text-xl font-bold text-gray-800 mb-2",
                        ),
                        rx.el.p(
                            "Le traitement de la vid\x92o a \x92chou\x92. Raison de l'erreur:",
                            class_name="text-gray-600",
                        ),
                        rx.el.code(
                            ProcessingState.processing_step,
                            class_name="mt-2 text-sm text-red-600 bg-red-50 p-2 rounded-md font-mono",
                        ),
                        rx.el.a(
                            rx.el.button(
                                "R\x92essayer avec une autre vid\x92o",
                                on_click=lambda: rx.redirect("/upload"),
                                class_name="mt-6 bg-orange-500 text-white px-6 py-2 rounded-lg font-semibold hover:bg-orange-600 transition-colors",
                            )
                        ),
                        class_name="flex flex-col items-center justify-center text-center p-12",
                    ),
                    class_name="bg-white rounded-2xl shadow-sm border border-red-200",
                ),
            ),
        ),
        class_name="w-full",
    )
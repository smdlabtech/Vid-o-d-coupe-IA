import reflex as rx
from app.states.videos_state import VideosState


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        status,
        class_name=rx.cond(
            status == "terminé",
            "bg-green-100 text-green-800 text-xs font-medium px-2.5 py-1 rounded-full",
            rx.cond(
                status == "en_cours",
                "bg-yellow-100 text-yellow-800 text-xs font-medium px-2.5 py-1 rounded-full",
                "bg-red-100 text-red-800 text-xs font-medium px-2.5 py-1 rounded-full",
            ),
        ),
    )


def videos_table() -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(
                        "Nom du Fichier",
                        scope="col",
                        class_name="py-3 px-6 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Date",
                        scope="col",
                        class_name="py-3 px-6 text-left text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Durée",
                        scope="col",
                        class_name="py-3 px-6 text-center text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Clips",
                        scope="col",
                        class_name="py-3 px-6 text-center text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Statut",
                        scope="col",
                        class_name="py-3 px-6 text-center text-sm font-semibold text-gray-600",
                    ),
                    rx.el.th(
                        "Actions",
                        scope="col",
                        class_name="py-3 px-6 text-center text-sm font-semibold text-gray-600",
                    ),
                    class_name="bg-gray-50",
                )
            ),
            rx.el.tbody(
                rx.foreach(
                    VideosState.filtered_videos,
                    lambda video: rx.el.tr(
                        rx.el.td(
                            rx.el.span(
                                video["filename"],
                                class_name="font-medium text-gray-800",
                                title=video["filename"],
                            ),
                            class_name="py-4 px-6 whitespace-nowrap",
                        ),
                        rx.el.td(
                            video["created_at"].to_string(),
                            class_name="py-4 px-6 text-gray-600 text-sm whitespace-nowrap",
                        ),
                        rx.el.td(
                            f"{rx.cond(video['duration'], video['duration'].to(float).to_string() + 's', 'N/A')}",
                            class_name="py-4 px-6 text-gray-600 text-center whitespace-nowrap",
                        ),
                        rx.el.td(
                            "0",
                            class_name="py-4 px-6 text-center font-medium text-gray-800",
                        ),
                        rx.el.td(
                            status_badge(video["status"]),
                            class_name="py-4 px-6 text-center",
                        ),
                        rx.el.td(
                            rx.el.div(
                                rx.el.a(
                                    rx.el.button(
                                        rx.icon("search", class_name="h-4 w-4 mr-1"),
                                        "Détails",
                                        class_name="text-blue-600 hover:text-blue-800 flex items-center gap-1 text-sm font-medium",
                                        variant="ghost",
                                    ),
                                    href=f"/processing/{video['id']}",
                                ),
                                rx.el.button(
                                    rx.icon("trash-2", class_name="h-4 w-4 mr-1"),
                                    "Supprimer",
                                    on_click=lambda: VideosState.delete_video(
                                        video["id"]
                                    ),
                                    class_name="text-red-600 hover:text-red-800 flex items-center gap-1 text-sm font-medium",
                                    variant="ghost",
                                ),
                                class_name="flex justify-center items-center gap-4",
                            ),
                            class_name="py-4 px-6 whitespace-nowrap",
                        ),
                        class_name="border-b border-gray-200 hover:bg-gray-50/50 transition-colors",
                    ),
                )
            ),
            class_name="min-w-full bg-white divide-y divide-gray-200",
        ),
        class_name="overflow-x-auto border border-gray-200 rounded-xl shadow-sm",
    )


def no_videos_placeholder() -> rx.Component:
    return rx.el.div(
        rx.icon("video_off", class_name="w-16 h-16 text-gray-300 mb-4"),
        rx.el.h3("Aucune vidéo trouvée", class_name="text-xl font-bold text-gray-700"),
        rx.el.p(
            "Commencez par uploader une vidéo pour la voir ici.",
            class_name="text-gray-500 mt-2",
        ),
        rx.el.a(
            rx.el.button(
                "Uploader une vidéo",
                rx.icon("upload", class_name="ml-2 h-4 w-4"),
                class_name="mt-6 bg-orange-500 text-white px-5 py-2.5 rounded-lg font-semibold hover:bg-orange-600 transition-colors flex items-center",
            ),
            href="/upload",
        ),
        class_name="flex flex-col items-center justify-center text-center p-12 bg-white rounded-xl shadow-sm border",
    )


def videos_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.input(
                    placeholder="Rechercher par nom de fichier...",
                    on_change=VideosState.set_search_query,
                    class_name="w-full max-w-xs border-gray-300 rounded-lg pl-10 pr-4 py-2 focus:outline-none focus:ring-2 focus:ring-orange-500",
                    default_value=VideosState.search_query,
                ),
                rx.icon(
                    "search",
                    class_name="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-gray-400",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.span("Statut:", class_name="text-gray-600 font-medium text-sm"),
                rx.el.select(
                    ["Tous", "terminé", "en_cours", "erreur"],
                    default_value="Tous",
                    on_change=VideosState.set_status_filter,
                    class_name="border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-orange-500",
                ),
                class_name="flex items-center gap-3",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            VideosState.loading,
            rx.el.div(
                rx.spinner(class_name="w-8 h-8 text-orange-500"),
                rx.el.p(
                    "Chargement de l'historique...", class_name="mt-2 text-gray-500"
                ),
                class_name="flex flex-col items-center justify-center p-12 bg-white rounded-xl shadow-sm border",
            ),
            rx.cond(
                VideosState.filtered_videos.length() > 0,
                videos_table(),
                no_videos_placeholder(),
            ),
        ),
        on_mount=VideosState.fetch_videos,
        class_name="w-full",
    )
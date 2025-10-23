import reflex as rx
from app.state import AppState
from app.states.processing_state import ProcessingState
from app.components.sidebar import sidebar
from app.components.header import header
from app.pages.home import home_page
from app.pages.upload import upload_page
from app.pages.placeholder import placeholder_page
from app.pages.processing import processing_page


def layout(page_content: rx.Component) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            header(),
            rx.el.div(page_content, class_name="p-4 md:p-8"),
            class_name="flex-1 overflow-y-auto",
        ),
        class_name="flex h-screen bg-gray-50 font-['Inter']",
    )


def index() -> rx.Component:
    return layout(home_page())


def upload() -> rx.Component:
    return layout(upload_page())


def processing() -> rx.Component:
    return layout(processing_page())


def videos() -> rx.Component:
    return layout(placeholder_page("Mes Vidéos"))


def settings() -> rx.Component:
    return layout(placeholder_page("Paramètres"))


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=lambda: AppState.set_active_page("Accueil"))
app.add_page(
    upload, route="/upload", on_load=lambda: AppState.set_active_page("Upload")
)
app.add_page(
    processing, route="/processing/[video_id]", on_load=ProcessingState.on_load
)
app.add_page(
    videos, route="/videos", on_load=lambda: AppState.set_active_page("Mes Vidéos")
)
app.add_page(
    settings, route="/settings", on_load=lambda: AppState.set_active_page("Paramètres")
)
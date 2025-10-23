import reflex as rx
from app.state import AppState


def header() -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.h1(
                AppState.active_page, class_name="text-2xl font-bold text-gray-800"
            ),
            class_name="flex items-center justify-between",
        ),
        class_name="bg-white/80 backdrop-blur-sm sticky top-0 z-10 p-4 border-b border-gray-200",
    )
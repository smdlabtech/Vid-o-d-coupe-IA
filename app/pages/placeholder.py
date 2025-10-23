import reflex as rx


def placeholder_page(title: str) -> rx.Component:
    return rx.el.div(
        rx.icon("construction", class_name="w-24 h-24 text-gray-300 mb-4"),
        rx.el.h2(f"Page {title}", class_name="text-3xl font-bold text-gray-800"),
        rx.el.p(
            "Cette page est en cours de construction.", class_name="text-gray-500 mt-2"
        ),
        class_name="flex flex-col items-center justify-center h-full text-center",
    )
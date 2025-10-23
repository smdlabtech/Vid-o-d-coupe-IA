import reflex as rx
from app.state import AppState


def nav_item(item: dict) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(
                item["icon"],
                class_name=rx.cond(
                    AppState.active_page == item["name"],
                    "text-orange-500",
                    "text-gray-500 group-hover:text-orange-500",
                ),
            ),
            rx.el.span(
                item["name"],
                class_name=rx.cond(
                    AppState.active_page == item["name"],
                    "font-semibold text-gray-800",
                    "text-gray-700 group-hover:text-gray-800",
                ),
            ),
            class_name="flex items-center gap-3 p-3 rounded-lg transition-colors duration-200",
        ),
        href=item["page"],
        on_click=lambda: AppState.set_active_page(item["name"]),
        class_name=rx.cond(
            AppState.active_page == item["name"],
            "block w-full bg-orange-100/50 rounded-lg group",
            "block w-full hover:bg-gray-100/50 rounded-lg group",
        ),
    )


def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("clapperboard", class_name="h-8 w-8 text-orange-500"),
                rx.el.span(
                    "SmartClip-AI", class_name="text-xl font-bold text-gray-800"
                ),
                class_name="flex items-center gap-3 px-4 h-16 border-b border-gray-200",
            ),
            rx.el.nav(
                rx.foreach(AppState.nav_items, nav_item),
                class_name="flex-1 p-4 space-y-2 font-medium",
            ),
            rx.el.div(
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/initials/svg?seed=User",
                        class_name="size-10 rounded-full",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Utilisateur",
                            class_name="font-semibold text-sm text-gray-800",
                        ),
                        rx.el.p("user@example.com", class_name="text-xs text-gray-500"),
                        class_name="flex-1",
                    ),
                    rx.icon("fold_vertical", class_name="text-gray-500"),
                    class_name="flex items-center gap-3",
                ),
                class_name="p-4 border-t border-gray-200",
            ),
            class_name="flex flex-col h-full",
        ),
        class_name="hidden md:flex flex-col w-64 bg-white border-r border-gray-200 shadow-md",
    )
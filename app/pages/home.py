import reflex as rx


def feature_card(icon: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.icon(icon, class_name="w-10 h-10 text-orange-500 mb-4"),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-600"),
        class_name="bg-white p-6 rounded-2xl border border-gray-100 shadow-sm hover:shadow-lg transition-shadow duration-300",
    )


def step_item(number: str, title: str, description: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(number, class_name="text-lg font-bold text-orange-500"),
            class_name="flex items-center justify-center w-12 h-12 bg-orange-100 rounded-full border-2 border-orange-200 mb-4",
        ),
        rx.el.h3(title, class_name="text-lg font-semibold text-gray-800 mb-2"),
        rx.el.p(description, class_name="text-sm text-gray-600"),
        class_name="flex flex-col items-center text-center",
    )


def home_page() -> rx.Component:
    return rx.el.div(
        rx.el.section(
            rx.el.h2(
                "Découpez vos vidéos intelligemment avec l'IA",
                class_name="text-4xl md:text-5xl font-extrabold text-gray-800 mb-4 text-center",
            ),
            rx.el.p(
                "Gagnez du temps et créez des clips parfaits en un clic. Laissez SmartClip-AI analyser et extraire les meilleurs moments pour vous.",
                class_name="text-lg text-gray-600 max-w-3xl mx-auto text-center mb-8",
            ),
            rx.el.a(
                rx.el.button(
                    "Commencer l'upload",
                    rx.icon("arrow-right", class_name="ml-2"),
                    class_name="bg-orange-500 text-white px-8 py-3 rounded-xl font-semibold hover:bg-orange-600 transition-colors shadow-md hover:shadow-lg transform hover:-translate-y-1 duration-300",
                ),
                href="/upload",
            ),
            class_name="flex flex-col items-center justify-center py-20 px-4",
        ),
        rx.el.section(
            rx.el.h2(
                "Fonctionnalités Clés",
                class_name="text-3xl font-bold text-gray-800 text-center mb-12",
            ),
            rx.el.div(
                feature_card(
                    "cloud_upload",
                    "Upload Facile",
                    "Importez vos vidéos rapidement via un simple glisser-déposer.",
                ),
                feature_card(
                    "brain-circuit",
                    "Transcription IA",
                    "Obtenez une transcription précise de votre audio grâce à la puissance de Whisper.",
                ),
                feature_card(
                    "scissors",
                    "Découpage Intelligent",
                    "Notre IA détecte les silences et les hésitations pour proposer des coupes parfaites.",
                ),
                feature_card(
                    "download",
                    "Export Rapide",
                    "Téléchargez vos clips segmentés en haute qualité, prêts à être partagés.",
                ),
                class_name="grid md:grid-cols-2 lg:grid-cols-4 gap-8 max-w-7xl mx-auto",
            ),
            class_name="py-16 bg-gray-50 px-4",
        ),
        rx.el.section(
            rx.el.h2(
                "Comment ça marche ?",
                class_name="text-3xl font-bold text-gray-800 text-center mb-16",
            ),
            rx.el.div(
                step_item(
                    "1",
                    "Uploadez votre vidéo",
                    "Sélectionnez un fichier vidéo depuis votre ordinateur.",
                ),
                rx.el.div(class_name="flex-1 h-px bg-gray-200 hidden lg:block"),
                step_item(
                    "2",
                    "Analyse par l'IA",
                    "Notre système transcrit l'audio et détecte les silences.",
                ),
                rx.el.div(class_name="flex-1 h-px bg-gray-200 hidden lg:block"),
                step_item(
                    "3",
                    "Téléchargez les clips",
                    "Récupérez les segments vidéo pertinents, prêts à l'emploi.",
                ),
                class_name="flex flex-col lg:flex-row items-center justify-center gap-8 lg:gap-16 max-w-5xl mx-auto",
            ),
            class_name="py-20 px-4",
        ),
    )
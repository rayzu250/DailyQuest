# themes.rpy
default themes = {
    "bosque": {"bg": "#2E7D32", "accent": "#81C784", "text": "#FFFFFF"},
    "océano": {"bg": "#0277BD", "accent": "#4FC3F7", "text": "#FFFFFF"},
    "atardecer": {"bg": "#E65100", "accent": "#FFB74D", "text": "#FFFFFF"},
    "noche": {"bg": "#212121", "accent": "#90CAF9", "text": "#FFFFFF"},
}

init python:
    def get_theme_bg():
        return Solid(themes[current_theme]["bg"])

    def get_theme_accent():
        return themes[current_theme]["accent"]

label change_theme:
    menu:
        "Bosque (verde)":
            $ current_theme = "bosque"
        "Océano (azul)":
            $ current_theme = "océano"
        "Atardecer (naranja)":
            $ current_theme = "atardecer"
        "Noche (oscuro)":
            $ current_theme = "noche"
        "Volver":
            jump main_menu_todo
    e "¡Tema cambiado! Tu mundo se ve diferente ahora."
    jump main_menu_todo
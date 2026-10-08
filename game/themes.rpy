# themes.rpy
default themes = {
    "bosque": {"bg": "#2E7D32", "accent": "#81C784", "text": "#FFFFFF"},
    "océano": {"bg": "#0277BD", "accent": "#4FC3F7", "text": "#FFFFFF"},
    "atardecer": {"bg": "#E65100", "accent": "#FFB74D", "text": "#FFFFFF"},
    "noche": {"bg": "#212121", "accent": "#90CAF9", "text": "#FFFFFF"},
    "prehistoria": {"bg": "#53662C", "accent": "#D5DA85", "text": "#FFFFFF"},
    "jardín": {"bg": "#326548", "accent": "#ADE5A0", "text": "#FFFFFF"},
    "robots": {"bg": "#245566", "accent": "#7DE3DF", "text": "#FFFFFF"},
}

init -2 python:
    # Los recursos visuales no se guardan dentro del documento de tareas.
    QUEST_THEME_ART = {
        "bosque": {"folder": "forest", "overlay": "#12352188", "panel": "#17352DF2", "guide": None,
            "crop": (16, 95, 2140, 532), "selection": "#C4E99A"},
        "océano": {"folder": "ocean", "overlay": "#032D4666", "panel": "#083D52F2", "guide": "shark.png",
            "crop": (0, 106, 2172, 512), "selection": "#FFE5A0"},
        "atardecer": {"folder": "sunset", "overlay": "#35203B88", "panel": "#442D40F2", "guide": "guide.png",
            "crop": (10, 97, 2153, 510), "selection": "#FFD090"},
        "noche": {"folder": "night", "overlay": "#12163233", "panel": "#202544F2", "guide": "guide.png",
            "crop": (8, 76, 2156, 548), "selection": "#B2E9F5"},
        "prehistoria": {"folder": "prehistoric", "overlay": "#26381577", "panel": "#303D24F2", "guide": "guide.png",
            "crop": (20, 98, 2133, 510), "selection": "#D5DA85", "label": "Prehistórico"},
        "jardín": {"folder": "garden", "overlay": "#153D2877", "panel": "#234532F2", "guide": "guide.png",
            "crop": (16, 117, 2139, 474), "selection": "#ADE5A0"},
        "robots": {"folder": "robots", "overlay": "#12323F77", "panel": "#213E4CF2", "guide": "guide.png",
            "crop": (23, 99, 2123, 496), "selection": "#7DE3DF"},
        "mecha": {"folder": "mecha", "stage": "secundaria", "label": "Escuadrón Mecha",
            "overlay": "#081B3377", "panel": "#10243BF2", "guide": "guide.png",
            "crop": (100, 141, 1973, 443), "selection": "#9BDEEA"},
        "arcane": {"folder": "arcane", "stage": "secundaria", "label": "Academia Arcana",
            "overlay": "#20152F77", "panel": "#281F3CF2", "guide": "guide.png",
            "crop": (50, 157, 2073, 410), "selection": "#D7C5F4"},
        "stage": {"folder": "stage", "stage": "secundaria", "label": "Camino al Escenario",
            "overlay": "#101B3577", "panel": "#17233BF2", "guide": "guide.png",
            "crop": (67, 156, 2040, 407), "selection": "#B6E9DD"},
    }

    def quest_theme_key():
        name = getattr(store, "current_theme", "bosque")
        return name if name in QUEST_THEME_ART else "bosque"

    def quest_ocean_theme():
        return quest_theme_key() == "océano"

    def quest_theme_label(name):
        return QUEST_THEME_ART[name].get("label", name.capitalize())

    def quest_reward_image(reward_token, world=None):
        # El campo histórico «fruit» conserva la recompensa sin duplicarla ni migrarla.
        key = world if world in QUEST_THEME_ART else quest_theme_key()
        return "images/themes/%s/reward.png" % QUEST_THEME_ART[key]["folder"]

    def get_theme_bg():
        return QUEST_THEME_BACKGROUNDS[quest_theme_key()]

    def get_theme_panel():
        return Solid(QUEST_THEME_ART[quest_theme_key()]["panel"])

    def get_theme_options_bg():
        return get_theme_bg()

    def get_theme_button(state="idle"):
        return QUEST_THEME_BUTTONS[quest_theme_key()][state]

    def quest_button_surface(st, at, state="idle", family="todo"):
        return get_theme_button(state), None

    # Se recorta solo el margen transparente en tiempo de renderizado.
    # Frame conserva las esquinas al adaptar el botón a cada texto.
    QUEST_THEME_BUTTONS = {}
    QUEST_THEME_BACKGROUNDS = {}
    for _name, _art in QUEST_THEME_ART.items():
        _folder = "images/themes/%s/" % _art["folder"]
        _button = Frame(Transform(Crop(_art["crop"], _folder + "button.png"),
            xysize=(384, 96)), 44, 24)
        QUEST_THEME_BUTTONS[_name] = {
            "idle": _button,
            "hover": Transform(_button, matrixcolor=BrightnessMatrix(0.10)),
            "selected": Transform(_button, matrixcolor=TintMatrix(_art["selection"])),
            "selected_hover": Transform(_button, matrixcolor=TintMatrix(_art["selection"]) * BrightnessMatrix(0.08)),
            "insensitive": Transform(_button, matrixcolor=SaturationMatrix(0.0) * BrightnessMatrix(-0.12)),
        }
        QUEST_THEME_BACKGROUNDS[_name] = Composite((1080, 1920),
            (0, 0), Transform(_folder + "background.png", xysize=(1080, 1920)),
            (0, 0), Solid(_art["overlay"], xysize=(1080, 1920)))

    def get_theme_accent():
        return themes[quest_theme_key()]["accent"]

label change_theme:
    show screen theme_screen
    jump main_menu_todo

# Las preferencias son independientes de las tareas y de la etapa escolar.
default persistent.school_stage = "primaria"
default persistent.quest_motion = "normal"
default persistent.quest_guide_enabled = True

init -2 python:
    # Solo se ofrecen etapas con una experiencia implementada.
    QUEST_SCHOOL_PROFILES = {
        "primaria": {
            "label": "Primaria", "ages": "6 a 12 años",
            "help": "Elige una tarea. Si parece grande, divídela en pasos pequeños.",
            "features": ("steps", "guide", "rewards"),
        },
    }

    def quest_profile():
        return QUEST_SCHOOL_PROFILES.get(persistent.school_stage, QUEST_SCHOOL_PROFILES["primaria"])

    def quest_setting(name, value):
        if name == "school_stage" and value not in QUEST_SCHOOL_PROFILES:
            return
        if name == "quest_motion" and value not in ("normal", "reduced", "off"):
            return
        if name not in ("school_stage", "quest_motion", "quest_guide_enabled", "page_flip_enabled"):
            return
        setattr(persistent, name, value)
        if name == "quest_motion":
            renpy.run(Preference("transitions", "none" if value == "off" else "all"))
        renpy.save_persistent()
        renpy.restart_interaction()

    def close_quest_options():
        renpy.save_persistent()
        renpy.hide_screen("quest_options")
        renpy.restart_interaction()

    def open_quest_options():
        renpy.run(DisableAllInputValues())
        renpy.hide_screen("navigation_drawer")
        # La página y sus borradores permanecen debajo del panel de opciones.
        renpy.show_screen("quest_options")
        renpy.restart_interaction()

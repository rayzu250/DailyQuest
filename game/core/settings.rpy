# Las preferencias son independientes de las tareas y de la etapa escolar.
default persistent.school_stage = "primaria"
default persistent.quest_motion = "normal"
default persistent.quest_guide_enabled = True
default stage_themes = {}

init -2 python:
    # Solo se ofrecen etapas con una experiencia implementada.
    QUEST_SCHOOL_PROFILES = {
        "primaria": {
            "label": "Primaria", "ages": "6 a 12 años",
            "help": "Elige una tarea. Si parece grande, divídela en pasos pequeños.",
            "features": ("steps", "guide", "rewards"),
        },
        "secundaria": {
            "label": "Secundaria", "ages": "12 a 15 años",
            "help": "Define tu objetivo, prepara los pasos e inicia una misión. Puedes pausarla cuando lo necesites.",
            "features": ("steps", "guide", "rewards", "expeditions"),
        },
    }

    def quest_profile():
        return QUEST_SCHOOL_PROFILES.get(persistent.school_stage, QUEST_SCHOOL_PROFILES["primaria"])

    def quest_secondary():
        return persistent.school_stage == "secundaria"

    def quest_stage_themes(stage=None):
        stage = stage or persistent.school_stage
        return tuple(name for name, art in QUEST_THEME_ART.items()
            if art.get("stage", "primaria") == stage)

    def quest_normalize_stage_theme():
        if persistent.school_stage not in QUEST_SCHOOL_PROFILES:
            persistent.school_stage = "primaria"
        allowed = quest_stage_themes()
        if store.current_theme not in allowed:
            remembered = store.stage_themes.get(persistent.school_stage)
            store.current_theme = remembered if remembered in allowed else allowed[0]
        store.stage_themes[persistent.school_stage] = store.current_theme

    def quest_setting(name, value):
        if name == "school_stage" and value not in QUEST_SCHOOL_PROFILES:
            return
        if name == "quest_motion" and value not in ("normal", "reduced", "off"):
            return
        if name not in ("school_stage", "quest_motion", "quest_guide_enabled"):
            return
        if name == "school_stage":
            # En el menú inicial, store todavía puede estar vacío: recuperar antes de guardar.
            if getattr(store, "main_menu", False) and persistent.quest_document:
                restore_quest_data()
            store.stage_themes[persistent.school_stage] = quest_theme_key()
        setattr(persistent, name, value)
        if name == "school_stage":
            quest_normalize_stage_theme()
            if not getattr(store, "main_menu", False) or persistent.quest_document:
                save_quest_data()
            if not getattr(store, "main_menu", False):
                quest_sync_theme_music()
            guide_event(quest_profile()["help"])
            renpy.hide_screen("quest_expedition_scene")
            renpy.hide_screen("quest_expedition_plan")
            renpy.hide_screen("quest_world_hub")
            if not quest_secondary() and store.task_filter == "week":
                store.task_filter = "all"
        if name == "quest_motion":
            renpy.run(Preference("transitions", "none" if value == "off" else "all"))
        renpy.save_persistent()
        renpy.restart_interaction()

    def close_quest_options():
        renpy.save_persistent()
        renpy.hide_screen("quest_options")
        renpy.restart_interaction()

    def quest_select_stage(stage):
        # Cambio de perfil desde la pantalla de opciones.
        quest_setting("school_stage", stage)
        # Tareas de otro perfil: preguntar aquí, donde el jugador acaba de
        # decidirlo. El aviso usa un zorder mayor que esta pantalla modal.
        if quest_secondary() and quest_tasks_without_expedition():
            renpy.show_screen("quest_convert_tasks")

    def quest_prepare_menu():
        if persistent.quest_document:
            restore_quest_data()
        quest_normalize_stage_theme()

    def open_quest_options():
        renpy.run(DisableAllInputValues())
        renpy.hide_screen("navigation_drawer")
        # La página y sus borradores permanecen debajo del panel de opciones.
        renpy.show_screen("quest_options")
        renpy.restart_interaction()

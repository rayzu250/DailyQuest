# Prueba visual y de persistencia aislada de los datos del usuario.
testcase ocean_theme:
    python:
        _test.timeout = 20.0
        assert "runtime-saves" in config.savedir.replace("\\", "/")
    run Jump("main_menu_todo")
    python:
        store.tasks = []
        store.task_lists = ["General"]
        store.current_list = "General"
        store.task_filter = "all"
        quest_setting("quest_guide_enabled", True)
        quest_setting("quest_motion", "normal")
        renpy.run(Preference("font size", 1.0))
        add_new_task("Preparar la mochila")
        add_subtask(0, "Guardar mis libros")
        before_tasks = [t.copy() for t in tasks]
    click "Menú"
    click "Cambiar mundo"
    click "Océano"
    python:
        assert current_theme == "océano"
        assert tasks == before_tasks
        assert guide_image() == "images/themes/ocean/shark.png"
        assert persistent.quest_document["theme"] == "océano"
    pause 0.5
    screenshot "ocean-tasks"
    click "Ayuda"
    pause 1.3
    screenshot "ocean-guide"
    click "Menú"
    screenshot "ocean-menu"
    click "Opciones"
    pause 0.3
    screenshot "ocean-options"
    click "Más grande"
    screenshot "ocean-options-large"
    click "Volver"
    run Preference("font size", 1.0)
    click "Ver pasos"
    screenshot "ocean-steps"
    click "Hora y recordatorio"
    screenshot "ocean-reminder"
    click "Cancelar"
    click "Menú"
    click "Calendario"
    pause 0.5
    screenshot "ocean-calendar"
    click "Menú"
    click "Nueva tarea"
    screenshot "ocean-form-disabled"
    click "Repetir esta tarea…"
    click "Elegir días del mes"
    screenshot "ocean-recurrence"
    click "Menú"
    click "Cambiar mundo"
    click "Bosque"
    python:
        assert current_theme == "bosque"
        assert not isinstance(guide_image(), str)
    screenshot "ocean-return-to-forest"
    click "Menú"
    click "Cambiar mundo"
    click "Océano"
    python:
        quest_setting("quest_motion", "off")
        guide_help()
        save_quest_data()
        store.current_theme = "bosque"
        assert restore_quest_data()
        assert current_theme == "océano" and tasks == before_tasks
    screenshot "ocean-motion-off"
    python:
        quest_setting("quest_motion", "normal")
        _test.timeout = 5.0

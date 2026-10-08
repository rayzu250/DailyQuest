# Cambiar mundos no debe alterar las tareas ni las preferencias.
testsuite illustrated_themes:
    before testcase:
        python:
            # La primera carga de texturas puede superar el límite de 5 segundos.
            _test.timeout = 20.0

    after testsuite:
        python:
            _test.timeout = 5.0

    testcase forest:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.task_filter = "all"
            quest_setting("quest_guide_enabled", True)
            quest_setting("quest_motion", "off")
            renpy.run(Preference("font size", 1.0))
            add_new_task("Preparar la mochila")
            add_subtask(0, "Guardar mis libros")
            before = quest_document()
        click "Menú"
        click "Cambiar mundo"
        click "Bosque"
        python:
            assert current_theme == "bosque"
            assert quest_document()["tasks"] == before["tasks"]
            assert persistent.quest_document["theme"] == "bosque"
            assert not isinstance(guide_image(), str)
        pause 0.3
        screenshot "forest-tasks"
        click "Ayuda"
        screenshot "forest-guide"
        click "Menú"
        screenshot "forest-menu"
        click "Calendario"
        screenshot "forest-calendar"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "forest-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        click "Menú"
        click "Mis tareas"
        click "Ver pasos"
        screenshot "forest-steps"
        python:
            save_quest_data()
            store.current_theme = "océano"
            assert restore_quest_data()
            assert current_theme == "bosque"
            assert quest_document()["tasks"] == before["tasks"]
        click "Menú"
        click "Cambiar mundo"
        click "Océano"
        python:
            assert guide_image() == "images/themes/ocean/shark.png"
            quest_setting("quest_motion", "normal")

    testcase sunset:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.task_filter = "all"
            quest_setting("quest_guide_enabled", True)
            quest_setting("quest_motion", "off")
            renpy.run(Preference("font size", 1.0))
            add_new_task("Preparar la mochila")
            add_subtask(0, "Guardar mis libros")
            before = quest_document()
        click "Menú"
        click "Cambiar mundo"
        click "Atardecer"
        python:
            assert current_theme == "atardecer"
            assert quest_document()["tasks"] == before["tasks"]
            assert persistent.quest_document["theme"] == "atardecer"
            assert guide_image() == "images/themes/sunset/guide.png"
        pause 0.3
        screenshot "sunset-tasks"
        click "Ayuda"
        screenshot "sunset-guide"
        click "Menú"
        screenshot "sunset-menu"
        click "Calendario"
        screenshot "sunset-calendar"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "sunset-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        click "Menú"
        click "Mis tareas"
        click "Ver pasos"
        screenshot "sunset-steps"
        python:
            save_quest_data()
            store.current_theme = "océano"
            assert restore_quest_data()
            assert current_theme == "atardecer"
            assert quest_document()["tasks"] == before["tasks"]
        click "Menú"
        click "Cambiar mundo"
        click "Océano"
        python:
            assert guide_image() == "images/themes/ocean/shark.png"
            quest_setting("quest_motion", "normal")

    testcase night:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.task_filter = "all"
            quest_setting("quest_guide_enabled", True)
            quest_setting("quest_motion", "off")
            renpy.run(Preference("font size", 1.0))
            add_new_task("Preparar la mochila")
            add_subtask(0, "Guardar mis libros")
            before = quest_document()
        click "Menú"
        click "Cambiar mundo"
        click "Noche"
        python:
            assert current_theme == "noche"
            assert quest_document()["tasks"] == before["tasks"]
            assert persistent.quest_document["theme"] == "noche"
            assert guide_image() == "images/themes/night/guide.png"
        pause 0.3
        screenshot "night-tasks"
        click "Ayuda"
        screenshot "night-guide"
        click "Menú"
        screenshot "night-menu"
        click "Calendario"
        screenshot "night-calendar"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "night-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        click "Menú"
        click "Mis tareas"
        click "Ver pasos"
        screenshot "night-steps"
        python:
            save_quest_data()
            store.current_theme = "océano"
            assert restore_quest_data()
            assert current_theme == "noche"
            assert quest_document()["tasks"] == before["tasks"]
        click "Menú"
        click "Cambiar mundo"
        click "Océano"
        python:
            assert guide_image() == "images/themes/ocean/shark.png"
            quest_setting("quest_motion", "normal")

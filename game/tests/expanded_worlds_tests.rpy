# Pruebas aisladas de compatibilidad, recompensas y música.
testsuite expanded_worlds:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            # Baseline explícito: otra suite pudo dejar un perfil secundario,
            # donde los pasos exigen una misión activa y no se otorgan frutas.
            quest_setting("school_stage", "primaria")
            _test.timeout = 25.0

    after testsuite:
        python:
            _test.timeout = 5.0

    testcase compatibility_and_music:
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            add_new_task("Cuidar mi mundo")
            add_subtask(0, "Completar un paso")
            toggle_subtask(0, 0)
            token = tasks[0]["subtasks"][0]["fruit"]
            original_tasks = quest_document()["tasks"]
            # Simular el catálogo guardado antes de incorporar los tres mundos.
            store.themes = {"bosque": themes["bosque"]}
            for name, art in QUEST_THEME_ART.items():
                quest_setting("school_stage", art.get("stage", "primaria"))
                select_quest_theme(name)
                assert renpy.loadable(quest_reward_image(token))
                assert art["folder"] in quest_reward_image(token)
                assert quest_document()["tasks"] == original_tasks
                store.current_theme = "bosque"
                assert restore_quest_data()
                assert current_theme == name
                assert name in themes
                assert quest_document()["tasks"] == original_tasks
            quest_setting("school_stage", "primaria")
            toggle_subtask(0, 0)
            toggle_subtask(0, 0)
            assert tasks[0]["subtasks"][0]["fruit"] == token
            assert last_reward is None
            assert not guide_animated
            assert config.main_menu_music is None
            for name in QUEST_THEME_ART:
                assert quest_music_track(name) == QUEST_THEME_MUSIC[name]
                assert renpy.loadable(quest_music_track(name))
            old_track = QUEST_THEME_MUSIC["robots"]
            old_play = renpy.music.play
            music_calls = []
            try:
                QUEST_THEME_MUSIC["robots"] = "audio/missing-test-track.ogg"
                assert quest_music_track("robots") == QUEST_MUSIC_FALLBACK
                QUEST_THEME_MUSIC["robots"] = "audio/reward_ding.ogg"
                renpy.music.play = lambda *args, calls=music_calls, **kwargs: calls.append((args, kwargs))
                select_quest_theme("robots")
                assert music_calls[-1][0][0] == "audio/reward_ding.ogg"
                assert music_calls[-1][1]["if_changed"] is True
                assert music_calls[-1][1]["channel"] == "music"
                assert music_calls[-1][1]["loop"] is True
                select_quest_theme("océano")
                assert music_calls[-1][0][0] == QUEST_THEME_MUSIC["océano"]
                assert quest_sync_theme_music in config.after_load_callbacks
            finally:
                renpy.music.play = old_play
                QUEST_THEME_MUSIC["robots"] = old_track
                quest_sync_theme_music()

    testcase prehistoric:
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
            add_new_task("Preparar mi aventura")
            add_subtask(0, "Guardar mis materiales")
        click "Menú"
        click "Cambiar mundo"
        screenshot "prehistoric-selector"
        click "Prehistórico"
        python:
            assert current_theme == "prehistoria"
            assert guide_image() == "images/themes/prehistoric/guide.png"
        pause 0.5
        screenshot "prehistoric-tasks"
        click "Ver pasos"
        python:
            toggle_subtask(0, 0)
            renpy.restart_interaction()
        pause 0.5
        screenshot "prehistoric-reward"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "prehistoric-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        python:
            quest_setting("quest_motion", "normal")

    testcase garden:
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
            add_new_task("Preparar mi aventura")
            add_subtask(0, "Guardar mis materiales")
        click "Menú"
        click "Cambiar mundo"
        screenshot "garden-selector"
        click "Jardín"
        python:
            assert current_theme == "jardín"
            assert guide_image() == "images/themes/garden/guide.png"
        pause 0.5
        screenshot "garden-tasks"
        click "Ver pasos"
        python:
            toggle_subtask(0, 0)
            renpy.restart_interaction()
        pause 0.5
        screenshot "garden-reward"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "garden-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        python:
            quest_setting("quest_motion", "normal")

    testcase robots:
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
            add_new_task("Preparar mi aventura")
            add_subtask(0, "Guardar mis materiales")
        click "Menú"
        click "Cambiar mundo"
        screenshot "robots-selector"
        click "Robots"
        python:
            assert current_theme == "robots"
            assert guide_image() == "images/themes/robots/guide.png"
        pause 0.5
        screenshot "robots-tasks"
        click "Ver pasos"
        python:
            toggle_subtask(0, 0)
            renpy.restart_interaction()
        pause 0.5
        screenshot "robots-reward"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "robots-options-large"
        click "Volver"
        run Preference("font size", 1.0)
        python:
            quest_setting("quest_motion", "normal")

testsuite options_guide:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            renpy.hide_screen("quest_options")

    testcase startup_options:
        run ShowMenu("preferences")
        assert screen "preferences"
        pause 0.5
        screenshot "options-startup"
        click "Silenciar todo"
        python:
            assert _preferences.get_mute("music")
            assert _preferences.get_mute("sfx")
        click "Silenciar todo"
        click "Volver"
        assert not screen "preferences"

    testcase in_task_options:
        run Jump("main_menu_todo")
        click "Agregar tarea"
        run SetVariable("new_title", "Preparar materiales")
        click "Menú"
        screenshot "menu-options"
        click "Opciones"
        assert screen "quest_options"
        assert screen "add_task_screen"
        python:
            widget = renpy.get_widget("quest_options", "quest_music_volume")
            widget.adjustment.change(widget.adjustment.range * 0.35)
            assert abs(_preferences.get_mixer("music") - 0.35) < 0.01
        click "Más grande"
        pause 0.3
        screenshot "options-large"
        python:
            widget = renpy.get_widget("quest_options", "quest_options_viewport")
            widget.yadjustment.change(650)
        pause 0.2
        click "Reducidas"
        python:
            assert persistent.quest_motion == "reduced"
            assert page_flip_or_none() is None
        screenshot "options-motion"
        click "Sin movimiento"
        python:
            assert persistent.quest_motion == "off"
        click "Otras opciones"
        python:
            widget = renpy.get_widget("quest_options", "quest_options_viewport")
            widget.yadjustment.change(widget.yadjustment.range)
        pause 0.2
        screenshot "options-advanced"
        click "Volver"
        assert not screen "quest_options"
        assert screen "add_task_screen"
        python:
            assert new_title == "Preparar materiales"
            assert _preferences.font_size == 1.15
        click "Guardar tarea"
        screenshot "guide-large"
        click "Ayuda"
        screenshot "guide-help-large"
        python:
            assert guide_message == quest_profile()["help"]
            quest_setting("school_stage", "secundaria")
            assert persistent.school_stage == "primaria"
        run Preference("font size", 1.0)

    testcase guide_events:
        run Jump("main_menu_todo")
        python:
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.completed_tasks = 0
            quest_setting("quest_motion", "normal")
            quest_setting("quest_guide_enabled", True)
            store.guide_session_greeted = False
            guide_greet()
            first = guide_event_serial
            guide_greet()
            assert guide_event_serial == first
            add_new_task("Leer un cuento")
            assert guide_message == "Ya anotaste lo que quieres hacer."
            complete_task(0)
            assert tasks[0]["celebrated"] and guide_pose == "guia_star"
        screenshot "guide-task-complete"
        python:
            complete_task(0)
            complete_task(0)
            assert not guide_animated
            assert completed_tasks == 1
            add_subtask(0, "Leer una página")
            toggle_subtask(0, 0)
            fruit = tasks[0]["subtasks"][0]["fruit"]
            assert last_reward == fruit and guide_fruit == fruit
            toggle_subtask(0, 0)
            toggle_subtask(0, 0)
            assert tasks[0]["subtasks"][0]["fruit"] == fruit
            assert last_reward is None and not guide_animated
            quest_setting("quest_guide_enabled", False)
        screenshot "guide-hidden"
        python:
            quest_setting("quest_guide_enabled", True)
            quest_setting("quest_motion", "reduced")
            guide_help()
        screenshot "guide-reduced"
        python:
            quest_setting("quest_motion", "off")
            guide_help()
        screenshot "guide-off"
        python:
            quest_setting("quest_motion", "normal")
            quest_setting("school_stage", "primaria")
            renpy.run(Preference("music volume", 0.35))
            renpy.save_persistent()

testcase quest_settings_restore:
    python:
        assert "runtime-saves" in config.savedir.replace("\\", "/")
        assert persistent.school_stage == "primaria"
        assert persistent.quest_motion == "normal"
        assert persistent.quest_guide_enabled
        assert abs(_preferences.get_volume("music") - 0.35) < 0.01

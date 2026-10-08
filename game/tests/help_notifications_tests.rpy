testsuite help_notifications:
    testcase reading_and_topics:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            quest_setting("school_stage", "primaria")
        run Jump("main_menu_todo")
        run Function(guide_help)
        assert screen "quest_help"
        click "Pasos pequeños"
        click "Ver ejemplo"
        pause 0.3
        screenshot "help-primary"
        click "Otro tema de ayuda"
        click "Descansar"
        click "Volver al juego"
        run Function(quest_setting, "school_stage", "secundaria")
        run Function(guide_help)
        click "Kanban: ver el trabajo"
        click "Ver ejemplo"
        pause 0.3
        screenshot "help-secondary"
        click "Volver al juego"
        run Preference("font size", 1.15)
        run renpy.notify("Los avisos están bloqueados. Activa el permiso de notificaciones. Puedes revisar las opciones del teléfono.")
        pause 0.4
        assert screen "notify"
        screenshot "notification-large"
        pause 4.0
        assert screen "notify"
        pause 7.0
        assert not screen "notify"
        run Preference("font size", 1.0)

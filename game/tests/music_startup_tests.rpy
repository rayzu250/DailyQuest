# Estas pruebas se ejecutan en dos aperturas reales sobre un directorio aislado.
testcase music_first_launch:
    python:
        assert "runtime-saves" in config.savedir.replace("\\", "/")
        _test.timeout = 20.0
        assert persistent.quest_document is None
        assert not main_menu
        assert config.main_menu_music is None
    assert not screen "main_menu"
    advance until screen "quest_text_editor"
    keysym "K_BACKSPACE"
    keysym "K_BACKSPACE"
    keysym "K_BACKSPACE"
    keysym "K_BACKSPACE"
    keysym "K_BACKSPACE"
    type "Prueba musical"
    click "Listo"
    advance until screen "view_tasks_screen"
    python:
        assert player_name == "Prueba musical"
        assert persistent.quest_document is not None
        add_new_task("Conservar al abrir")
        quest_setting("school_stage", "secundaria")
        select_quest_theme("mecha")
        renpy.run(Preference("music volume", 0.25))
        renpy.run(Preference("music mute", "enable"))
        save_quest_data()
    pause 1.0
    python:
        assert renpy.music.get_playing("music") == QUEST_THEME_MUSIC["mecha"]
    screenshot "music-first-direct"

testcase music_resume_launch:
    python:
        assert "runtime-saves" in config.savedir.replace("\\", "/")
        _test.timeout = 20.0
    assert screen "view_tasks_screen"
    assert not screen "main_menu"
    assert not screen "quest_text_editor"
    python:
        assert not main_menu
        assert player_name == "Prueba musical"
        assert tasks[0]["title"] == "Conservar al abrir"
        assert current_theme == "mecha" and quest_secondary()
        assert _preferences.get_mute("music")
    pause 1.0
    python:
        assert renpy.music.get_playing("music") == QUEST_THEME_MUSIC["mecha"]
        renpy.run(Preference("music mute", "disable"))
        assert abs(_preferences.get_volume("music") - 0.25) < 0.01
        select_quest_theme("arcane")
    pause 1.2
    python:
        assert renpy.music.get_playing("music") == QUEST_THEME_MUSIC["arcane"]
        quest_setting("school_stage", "primaria")
        select_quest_theme("océano")
    pause 1.2
    python:
        assert renpy.music.get_playing("music") == QUEST_THEME_MUSIC["océano"]
    click "Menú"
    click "Opciones"
    assert screen "quest_options"
    screenshot "music-options-direct"
    click "Volver"
    python:
        _test.timeout = 5.0

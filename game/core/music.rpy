init -2 python:
    QUEST_MUSIC_FALLBACK = "audio/Little_Notes_for_Big_Tasks.ogg"

    # TODO-music: aquí puedes sustituir las composiciones por otras pistas OGG.
    # El arranque directo usa la canción del mundo, sin pista de menú independiente.
    QUEST_THEME_MUSIC = {
        "bosque": "audio/themes/forest.ogg",
        "océano": "audio/themes/ocean.ogg",
        "atardecer": "audio/themes/sunset.ogg",
        "noche": "audio/themes/night.ogg",
        "prehistoria": "audio/themes/prehistoric.ogg",
        "jardín": "audio/themes/garden.ogg",
        "robots": "audio/themes/robots.ogg",
        # TODO-music: pistas más rítmicas de Secundaria.
        "mecha": "audio/themes/secondary/mecha.ogg",
        "arcane": "audio/themes/secondary/arcane.ogg",
        "stage": "audio/themes/secondary/stage.ogg",
    }

    def quest_music_track(theme=None):
        candidate = QUEST_THEME_MUSIC.get(theme or quest_theme_key())
        return candidate if candidate and renpy.loadable(candidate) else QUEST_MUSIC_FALLBACK

    def quest_sync_theme_music():
        # El mismo canal respeta el volumen elegido y evita reiniciar la misma canción.
        renpy.music.play(quest_music_track(), channel="music", loop=True,
            if_changed=True, fadeout=0.5, fadein=0.5)

init 20 python:
    config.after_load_callbacks.append(quest_sync_theme_music)

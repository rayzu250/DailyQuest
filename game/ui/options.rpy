# Mismo contenido desde el menú de inicio y durante una tarea.
screen quest_options():
    modal True
    zorder 180
    key "game_menu" action Function(close_quest_options)
    use quest_options_content(Function(close_quest_options))

screen quest_options_content(back_action):
    default advanced = False
    add Solid("#17352D")
    text "Opciones" size 54 bold True color "#FFFFFF" xalign 0.5 ypos 45
    textbutton "Volver" style "quest_option_button" xpos 50 ypos 135 action back_action
    viewport:
        id "quest_options_viewport"
        xpos 50 ypos 275 xsize 980 ysize 1550
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            xsize 910
            spacing 26
            text "Sonido" style "quest_option_heading"
            text "Música" style "quest_option_text"
            bar id "quest_music_volume" value Preference("music volume") style "quest_volume_bar"
            text "Efectos de sonido" style "quest_option_text"
            bar id "quest_sound_volume" value Preference("sound volume") style "quest_volume_bar"
            textbutton "Silenciar todo" style "quest_option_button" action Preference("all mute", "toggle")
            null height 12
            text "Etapa escolar" style "quest_option_heading"
            for stage, profile in QUEST_SCHOOL_PROFILES.items():
                textbutton (profile["label"] + " · " + profile["ages"]):
                    style "quest_option_button"
                    selected persistent.school_stage == stage
                    action Function(quest_setting, "school_stage", stage)
            text "Tareas y pasos pequeños para organizar tu día." style "quest_option_hint"
            text "Tamaño de letra" style "quest_option_heading"
            hbox:
                spacing 24
                textbutton "Grande" style "quest_option_button" action Preference("font size", 1.0)
                textbutton "Más grande" style "quest_option_button" action Preference("font size", 1.15)
            text "Animaciones" style "quest_option_heading"
            hbox:
                spacing 18
                for mode, caption in [("normal", "Normales"), ("reduced", "Reducidas"), ("off", "Sin movimiento")]:
                    textbutton caption:
                        style "quest_motion_button"
                        selected persistent.quest_motion == mode
                        action Function(quest_setting, "quest_motion", mode)
            text "Reducidas: apariciones suaves, sin saltos.\nSin movimiento: imágenes y mensajes quietos." style "quest_option_hint"
            textbutton "Mostrar a Guía":
                style "quest_option_button"
                selected persistent.quest_guide_enabled
                action Function(quest_setting, "quest_guide_enabled", not persistent.quest_guide_enabled)
            textbutton "Efecto de pasar página":
                style "quest_option_button"
                selected persistent.page_flip_enabled
                action Function(quest_setting, "page_flip_enabled", not persistent.page_flip_enabled)
            text "El efecto de página solo se usa con animaciones normales." style "quest_option_hint"
            textbutton ("Ocultar otras opciones" if advanced else "Otras opciones"):
                style "quest_option_button"
                action ToggleLocalVariable("advanced")
            if advanced:
                if renpy.variant("pc"):
                    text "Pantalla" style "quest_option_heading"
                    hbox:
                        spacing 24
                        textbutton "Ventana" style "quest_option_button" action Preference("display", "window")
                        textbutton "Completa" style "quest_option_button" action Preference("display", "fullscreen")
                text "Velocidad del texto" style "quest_option_text"
                bar value Preference("text speed") style "quest_volume_bar"
                text "Tiempo del autoavance" style "quest_option_text"
                bar value Preference("auto-forward time") style "quest_volume_bar"
                textbutton "Saltar texto no visto" style "quest_option_button" action Preference("skip", "toggle")
                textbutton "Seguir saltando tras elegir" style "quest_option_button" action Preference("after choices", "toggle")
                if config.has_voice:
                    text "Voz" style "quest_option_text"
                    bar value Preference("voice volume") style "quest_volume_bar"
            null height 40

style quest_option_heading:
    size 44
    color "#FFFFFF"
    bold True

style quest_option_text:
    size 40
    color "#FFFFFF"

style quest_option_hint:
    size 32
    color "#D5EEE4"

style quest_option_button:
    background Solid("#FFFFFF")
    hover_background Solid("#E8F5E9")
    selected_background Solid("#FFD54F")
    padding (24, 20)
    yminimum 100

style quest_option_button_text:
    size 38
    color "#17352D"
    yalign 0.5

style quest_motion_button is quest_option_button:
    xsize 285

style quest_motion_button_text is quest_option_button_text:
    size 34
    textalign 0.5

style quest_volume_bar:
    xsize 890
    ysize 70
    left_bar Solid("#FFD54F")
    right_bar Solid("#608478")
    thumb Solid("#FFFFFF", xsize=40, ysize=70)
    thumb_offset 20

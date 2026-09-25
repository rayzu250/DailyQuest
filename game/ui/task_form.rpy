screen add_task_screen():
    modal True
    default advanced = False
    key "game_menu" action Function(quest_navigate)
    add Solid(themes[current_theme]["bg"])
    use quest_header("Nueva tarea")
    viewport:
        xpos 60 ypos 280 xsize 960 ysize 1280
        draggable True
        mousewheel True
        scrollbars "vertical"
        vbox:
            spacing 30
            xsize 900
            text "¿Qué quieres hacer?" style "todo_text" textalign 0.0
            use quest_text_field("new_title", "¿Qué quieres hacer?", 60)
            text "Lista: [new_task_list]" style "todo_text" size 32
            textbutton ("Ocultar opciones" if advanced else "Repetir esta tarea…") style "todo_button" action ToggleScreenVariable("advanced")
            if advanced:
                for freq, caption in [("ninguna", "Una vez"), ("diaria", "Cada día"), ("semanal", "Elegir días de la semana"), ("mensual", "Elegir días del mes")]:
                    textbutton caption:
                        style "todo_button"
                        text_size 34
                        selected new_rec_freq == freq
                        action [SetVariable("new_rec_freq", freq), SetVariable("new_rec_days", [])]
                if new_rec_freq == "semanal":
                    grid 4 2:
                        spacing 14
                        for day in range(7):
                            textbutton WD_SHORT_ES[day].capitalize():
                                style "todo_button_rec"
                                text_style "todo_button_small_text"
                                selected day in new_rec_days
                                action Function(toggle_new_rec_day, day)
                        null
                elif new_rec_freq == "mensual":
                    grid 7 5:
                        spacing 12
                        for day in range(1, 36):
                            if day <= 31:
                                textbutton str(day):
                                    style "todo_button_rec"
                                    text_style "todo_button_small_text"
                                    selected day in new_rec_days
                                    action Function(toggle_new_rec_day, day)
                            else:
                                null
                textbutton "Asignar una hora":
                    style "todo_button"
                    selected new_has_time
                    action ToggleVariable("new_has_time")
                if new_has_time:
                    text ("Hora prevista: %02d:%02d" % (new_rec_h, new_rec_m)) style "todo_text" size 40
                    hbox:
                        spacing 20
                        textbutton "Hora −" style "todo_button_small" text_style "todo_button_small_text" action Function(bump_new_rec_h, -1)
                        textbutton "Hora +" style "todo_button_small" text_style "todo_button_small_text" action Function(bump_new_rec_h, 1)
                    hbox:
                        spacing 20
                        textbutton "Minuto −" style "todo_button_small" text_style "todo_button_small_text" action Function(bump_new_rec_m, -1)
                        textbutton "Minuto +" style "todo_button_small" text_style "todo_button_small_text" action Function(bump_new_rec_m, 1)
                    if new_rec_freq != "ninguna":
                        textbutton "Recordarme en el teléfono":
                            style "todo_button"
                            text_size 34
                            selected new_reminder
                            action ToggleVariable("new_reminder")
                    else:
                        text "Para un aviso de una sola vez, guarda la tarea y elige Fecha y Hora y recordatorio." style "todo_text" size 30
                    text quest_reminder_status() style "todo_text" size 30
    textbutton "Guardar tarea":
        style "todo_button"
        text_style "todo_button_text"
        xalign 0.5 yalign 0.91
        sensitive bool(new_title.strip())
        action Function(save_task_form)

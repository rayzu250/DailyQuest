screen task_reminder_screen(i):
    modal True
    zorder 140
    key "game_menu" action Hide("task_reminder_screen")
    add get_theme_options_bg()
    on "show" action SetVariable("reminder_form_error", "")
    # Una pantalla abierta que quedó fuera de la lista se cierra sola.
    $ reminder_task = tasks[i] if 0 <= i < len(tasks) else None
    if reminder_task is None:
        timer 0.01 action Hide("task_reminder_screen")
    else:
        default has_time = bool(quest_time_parts(quest_task_time(reminder_task)))
        default hour = (quest_time_parts(quest_task_time(reminder_task)) or (8, 0))[0]
        default minute = (quest_time_parts(quest_task_time(reminder_task)) or (8, 0))[1]
        default enabled = bool(reminder_task.get("reminder", False))
        text "Hora y recordatorio" style "quest_option_heading" size 50 xalign 0.5 ypos 60 yanchor 0 outlines [(2, "#032D46", 0, 0)]
        viewport:
            xpos 60 ypos 200 xsize 960 ysize 1370
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                xsize 890
                spacing 32
                text reminder_task["title"] style "quest_option_text"
                if reminder_form_error:
                    text reminder_form_error size 36 color "#FFE5A0"
                text ("Fecha de la tarea: " + date_tuple_to_string(reminder_task.get("deadline"))) style "quest_option_text"
                textbutton "Fecha del aviso" style "quest_option_button" action [SetVariable("reminder_form_error", ""), Show("deadline_pick_screen", i=i)]
                if reminder_task.get("recurrence"):
                    text ("Repetición: " + recurrence_description(reminder_task)) style "quest_option_hint"
                textbutton "Asignar una hora":
                    style "quest_option_button"
                    selected has_time
                    action ToggleScreenVariable("has_time")
                if has_time:
                    text ("Hora prevista: %02d:%02d" % (hour, minute)) style "quest_option_heading"
                    hbox:
                        spacing 24
                        textbutton "Hora −" style "quest_option_button" action SetScreenVariable("hour", (hour - 1) % 24)
                        textbutton "Hora +" style "quest_option_button" action SetScreenVariable("hour", (hour + 1) % 24)
                    hbox:
                        spacing 24
                        textbutton "Minuto −" style "quest_option_button" action SetScreenVariable("minute", (minute - 1) % 60)
                        textbutton "Minuto +" style "quest_option_button" action SetScreenVariable("minute", (minute + 1) % 60)
                    textbutton "Recordarme en el teléfono":
                        style "quest_option_button"
                        selected enabled
                        action ToggleScreenVariable("enabled")
                if not reminder_task.get("recurrence") and not valid_date(reminder_task.get("deadline")):
                    text "Para recibir un aviso, elige Fecha del aviso. Las fechas de los pasos son independientes." style "quest_option_hint"
                elif reminder_task.get("recurrence"):
                    text "Se avisará en los días elegidos, aunque el juego esté cerrado." style "quest_option_hint"
                text "Los horarios usan el reloj del teléfono (00:00 a 23:59). Las horas pasadas no generan avisos atrasados." style "quest_option_hint"
                text quest_reminder_status() style "quest_option_hint"
                if renpy.android:
                    textbutton "Permitir avisos" style "quest_option_button" action Function(quest_reminder_permission)
                    textbutton "Permitir horarios puntuales" style "quest_option_button" action Function(quest_exact_permission)
                    text "Puedes pedir ayuda a un adulto para estos permisos." style "quest_option_hint"
    hbox:
        xalign 0.5 ypos 1650 spacing 30
        textbutton "Cancelar" style "quest_option_button" action Hide("task_reminder_screen")
        textbutton "Guardar horario" style "quest_option_button" action Function(save_task_reminder, i, has_time, hour, minute, enabled and has_time)

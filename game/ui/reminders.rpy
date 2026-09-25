screen task_reminder_screen(i):
    modal True
    zorder 140
    default has_time = bool(quest_time_parts(quest_task_time(tasks[i])))
    default hour = (quest_time_parts(quest_task_time(tasks[i])) or (8, 0))[0]
    default minute = (quest_time_parts(quest_task_time(tasks[i])) or (8, 0))[1]
    default enabled = tasks[i].get("reminder", False)
    key "game_menu" action Hide("task_reminder_screen")
    add Solid("#17352D")
    text "Hora y recordatorio" style "quest_option_heading" size 50 xalign 0.5 ypos 60
    viewport:
        xpos 60 ypos 200 xsize 960 ysize 1370
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            xsize 890
            spacing 32
            text tasks[i]["title"] style "quest_option_text"
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
            if not tasks[i].get("recurrence") and not valid_date(tasks[i].get("deadline")):
                text "Para recibir un aviso, vuelve a Mis pasos y elige Fecha." style "quest_option_hint"
            elif tasks[i].get("recurrence"):
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

init python:
    def visible_task_indices():
        result = []
        for i, task in enumerate(store.tasks):
            if task.get("list", store.task_lists[0]) != store.current_list:
                continue
            date = next_deadline(task)
            if store.task_filter == "today" and (task.get("done") or not date or date > today_tuple()):
                continue
            if store.task_filter == "undated" and (date or task.get("done")):
                continue
            if store.task_filter == "week":
                week_end = _dt.date(*today_tuple()) + _dt.timedelta(days=6)
                if task.get("done") or not date or not (today_tuple() <= tuple(date) <= (week_end.year, week_end.month, week_end.day)):
                    continue
            result.append(i)
        return sorted(result, key=lambda i: (store.tasks[i].get("done", False), store.tasks[i].get("priority", 1) if quest_secondary() else 1))

screen view_tasks_screen():
    modal True
    if renpy.android:
        timer 2.0 repeat True action Function(quest_poll_reminders)
    on "show" action Function(guide_greet)
    add get_theme_bg()
    text _("Mis tareas") style "todo_title" xalign 0.5 ypos 45
    textbutton _("Menú") style "todo_button_small" text_style "todo_button_small_text" xpos 35 ypos 145 action Show("navigation_drawer")
    textbutton _("Mis logros") style "todo_button_small" text_style "todo_button_small_text" xalign 1.0 xoffset -35 ypos 145 action Function(quest_navigate, "progress_screen")
    textbutton _("Lista: [current_list] ▾") style "todo_button" text_size 34 xalign 0.5 ypos 265 action Function(quest_navigate, "lists_screen")
    hbox:
        xalign 0.5 ypos 390 spacing 16
        for value, caption in [("all", _("Todas")), ("today", _("Hoy")), ("undated", _("Sin fecha"))]:
            textbutton caption:
                style "todo_button_small"
                text_style "todo_button_small_text"
                selected task_filter == value
                action SetVariable("task_filter", value)
        if quest_secondary():
            textbutton _("7 días") style "todo_button_small" text_style "todo_button_small_text" selected task_filter == "week" action SetVariable("task_filter", "week")
    $ shown = visible_task_indices()
    viewport:
        xpos 50 ypos 505 xsize 980 ysize (940 if persistent.quest_guide_enabled else 1060)
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            spacing 22
            xsize 930
            if not shown:
                text "No hay tareas aquí.\nPuedes agregar una o mirar Todas." style "todo_text" size 36
            for i in shown:
                $ task = tasks[i]
                $ steps = subtask_progress(task)
                $ date = next_deadline(task)
                frame:
                    background get_theme_panel()
                    padding (24, 24)
                    xfill True
                    vbox:
                        spacing 18
                        textbutton task["title"]:
                            substitute False
                            text_size 40
                            text_color "#FFFFFF"
                            xfill True
                            action [SetVariable("new_subtask", ""), Show("task_detail_screen", i=i)]
                        if steps:
                            text "Pasos: [steps[0]] de [steps[1]]" size 30 color "#D5EEE4"
                        if date:
                            text ("Fecha: " + date_tuple_to_string(date)) size 30 color "#FFFFFF"
                        if quest_secondary():
                            text quest_expedition_state(task) size 28 color "#D5EEE4"
                        hbox:
                            spacing 20
                            textbutton ("Reabrir" if task["done"] else ("Misión" if quest_secondary() else "Completar")) style "todo_button_small" text_style "todo_button_small_text" action (Show("task_detail_screen", i=i) if quest_secondary() and not task["done"] else Function(complete_task, i))
                            textbutton "Ver pasos" style "todo_button_small" text_style "todo_button_small_text" action [SetVariable("new_subtask", ""), Show("task_detail_screen", i=i)]
    textbutton "Agregar tarea" style "todo_button" text_style "todo_button_text" xalign 0.5 yalign 0.94 action Function(open_task_form)
    use quest_guide

screen task_detail_screen(i):
    modal True
    key "game_menu" action Function(quest_navigate)
    add get_theme_bg()
    use quest_header("Mis pasos")
    $ task = tasks[i] if 0 <= i < len(tasks) else None
    if task is not None:
        viewport:
            xpos 50 ypos 280 xsize 980 ysize (1160 if persistent.quest_guide_enabled else 1240)
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                spacing 24
                xsize 930
                text task["title"] style "todo_text" size 46 substitute False
                if quest_secondary():
                    use quest_expedition_controls(i, task)
                hbox:
                    spacing 16
                    textbutton "Fecha" style "todo_button_small" text_style "todo_button_small_text" action Show("deadline_pick_screen", i=i)
                    textbutton "Mover a lista" style "todo_button_small" text_style "todo_button_small_text" action Show("move_task_screen", i=i)
                    textbutton _("Eliminar tarea") style "todo_button_small" text_style "todo_button_small_text" action Confirm(_("¿Borrar esta tarea para siempre?"), [Function(delete_task, i), Hide("task_detail_screen")])
                    textbutton "Renombrar tarea" style "todo_button_small" text_style "todo_button_small_text" action Function(open_rename_task_form, i)
                if valid_date(task.get("deadline")):
                    text date_tuple_to_string(task["deadline"]) style "todo_text" size 32
                textbutton "Hora y recordatorio" style "todo_button_small" text_style "todo_button_small_text" action Show("task_reminder_screen", i=i)
                if quest_task_time(task):
                    text ("Hora: " + quest_task_time(task) + (" · Aviso activado" if task.get("reminder") else "")) style "todo_text" size 32
                for j, step in enumerate(task.get("subtasks", [])):
                    frame:
                        background get_theme_panel()
                        padding (24, 24)
                        xfill True
                        vbox:
                            spacing 16
                            if step.get("done") and step.get("fruit"):
                                add quest_reward_image(step["fruit"], step.get("reward_world") if quest_secondary() else None):
                                    xysize (80, 80)
                                    fit "contain"
                            text step["text"] size 38 color "#FFFFFF"
                            if valid_date(step.get("deadline")):
                                text date_tuple_to_string(step["deadline"]) size 30 color "#D5EEE4"
                            hbox:
                                spacing 16
                                textbutton ("Hecho ✓" if step["done"] else "Completar") style "todo_button_small" text_style "todo_button_small_text" action Function(toggle_subtask, i, j)
                                textbutton "Fecha" style "todo_button_small" text_style "todo_button_small_text" action Show("deadline_pick_screen", i=i, j=j)
                                textbutton "Borrar" style "todo_button_small" text_style "todo_button_small_text" action Confirm("¿Borrar este paso?", Function(remove_subtask, i, j))
                text "Agrega un paso pequeño" style "todo_text" size 36
                use quest_text_field("new_subtask", "¿Cuál es el siguiente paso?", 120)
                textbutton "Agregar paso":
                    style "todo_button"
                    text_style "todo_button_text"
                    sensitive bool(new_subtask.strip())
                    action [Function(add_subtask, i, new_subtask), SetVariable("new_subtask", "")]
                if task.get("recurrence"):
                    text recurrence_description(task) style "todo_text" size 32
                    textbutton "Quitar repetición" style "todo_button_small" text_style "todo_button_small_text" action Confirm("¿Dejar de repetir esta tarea?", Function(clear_recurrence, i))
                    $ _series_size = len(quest_series_members(task))
                    $ _series_text = (_("¿Cerrar la serie? Solo se borrará esta tarea.") if _series_size == 1
                        else _("¿Cerrar la serie? Se borrarán las %d copias de la serie.") % _series_size)
                    textbutton _("Cerrar serie") style "todo_button_small" text_style "todo_button_small_text" action Confirm(_series_text, [Function(close_recurrence_series, i), Hide("task_detail_screen")])
        textbutton ("Reabrir tarea" if task["done"] else ("Finalizar misión" if quest_secondary() else "Completar tarea")) style "todo_button" text_style "todo_button_text" xalign 0.5 yalign 0.94 action Function(complete_task, i)
        use quest_guide

screen rename_task_screen(i):
    modal True
    zorder 140
    key "game_menu" action Hide("rename_task_screen")
    add Solid("#000000CC")
    frame:
        xalign 0.5 yalign 0.35 xsize 900
        padding (32, 32)
        background get_theme_panel()
        vbox:
            spacing 28
            text "Cambiar nombre de tarea" style "todo_text" size 42
            use quest_text_field("task_title_draft", "Nombre de la tarea", 120)
            hbox:
                spacing 24
                textbutton "Guardar nombre" style "todo_button_small" text_style "todo_button_small_text" sensitive bool(task_title_draft.strip()) action Function(save_task_title_form, i)
                textbutton "Cancelar" style "todo_button_small" text_style "todo_button_small_text" action Hide("rename_task_screen")

screen move_task_screen(i):
    modal True
    zorder 120
    key "game_menu" action Hide("move_task_screen")
    add Solid("#000000CC")
    frame:
        xalign 0.5 yalign 0.35 xsize 850
        padding (30, 30)
        background get_theme_panel()
        vbox:
            spacing 24
            text "Mover a otra lista" style "todo_text"
            viewport:
                xsize 780 ysize 600
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    spacing 20
                    for name in task_lists:
                        textbutton name style "todo_button" text_size 34 action [Function(move_task, i, name), Hide("move_task_screen")]
            textbutton "Cancelar" style "todo_button" action Hide("move_task_screen")

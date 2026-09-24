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
            result.append(i)
        return sorted(result, key=lambda i: store.tasks[i].get("done", False))

screen view_tasks_screen():
    modal True
    add Solid(themes[current_theme]["bg"])
    text "Mis tareas" style "todo_title" xalign 0.5 ypos 45
    textbutton "Menú" style "todo_button_small" text_style "todo_button_small_text" xpos 35 ypos 145 action Show("navigation_drawer")
    textbutton "Mis logros" style "todo_button_small" text_style "todo_button_small_text" xalign 1.0 xoffset -35 ypos 145 action Function(quest_navigate, "progress_screen")
    textbutton "Lista: [current_list] ▾" style "todo_button" text_size 34 xalign 0.5 ypos 265 action Function(quest_navigate, "lists_screen")
    hbox:
        xalign 0.5 ypos 390 spacing 16
        for value, caption in [("all", "Todas"), ("today", "Hoy"), ("undated", "Sin fecha")]:
            textbutton caption:
                style "todo_button_small"
                text_style "todo_button_small_text"
                selected task_filter == value
                action SetVariable("task_filter", value)
    $ shown = visible_task_indices()
    viewport:
        xpos 50 ypos 505 xsize 980 ysize 1060
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
                    background Solid("#17352D")
                    padding (24, 24)
                    xfill True
                    vbox:
                        spacing 18
                        textbutton task["title"]:
                            text_size 40
                            text_color "#FFFFFF"
                            xfill True
                            action [SetVariable("new_subtask", ""), Show("task_detail_screen", i=i)]
                        if steps:
                            text "Pasos: [steps[0]] de [steps[1]]" size 30 color "#D5EEE4"
                        if date:
                            text ("Fecha: " + date_tuple_to_string(date)) size 30 color "#FFFFFF"
                        hbox:
                            spacing 20
                            textbutton ("Reabrir" if task["done"] else "Completar") style "todo_button_small" text_style "todo_button_small_text" action Function(complete_task, i)
                            textbutton "Ver pasos" style "todo_button_small" text_style "todo_button_small_text" action [SetVariable("new_subtask", ""), Show("task_detail_screen", i=i)]
    textbutton "Agregar tarea" style "todo_button" text_style "todo_button_text" xalign 0.5 yalign 0.91 action Function(open_task_form)

screen task_detail_screen(i):
    modal True
    key "game_menu" action Function(quest_navigate)
    add Solid(themes[current_theme]["bg"])
    use quest_header("Mis pasos")
    $ task = tasks[i] if 0 <= i < len(tasks) else None
    if task is not None:
        viewport:
            xpos 50 ypos 280 xsize 980 ysize 1240
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                spacing 24
                xsize 930
                text task["title"] style "todo_text" size 46
                hbox:
                    spacing 16
                    textbutton "Fecha" style "todo_button_small" text_style "todo_button_small_text" action Show("deadline_pick_screen", i=i)
                    textbutton "Mover a lista" style "todo_button_small" text_style "todo_button_small_text" action Show("move_task_screen", i=i)
                if valid_date(task.get("deadline")):
                    text date_tuple_to_string(task["deadline"]) style "todo_text" size 32
                for j, step in enumerate(task.get("subtasks", [])):
                    frame:
                        background Solid("#17352D")
                        padding (24, 24)
                        xfill True
                        vbox:
                            spacing 16
                            if step.get("done") and step.get("fruit"):
                                add ("images/fruits/%s.png" % step["fruit"]):
                                    xysize (80, 80)
                                    fit "contain"
                            text step["text"] size 38 color "#FFFFFF"
                            if valid_date(step.get("deadline")):
                                text date_tuple_to_string(step["deadline"]) size 30 color "#D5EEE4"
                            hbox:
                                spacing 16
                                textbutton ("Hecho ✓" if step["done"] else "Completar") style "todo_button_small" text_style "todo_button_small_text" action [Function(toggle_subtask, i, j), Show("reward_popup")]
                                textbutton "Fecha" style "todo_button_small" text_style "todo_button_small_text" action Show("deadline_pick_screen", i=i, j=j)
                                textbutton "Borrar" style "todo_button_small" text_style "todo_button_small_text" action Confirm("¿Borrar este paso?", Function(remove_subtask, i, j))
                text "Agrega un paso pequeño" style "todo_text" size 36
                use quest_text_field("new_subtask", "¿Cuál es el siguiente paso?", 60)
                textbutton "Agregar paso":
                    style "todo_button"
                    text_style "todo_button_text"
                    sensitive bool(new_subtask.strip())
                    action [Function(add_subtask, i, new_subtask), SetVariable("new_subtask", "")]
                if task.get("recurrence"):
                    text recurrence_description(task) style "todo_text" size 32
                    textbutton "Quitar repetición" style "todo_button_small" text_style "todo_button_small_text" action Confirm("¿Dejar de repetir esta tarea?", Function(clear_recurrence, i))
        textbutton ("Reabrir tarea" if task["done"] else "Completar tarea") style "todo_button" text_style "todo_button_text" xalign 0.5 yalign 0.91 action Function(complete_task, i)

screen move_task_screen(i):
    modal True
    zorder 120
    key "game_menu" action Hide("move_task_screen")
    add Solid("#000000CC")
    frame:
        xalign 0.5 yalign 0.35 xsize 850
        padding (30, 30)
        background Solid("#17352D")
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

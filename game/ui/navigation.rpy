init python:
    QUEST_PAGES = ("main_todo", "add_task_screen", "task_detail_screen", "rename_task_screen", "lists_screen",
        "calendar_screen", "deadline_pick_screen", "theme_screen", "progress_screen", "move_task_screen",
        "quest_world_hub", "quest_expedition_scene", "quest_expedition_plan", "quest_convert_tasks")

    def quest_navigate(page="view_tasks_screen"):
        renpy.run(DisableAllInputValues())
        renpy.hide_screen("quest_text_editor")
        renpy.hide_screen("navigation_drawer")
        renpy.hide_screen("quest_options")
        renpy.hide_screen("task_reminder_screen")
        for name in QUEST_PAGES:
            renpy.hide_screen(name)
        store.show_list_dropdown = False
        if not renpy.get_screen("view_tasks_screen"):
            renpy.show_screen("view_tasks_screen")
        if page != "view_tasks_screen":
            renpy.show_screen(page)
        renpy.restart_interaction()

    def open_task_form():
        store.new_title = ""
        store.new_task_list = store.current_list
        store.new_rec_freq = "ninguna"
        store.new_rec_days = []
        store.new_rec_h = 8
        store.new_rec_m = 0
        store.new_has_time = False
        store.new_reminder = False
        quest_navigate("add_task_screen")

    def save_task_form():
        if not store.new_title.strip():
            renpy.notify("Escribe el nombre de tu tarea.")
            return
        if store.new_rec_freq in ("semanal", "mensual") and not store.new_rec_days:
            renpy.notify("Elige al menos un día para repetir.")
            return
        recurrence = None
        if store.new_rec_freq != "ninguna":
            recurrence = {"freq": store.new_rec_freq, "days": sorted(store.new_rec_days), "time": "%02d:%02d" % (store.new_rec_h, store.new_rec_m) if store.new_has_time else ""}
        add_new_task(store.new_title, store.new_task_list, recurrence)
        task = store.tasks[-1]
        task["time"] = "%02d:%02d" % (store.new_rec_h, store.new_rec_m) if store.new_has_time else ""
        task["reminder"] = bool(recurrence and store.new_has_time and store.new_reminder)
        save_quest_data()
        store.new_title = ""
        quest_navigate()
        if task["reminder"]:
            renpy.notify(quest_reminder_status())

    def open_rename_task_form(index):
        if 0 <= index < len(store.tasks):
            store.task_title_draft = store.tasks[index]["title"]
            renpy.show_screen("rename_task_screen", i=index)

    def save_task_title_form(index):
        if rename_task(index, store.task_title_draft):
            store.task_title_draft = ""
            renpy.hide_screen("rename_task_screen")
        renpy.restart_interaction()

    def open_rename_subtask_form(task_index, subtask_index):
        if not 0 <= task_index < len(store.tasks):
            return
        steps = store.tasks[task_index].get("subtasks", [])
        if not 0 <= subtask_index < len(steps):
            return
        store.subtask_text_draft = steps[subtask_index].get("text", "")
        renpy.show_screen("rename_subtask_screen", i=task_index, j=subtask_index)

    def save_subtask_title_form(task_index, subtask_index):
        if rename_subtask(task_index, subtask_index, store.subtask_text_draft):
            store.subtask_text_draft = ""
            renpy.hide_screen("rename_subtask_screen")
        renpy.restart_interaction()

screen quest_header(title):
    text title style "todo_title" size 54 xalign 0.5 ypos 50
    textbutton _("Volver") style "todo_button_small" text_style "todo_button_small_text" xpos 30 ypos 140 action Function(quest_navigate)
    textbutton _("Menú") style "todo_button_small" text_style "todo_button_small_text" xalign 1.0 xoffset -30 ypos 140 action Show("navigation_drawer")

screen navigation_drawer():
    modal True
    zorder 150
    key "game_menu" action Hide("navigation_drawer")
    button:
        style "blank_button"
        background Solid("#000000AA")
        xfill True
        yfill True
        action Hide("navigation_drawer")
    frame:
        xsize 600
        yfill True
        padding (40, 60)
        background get_theme_panel()
        vbox:
            spacing 28
            text "Daily Quest" size 52 color "#FFFFFF"
            textbutton _("Mis tareas") style "todo_button" action Function(quest_navigate)
            textbutton _("Nueva tarea") style "todo_button" action Function(open_task_form)
            textbutton _("Mis listas") style "todo_button" action Function(quest_navigate, "lists_screen")
            textbutton _("Calendario") style "todo_button" action Function(quest_navigate, "calendar_screen")
            textbutton _("Mis logros") style "todo_button" action Function(quest_navigate, "progress_screen")
            if quest_secondary():
                textbutton _("Expediciones") style "todo_button" action Function(quest_navigate, "quest_world_hub")
            textbutton _("Cambiar mundo") style "todo_button" action Function(quest_navigate, "theme_screen")
            textbutton _("Opciones") style "todo_button" action Function(open_quest_options)
            textbutton _("Ayuda") style "todo_button" action [Hide("navigation_drawer"), Function(guide_help)]
            textbutton _("Cerrar menú") style "todo_button" action Hide("navigation_drawer")

screen main_todo():
    on "show" action Function(quest_navigate)

init python:
    QUEST_PAGES = ("main_todo", "add_task_screen", "task_detail_screen", "lists_screen",
        "calendar_screen", "deadline_pick_screen", "theme_screen", "progress_screen", "move_task_screen")

    def quest_navigate(page="view_tasks_screen"):
        renpy.run(DisableAllInputValues())
        renpy.hide_screen("quest_text_editor")
        renpy.hide_screen("navigation_drawer")
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
            recurrence = {"freq": store.new_rec_freq, "days": sorted(store.new_rec_days), "time": ""}
        add_new_task(store.new_title, store.new_task_list, recurrence)
        store.new_title = ""
        quest_navigate()

screen quest_header(title):
    text title style "todo_title" size 54 xalign 0.5 ypos 50
    textbutton "Volver" style "todo_button_small" text_style "todo_button_small_text" xpos 30 ypos 140 action Function(quest_navigate)
    textbutton "Menú" style "todo_button_small" text_style "todo_button_small_text" xalign 1.0 xoffset -30 ypos 140 action Show("navigation_drawer")

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
        background Solid("#17352D")
        vbox:
            spacing 28
            text "Daily Quest" size 52 color "#FFFFFF"
            textbutton "Mis tareas" style "todo_button" action Function(quest_navigate)
            textbutton "Nueva tarea" style "todo_button" action Function(open_task_form)
            textbutton "Mis listas" style "todo_button" action Function(quest_navigate, "lists_screen")
            textbutton "Calendario" style "todo_button" action Function(quest_navigate, "calendar_screen")
            textbutton "Mis logros" style "todo_button" action Function(quest_navigate, "progress_screen")
            textbutton "Cambiar mundo" style "todo_button" action Function(quest_navigate, "theme_screen")
            textbutton "Cerrar menú" style "todo_button" action Hide("navigation_drawer")

screen main_todo():
    on "show" action Function(quest_navigate)

init python:
    def save_list_form():
        name = store.new_list_name.strip()
        if not name:
            renpy.notify("Escribe un nombre para la lista.")
            return
        if name in store.task_lists and name != store.renaming_list:
            renpy.notify("Ya hay una lista con ese nombre.")
            return
        if store.renaming_list:
            rename_task_list(store.renaming_list, name)
        else:
            add_task_list(name)
        store.renaming_list = None
        store.new_list_name = ""

screen lists_screen():
    modal True
    key "game_menu" action Function(quest_navigate)
    add Solid(themes[current_theme]["bg"])
    use quest_header("Mis listas")
    viewport:
        xpos 50 ypos 280 xsize 980 ysize 920
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            spacing 24
            xsize 930
            for name in task_lists:
                frame:
                    background Solid("#17352D")
                    padding (24, 24)
                    xfill True
                    vbox:
                        spacing 16
                        textbutton name text_size 42 text_color "#FFFFFF" action [SetVariable("current_list", name), Function(quest_navigate)]
                        hbox:
                            spacing 24
                            textbutton "Cambiar nombre" style "todo_button_small" text_style "todo_button_small_text" action [SetVariable("renaming_list", name), SetVariable("new_list_name", name)]
                            textbutton "Borrar" style "todo_button_small" text_style "todo_button_small_text" sensitive len(task_lists) > 1 action Confirm("¿Borrar esta lista? Sus tareas se moverán a otra lista.", Function(delete_task_list, name))
    vbox:
        xpos 60 ypos 1280 xsize 930 spacing 24
        text ("Cambiar nombre" if renaming_list else "Nueva lista") style "todo_text" size 36
        use quest_text_field("new_list_name", "Nombre de la lista", 30)
        hbox:
            spacing 24
            textbutton "Guardar lista" style "todo_button_small" text_style "todo_button_small_text" sensitive bool(new_list_name.strip()) action Function(save_list_form)
            if renaming_list:
                textbutton "Cancelar" style "todo_button_small" text_style "todo_button_small_text" action [SetVariable("renaming_list", None), SetVariable("new_list_name", "")]

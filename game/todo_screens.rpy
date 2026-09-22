################################################################################
## Pantallas del ToDo (estilos, menú principal, tareas, temas y progreso)
################################################################################

init offset = -1

default new_title = ""
default new_subtask = ""
default new_task_list = "General"
default new_list_name = ""
default renaming_list = None
default pick_year = None
default pick_month = None
default cal_selected = None
default show_list_dropdown = False
default new_task_list_locked = False

################################################################################
## Estilos base amigables para niños
################################################################################

style todo_button:
    background Frame(Solid("#FFFFFF"), 12, 12)
    hover_background Frame(Solid("#E8F5E9"), 12, 12)
    padding (42, 28)
    xminimum 460
    yminimum 94
    size_group "todo_buttons"

style todo_button_text:
    size 42
    color "#212121"
    hover_color "#1B5E20"
    font "DejaVuSans.ttf"          # Cambia por la fuente que uses
    textalign 0.5
    xalign 0.5
    yalign 0.5

# Variante compacta para filas con varios botones (grupo propio para no
# heredar el tamaño de los botones grandes)
style todo_button_small is todo_button:
    padding (20, 14)
    xminimum 180
    yminimum 66
    size_group "todo_row_buttons"

style todo_button_small_text is todo_button_text:
    size 26

style todo_title:
    size 64
    color "#FFFFFF"
    bold True
    textalign 0.5
    outlines [(3, "#00000080", 0, 0)]

style todo_text:
    size 40
    color "#FFFFFF"
    textalign 0.5
    outlines [(2, "#00000060", 0, 0)]

style task_item:
    size 38
    color "#FFFFFF"
    outlines [(2, "#00000050", 0, 0)]

style subtask_button:
    background Solid("#FFFFFF22")
    hover_background Solid("#FFFFFF44")
    padding (22, 16)
    xminimum 640

style subtask_text:
    size 38
    color "#FFFFFF"

style cal_day:
    background Solid("#FFFFFF22")
    hover_background Solid("#FFFFFF55")

style cal_day_text:
    size 34
    color "#FFFFFF"

################################################################################
## Pantalla principal (Main Menu ToDo)
################################################################################

screen main_todo():
    tag menu
    modal True

    # Fondo según tema actual
    add Solid(themes[current_theme]["bg"])

    # Título
    text "¡Mis Proyectos!" style "todo_title" xalign 0.5 ypos 55

    # Nombre del niño
    text "Hola [player_name]!" style "todo_text" xalign 0.5 ypos 150

    # Contador de estrellas
    hbox:
        xalign 0.5
        ypos 230
        spacing 15
        text "★" size 52 color "#FFD700"
        text "[completed_tasks] estrellas" style "todo_text"

    # Botones principales
    vbox:
        xalign 0.5
        yalign 0.55
        spacing 28

        textbutton "Ver mis tareas" action Show("view_tasks_screen", transition=page_flip_or_none) style "todo_button" text_style "todo_button_text"
        textbutton "Agregar nueva tarea" action [SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), Show("add_task_screen", transition=page_flip_or_none)] style "todo_button" text_style "todo_button_text"
        textbutton "Ver calendario" action [SetVariable("pick_year", None), SetVariable("pick_month", None), SetVariable("cal_selected", None), Show("calendar_screen", transition=page_flip_or_none)] style "todo_button" text_style "todo_button_text"
        textbutton "Cambiar tema" action Show("theme_screen", transition=page_flip_or_none) style "todo_button" text_style "todo_button_text"
        textbutton "Ver mi progreso" action Show("progress_screen", transition=page_flip_or_none) style "todo_button" text_style "todo_button_text"

    # Botón salir
    textbutton "Salir" action Return() style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.92

################################################################################
## Pantalla: Ver tareas
################################################################################

screen view_tasks_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mis Tareas" style "todo_title" xalign 0.5 ypos 35

    text "Lista: [current_list.capitalize()]" style "todo_text" size 34 xalign 0.5 ypos 115

    # Selector de listas desplegable
    $ dd_arrow = " ▴" if show_list_dropdown else " ▾"
    textbutton "[current_list.capitalize()][dd_arrow]" action ToggleVariable("show_list_dropdown"):
        style "todo_button"
        text_style "todo_button_text"
        xalign 0.5
        ypos 170
        xminimum 460
        yminimum 80

    $ shown = [i for i, t in enumerate(tasks) if t.get("list", task_lists[0]) == current_list]

    if not tasks:
        text "¡Todavía no tienes tareas!\nAgrega una para empezar tu aventura." style "todo_text" xalign 0.5 ypos 400
    elif not shown:
        text "Esta lista aún está vacía.\n¡Agrega una tarea aquí!" style "todo_text" xalign 0.5 ypos 400
    else:
        viewport:
            xalign 0.5
            ypos 270
            xsize 900
            ysize 480
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 18
                xalign 0.5

                for i in shown:
                    $ t = tasks[i]
                    $ status = "✓  " if t["done"] else "○  "
                    $ color_status = "#A5D6A7" if t["done"] else "#FFFFFF"
                    $ sp = subtask_progress(t)
                    $ dl = next_deadline(t)
                    $ dcolor = deadline_date_color(dl)

                    frame:
                        background Solid("#FFFFFF22")
                        padding (25, 20)
                        xminimum 850

                        vbox:
                            spacing 14

                            hbox:
                                spacing 20
                                text "[status][t['title']]" style "task_item" color color_status xmaximum 500
                                if sp:
                                    text "[sp[0]]/[sp[1]]" style "task_item" size 30 color "#81C784" xalign 0.5 xminimum 70
                                if dl:
                                    text date_tuple_to_string(dl) style "task_item" size 28 color (dcolor or "#81C784") xalign 0.5 xminimum 110

                            hbox:
                                spacing 20
                                xalign 1.0

                                if not t["done"]:
                                    textbutton "Completar" action Function(complete_task, i):
                                        style "todo_button_small"
                                        text_style "todo_button_small_text"
                                textbutton "Mover" action Show("move_task_screen", i=i, transition=page_flip_or_none):
                                    style "todo_button_small"
                                    text_style "todo_button_small_text"
                                textbutton "Detalles" action Show("task_detail_screen", i=i, transition=page_flip_or_none):
                                    style "todo_button_small"
                                    text_style "todo_button_small_text"

    # Botones inferiores
    hbox:
        xalign 0.5
        ypos 0.90
        spacing 40

        textbutton "Volver" action Hide("view_tasks_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text"
        textbutton "Agregar tarea" action [SetVariable("show_list_dropdown", False), SetVariable("new_task_list", current_list), SetVariable("new_task_list_locked", True), Show("add_task_screen", transition=page_flip_or_none)] style "todo_button" text_style "todo_button_text"

    # Panel desplegable de listas (al final para que pinte encima de la lista)
    if show_list_dropdown:
        frame:
            background Solid("#2E7D32")
            padding (16, 16)
            xalign 0.5
            ypos 265
            xmaximum 560

            viewport:
                xsize 500
                ysize 420
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 10
                    xalign 0.5

                    for lname in task_lists:
                        $ lbg2 = Frame(Solid("#FFD54F"), 12, 12) if lname == current_list else Frame(Solid("#FFFFFF"), 12, 12)
                        textbutton lname.capitalize() action [SetVariable("current_list", lname), SetVariable("show_list_dropdown", False)]:
                            style "todo_button"
                            text_size 32
                            xminimum 440
                            yminimum 70
                            background lbg2

                    textbutton "Listas" action [SetVariable("show_list_dropdown", False), Show("lists_screen", transition=page_flip_or_none)]:
                        style "todo_button"
                        text_size 32
                        xminimum 440
                        yminimum 70

################################################################################
## Pantalla: Mover tarea a otra lista
################################################################################

screen move_task_screen(i):
    modal True

    add Solid("#000000AA")

    $ t = tasks[i] if 0 <= i < len(tasks) else None

    frame:
        background Solid("#2E7D32")
        padding (30, 30)
        xalign 0.5
        yalign 0.4
        xmaximum 640

        vbox:
            spacing 14
            xalign 0.5

            text "Mover tarea a…" style "todo_text" size 40 xalign 0.5

            if t is None:
                text "Esta tarea ya no existe." style "todo_text" xalign 0.5
            else:
                viewport:
                    xsize 540
                    ysize 380
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 10
                        xalign 0.5

                        for lname in task_lists:
                            $ mbg = Frame(Solid("#FFD54F"), 12, 12) if lname == t.get("list", task_lists[0]) else Frame(Solid("#FFFFFF"), 12, 12)
                            textbutton lname.capitalize() action [Function(move_task, i, lname), Hide("move_task_screen", transition=page_flip_back_or_none)]:
                                style "todo_button"
                                text_size 32
                                xminimum 460
                                yminimum 70
                                background mbg

            textbutton "Cancelar" action Hide("move_task_screen", transition=page_flip_back_or_none):
                style "todo_button"
                text_style "todo_button_text"
                xalign 0.5

################################################################################
## Pantalla: Agregar tarea
################################################################################

screen add_task_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    $ new_task_list = new_task_list if new_task_list in task_lists else task_lists[0]

    text "Nueva Tarea / Proyecto" style "todo_title" xalign 0.5 ypos 70

    text "¿Qué quieres lograr?" style "todo_text" xalign 0.5 ypos 200

    frame:
        background Solid("#00000040")
        padding (20, 15)
        xalign 0.5
        ypos 280
        xmaximum 760

        input:
            value VariableInputValue("new_title")
            length 40
            size 40
            color "#FFFFFF"
            xalign 0.0
            yalign 0.5

    if new_task_list_locked:
        text "Lista: [new_task_list.capitalize()]" style "todo_text" xalign 0.5 ypos 430
    else:
        text "¿En qué lista?" style "todo_text" xalign 0.5 ypos 430

        viewport:
            xalign 0.5
            ypos 490
            xsize 940
            ysize 96
            scrollbars "horizontal"
            draggable True
            mousewheel "horizontal"

            hbox:
                spacing 12

                for lname in task_lists:
                    $ lbg = Frame(Solid("#FFD54F"), 12, 12) if lname == new_task_list else Frame(Solid("#FFFFFF"), 12, 12)
                    textbutton lname.capitalize() action SetVariable("new_task_list", lname):
                        style "todo_button"
                        text_size 30
                        xminimum 180
                        yminimum 62
                        background lbg

    hbox:
        xalign 0.5
        ypos 660
        spacing 50

        textbutton "Guardar":
            action [Function(add_new_task, new_title, new_task_list), SetVariable("new_title", ""), SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), Hide("add_task_screen", transition=page_flip_back_or_none)]
            style "todo_button"
            text_style "todo_button_text"

        textbutton "Cancelar":
            action [SetVariable("new_title", ""), SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), Hide("add_task_screen", transition=page_flip_back_or_none)]
            style "todo_button"
            text_style "todo_button_text"

################################################################################
## Pantalla: Cambiar tema
################################################################################

screen theme_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Elige tu mundo" style "todo_title" xalign 0.5 ypos 60

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        for theme_name in themes:
            textbutton theme_name.capitalize() action [SetVariable("current_theme", theme_name), Hide("theme_screen")] style "todo_button" text_style "todo_button_text"

    textbutton "Volver" action Hide("theme_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Progreso
################################################################################

screen progress_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mi Progreso" style "todo_title" xalign 0.5 ypos 60

    $ total = len(tasks)
    $ done = sum(1 for t in tasks if t["done"])
    $ percent = int((done / total * 100) if total > 0 else 0)

    vbox:
        xalign 0.5
        yalign 0.45
        spacing 30

        text "Tareas completadas: [done] / [total]" style "todo_text"
        text "Estrellas ganadas: [completed_tasks]" style "todo_text" size 46

        # Barra de progreso simple
        fixed:
            xsize 720
            ysize 56
            xalign 0.5

            add Solid("#FFFFFF40")
            add Solid(themes[current_theme]["accent"]) xsize int(720 * percent / 100)

        text "[percent]%" style "todo_text" size 52

        if percent == 100 and total > 0:
            text "¡Eres un campeón de los proyectos!" style "todo_text" color "#FFD700"
        elif percent >= 50:
            text "¡Vas muy bien! Sigue así." style "todo_text"
        else:
            text "Cada tarea te acerca a tu meta." style "todo_text"

    textbutton "Volver" action Hide("progress_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Popup de recompensa (fruta + guía)
################################################################################

screen reward_popup():
    zorder 100

    # Solo pinta si hay recompensa pendiente (al desmarcar no molesta)
    if last_reward:
        add "images/fruits/%s.png" % last_reward:
            at reward_pop_up
            xalign 0.5
            yalign 0.38
            xysize (192, 192)
            fit "contain"

        add "images/guias/red.png":
            at guia_reward_bounce
            xalign 0.88
            yalign 1.0

        timer 1.2 action [SetVariable("last_reward", None), Hide("reward_popup")]

################################################################################
## Pantalla: Detalles de tarea (subtareas)
################################################################################

screen task_detail_screen(i):
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Detalles" style "todo_title" xalign 0.5 ypos 50

    $ t = tasks[i] if 0 <= i < len(tasks) else None

    if t is None:
        text "Esta tarea ya no existe." style "todo_text" xalign 0.5 yalign 0.45
        textbutton "Volver" action Hide("task_detail_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
            xalign 0.5 
            ypos 0.90
    else:
        text "[t['title']]" style "todo_text" size 44 bold True xalign 0.5 ypos 140

        $ substeps = t.get("subtasks", [])

        if not substeps:
            text "Aún no tiene subtareas.\n¡Divide la tarea en pasos divertidos!" style "todo_text" xalign 0.5 ypos 260
        else:
            viewport:
                xalign 0.5
                ypos 260
                xsize 900
                ysize 460
                scrollbars "vertical"
                mousewheel True
                draggable True

                vbox:
                    spacing 18
                    xalign 0.5

                    for j, st in enumerate(substeps):
                        $ is_st_done = st.get("done", False)
                        # Si está completada, muestra su fruta; si no, la casilla vacía
                        $ fruit_img = "images/fruits/%s.png" % st["fruit"] if (is_st_done and st.get("fruit")) else None
                        $ st_color = "#A5D6A7" if is_st_done else "#FFFFFF"
                        $ sdl = st.get("deadline")
                        $ sdc = subtask_deadline_color(st)

                        frame:
                            background Solid("#FFFFFF22")
                            padding (20, 16)
                            xminimum 850

                            hbox:
                                spacing 12
                                if fruit_img:
                                    add fruit_img:
                                        xysize (56, 56)
                                        fit "contain"
                                        yalign 0.5
                                else:
                                    fixed:
                                        xysize (56, 56)
                                        text "○" style "subtask_text" xalign 0.5 yalign 0.5
                                textbutton "[st.get('text', '')]" action [Function(toggle_subtask, i, j), Show("reward_popup")]:
                                    style "subtask_button"
                                    text_style "subtask_text"
                                    text_color st_color
                                    xminimum 360
                                if valid_date(sdl):
                                    text date_tuple_to_string(sdl) style "subtask_text" size 28 color (sdc or "#81C784") xalign 0.5 xminimum 110
                                textbutton "Fecha" action Show("deadline_pick_screen", i=i, j=j, transition=page_flip_or_none):
                                    style "todo_button" 
                                    text_size 26 
                                    xminimum 130 
                                    yminimum 58
                                textbutton "✕" action Function(remove_subtask, i, j):
                                    style "todo_button"
                                    text_size 28
                                    xminimum 100
                                    yminimum 58

        # Entrada para agregar subtarea
        frame:
            background Solid("#00000040")
            padding (20, 15)
            xalign 0.5
            ypos 760
            xmaximum 760

            input:
                value VariableInputValue("new_subtask")
                length 60
                size 40
                color "#FFFFFF"
                xalign 0.0
                yalign 0.5

        textbutton "Agregar" action [Function(add_subtask, i, new_subtask), SetVariable("new_subtask", "")] style "todo_button" text_style "todo_button_text":
            xalign 0.5
            ypos 880

        textbutton "Volver" action Hide("task_detail_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
            xalign 0.5 
            ypos 0.90

################################################################################
## Pantalla: Gestión de listas
################################################################################

screen lists_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mis Listas" style "todo_title" xalign 0.5 ypos 50

    viewport:
        xalign 0.5
        ypos 150
        xsize 900
        ysize 420
        scrollbars "vertical"
        mousewheel True
        draggable True

        vbox:
            spacing 18
            xalign 0.5

            for lname in task_lists:
                frame:
                    background Solid("#FFFFFF22")
                    padding (20, 16)
                    xminimum 850

                    vbox:
                        spacing 12

                        textbutton lname.capitalize() action [SetVariable("current_list", lname), Hide("lists_screen")]:
                            style "subtask_button"
                            text_style "subtask_text"
                            xminimum 460

                        hbox:
                            spacing 20
                            xalign 1.0

                            textbutton "Renombrar" action [SetVariable("renaming_list", lname), SetVariable("new_list_name", lname)]:
                                style "todo_button"
                                text_size 30
                                xminimum 190
                                yminimum 64
                            textbutton "✕" action Function(delete_task_list, lname):
                                style "todo_button"
                                text_size 30
                                xminimum 110
                                yminimum 64

    if renaming_list:
        text "Renombrando: [renaming_list]" style "todo_text" size 32 xalign 0.5 ypos 620

        frame:
            background Solid("#00000040")
            padding (20, 15)
            xalign 0.5
            ypos 680
            xmaximum 760

            input:
                value VariableInputValue("new_list_name")
                length 30
                size 36
                color "#FFFFFF"
                xalign 0.0
                yalign 0.5

        hbox:
            xalign 0.5
            ypos 800
            spacing 30

            textbutton "Guardar nombre":
                action [Function(rename_task_list, renaming_list, new_list_name), SetVariable("renaming_list", None), SetVariable("new_list_name", "")]
                style "todo_button"
                text_style "todo_button_text"

            textbutton "Cancelar":
                action [SetVariable("renaming_list", None), SetVariable("new_list_name", "")]
                style "todo_button"
                text_style "todo_button_text"
    else:
        text "Crea una nueva lista" style "todo_text" size 32 xalign 0.5 ypos 620

        frame:
            background Solid("#00000040")
            padding (20, 15)
            xalign 0.5
            ypos 680
            xmaximum 760

            input:
                value VariableInputValue("new_list_name")
                length 30
                size 36
                color "#FFFFFF"
                xalign 0.0
                yalign 0.5

        textbutton "Crear lista":
            action [Function(add_task_list, new_list_name), SetVariable("new_list_name", "")]
            style "todo_button"
            text_style "todo_button_text"
            xalign 0.5
            ypos 800

    textbutton "Volver" action Hide("lists_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
        xalign 0.5 
        ypos 0.90

################################################################################
## Pantalla: Elegir fecha límite
################################################################################

screen deadline_pick_screen(i, j=None):
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Elige la fecha límite" style "todo_title" xalign 0.5 ypos 40

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 115

    hbox:
        xalign 0.5
        ypos 190
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34
        textbutton "Hoy" action Function(set_pick_today) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34
        textbutton "▶" action Function(month_move, 1) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34

    grid 7 1:
        xalign 0.5
        ypos 275
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                text wd style "todo_text" size 34 xalign 0.5 yalign 0.5

    vbox:
        xalign 0.5
        ypos 320
        spacing 8

        for week in grid:
            grid 7 1:
                xalign 0.5
                xspacing 8

                for d in week:
                    $ dkey = (d.year, d.month, d.day)
                    $ in_month = d.month == cm
                    $ is_today = dkey == today_tuple()
                    $ has_dl = count_deadlines_on(dkey) > 0
                    $ d_bg = "#4CAF5088" if has_dl else ("#FFFFFF33" if in_month else "#FFFFFF11")
                    $ d_tcolor = "#FFD54F" if is_today else ("#FFFFFF55" if not in_month else "#FFFFFF")
                    $ d_action = Function(set_subtask_deadline, i, j, dkey) if j is not None else Function(set_deadline, i, dkey)

                    textbutton str(d.day):
                        action d_action
                        background d_bg
                        style "cal_day"
                        text_style "cal_day_text"
                        text_color d_tcolor
                        xsize 120
                        ysize 76

    $ clear_dl_action = [Function(set_subtask_deadline, i, j, None) if j is not None else Function(set_deadline, i, None), Hide("deadline_pick_screen")]

    textbutton "Quitar fecha" action clear_dl_action style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 850

    textbutton "Volver" action Hide("deadline_pick_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Calendario
################################################################################

screen calendar_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mi Calendario" style "todo_title" xalign 0.5 ypos 40

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)
    $ sel = cal_selected if valid_date(cal_selected) else today_tuple()

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 115

    hbox:
        xalign 0.5
        ypos 190
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34
        textbutton "Hoy" action Function(set_pick_today) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34
        textbutton "▶" action Function(month_move, 1) style "todo_button" text_style "todo_button_text":
            xminimum 130
            yminimum 70
            text_size 34

    grid 7 1:
        xalign 0.5
        ypos 270
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                text wd style "todo_text" size 34 xalign 0.5 yalign 0.01

    vbox:
        xalign 0.5
        ypos 350
        spacing 7

        for week in grid:
            grid 7 1:
                xalign 0.5
                xspacing 8

                for d in week:
                    $ dkey = (d.year, d.month, d.day)
                    $ in_month = d.month == cm
                    $ is_today = dkey == today_tuple()
                    $ is_sel = dkey == sel
                    $ n_dl = count_deadlines_on(dkey)
                    $ dlabel = ("%d" % d.day) + (("  ·%d" % n_dl) if n_dl else "")
                    $ d_bg = "#E8F5E9" if is_sel else ("#4CAF5088" if n_dl else ("#FFD54F44" if is_today else ("#FFFFFF33" if in_month else "#FFFFFF11")))
                    $ d_tcolor = "#1B5E20" if is_sel else ("#FFD54F" if is_today else ("#FFFFFF55" if not in_month else "#FFFFFF"))

                    textbutton dlabel:
                        action SetVariable("cal_selected", dkey)
                        background d_bg
                        style "cal_day"
                        text_style "cal_day_text"
                        text_color d_tcolor
                        xsize 120
                        ysize 70

    $ sel_title = "Tareas del %d de %s" % (sel[2], MONTHS_ES[sel[1] - 1])

    text "[sel_title]" style "todo_text" size 36 xalign 0.5 ypos 800

    python:
        sel_tasks = []
        for idx, t in enumerate(tasks):
            steps = t.get("subtasks", [])
            for j, s in enumerate(steps):
                if valid_date(s.get("deadline")) and tuple(s["deadline"]) == sel:
                    sel_tasks.append((idx, j, s.get("text", "")))
            if not steps and valid_date(t.get("deadline")) and tuple(t["deadline"]) == sel:
                sel_tasks.append((idx, None, ""))

    if not sel_tasks:
        text "No hay tareas para este día." style "todo_text" xalign 0.5 ypos 845
    else:
        viewport:
            xalign 0.5
            ypos 845
            xsize 900
            ysize 420
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 18
                xalign 0.5

                for idx, j, stext in sel_tasks:
                    $ t = tasks[idx]
                    $ c_status = "#A5D6A7" if t["done"] else "#FFFFFF"
                    $ dlabel2 = t["title"] + ((" - " + stext) if stext else "")

                    frame:
                        background Solid("#FFFFFF22")
                        padding (20, 16)
                        xminimum 850

                        hbox:
                            spacing 15
                            text "[dlabel2]" style "task_item" color c_status xmaximum 540
                            text "· [t.get('list', task_lists[0]).capitalize()]" style "task_item" size 30 color "#B9F6CA" xmaximum 180
                            textbutton "Abrir" action Show("task_detail_screen", i=idx, transition=page_flip_or_none):
                                style "todo_button"
                                text_size 30
                                xminimum 150
                                yminimum 66

    textbutton "Volver" action Hide("calendar_screen", transition=page_flip_back_or_none) style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.90
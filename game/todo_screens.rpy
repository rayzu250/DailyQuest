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
default new_rec_freq = "ninguna"
default new_rec_days = []
default new_rec_h = 8
default new_rec_m = 0
default show_rec_dropdown = False
default show_add_task_list_dropdown = False

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

# Variante para navegación de mes (grupo propio para no heredar el
# tamaño de los botones grandes)
style todo_button_nav is todo_button:
    padding (16, 10)
    xminimum 130
    yminimum 70
    size_group "todo_nav_buttons"

style todo_button_nav_text is todo_button_text:
    size 34

# Variante para chips de recurrencia (grupo propio para no heredar el
# tamaño de los botones grandes)
style todo_button_rec is todo_button:
    padding (20, 12)
    xminimum 100
    yminimum 62
    size_group "todo_rec_buttons"

# Opciones del panel de frecuencia (uniformes entre sí, sin afectar a las chips)
style todo_button_rec_panel is todo_button_rec:
    size_group "todo_rec_panel"

# Botones Fecha/Quitar de detalle (uniformes entre sí)
style todo_button_detail is todo_button:
    padding (16, 10)
    xminimum 120
    yminimum 58
    size_group "todo_detail_buttons"

# Texto grande para botones de icono (✓ / ✕ junto a los inputs)
style todo_button_icon_text is todo_button_text:
    size 48

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

# Botón invisible para cerrar el drawer al tocar fuera
style blank_button is empty

# Botones del panel lateral (grupo propio para no heredar otros tamaños)
style drawer_button:
    background Frame(Solid("#FFFFFF"), 12, 12)
    hover_background Frame(Solid("#FFD54F"), 12, 12)
    padding (20, 12)
    xminimum 360
    yminimum 64
    size_group "todo_drawer_buttons"

style drawer_button_text:
    size 30
    color "#212121"
    hover_color "#1B5E20"
    textalign 0.5
    xalign 0.5
    yalign 0.5

style drawer_button_close is drawer_button

style drawer_button_close_text is drawer_button_text:
    color "#EF5350"

################################################################################
## Pantalla: Panel lateral de navegación estilo cómic
################################################################################

screen navigation_drawer():
    modal True

    # Fondo para cerrar al tocar fuera
    button:
        style "blank_button"
        xfill True yfill True
        action Hide("navigation_drawer")

    # Panel lateral con borde de acento del tema actual
    frame:
        at drawer_slide
        xalign 0.0 yalign 0.0
        xsize 460
        yfill True
        background Solid(themes[current_theme]["accent"])
        padding (6, 6)

        frame:
            background Solid(themes[current_theme]["bg"])
            padding (25, 30)
            xfill True
            yfill True

            $ guia_img, guia_msg = get_guia_greeting()
            $ guia_img = guia_img if renpy.loadable("images/guias/%s.png" % guia_img) else "images/guias/red.png"

            vbox:
                spacing 20

                # Encabezado con la mascota
                hbox:
                    spacing 15
                    add guia_img:
                        xysize (75, 75)
                        fit "contain"
                        yalign 0.5
                    vbox:
                        text "Daily Quest" size 34 bold True color "#FFD54F"
                        text "Tu compañero guía" size 22 color "#A5D6A7"

                # Globo de diálogo estilo cómic
                frame:
                    background Solid("#FFFFFF1A")
                    padding (15, 12)
                    xfill True

                    text "[guia_msg]" size 24 color "#FFFFFF" italic True

                null height 10

                # Opciones de navegación
                textbutton "📂 Mis Listas" action [Hide("navigation_drawer"), Hide("main_todo"), SetVariable("show_list_dropdown", False), Show("view_tasks_screen", transition=page_flip_or_none)] style "drawer_button" text_style "drawer_button_text"
                textbutton "➕ Nueva Tarea" action [Hide("navigation_drawer"), SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), SetVariable("show_rec_dropdown", False), SetVariable("show_add_task_list_dropdown", False), Show("add_task_screen", transition=page_flip_or_none)] style "drawer_button" text_style "drawer_button_text"
                textbutton "📅 Calendario" action [Hide("navigation_drawer"), SetVariable("pick_year", None), SetVariable("pick_month", None), SetVariable("cal_selected", None), Show("calendar_screen", transition=page_flip_or_none)] style "drawer_button" text_style "drawer_button_text"
                textbutton "🎨 Cambiar Mundo" action [Hide("navigation_drawer"), Show("theme_screen", transition=page_flip_or_none)] style "drawer_button" text_style "drawer_button_text"
                textbutton "📊 Mi Progreso" action [Hide("navigation_drawer"), Show("progress_screen", transition=page_flip_or_none)] style "drawer_button" text_style "drawer_button_text"

                null height 20

                textbutton "Cerrar" action Hide("navigation_drawer") style "drawer_button_close" text_style "drawer_button_close_text"

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

    # Saludo de la guía según el progreso
    $ guia_img_main, guia_msg_main = get_guia_greeting()
    $ guia_img_main = guia_img_main if renpy.loadable("images/guias/%s.png" % guia_img_main) else "images/guias/red.png"

    hbox:
        xalign 0.5
        ypos 330
        spacing 20

        add guia_img_main:
            xysize (110, 110)
            fit "contain"
            yalign 0.5

        frame:
            background Solid("#FFFFFF22")
            padding (20, 15)
            xmaximum 560

            text "[guia_msg_main]" style "todo_text" size 32 italic True

    # Acceso principal al panel lateral
    textbutton "☰ Menú" action Show("navigation_drawer") style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 520

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

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

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
                    $ rec_txt = recurrence_description(t)

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

                            if rec_txt:
                                text "Se repite: [rec_txt]" style "task_item" size 28 color "#B9F6CA"

                            hbox:
                                spacing 20
                                xalign 1.0

                                $ done_label = "Reabrir" if t["done"] else "Completar"
                                textbutton "[done_label]" action Function(complete_task, i):
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

        textbutton "↩" action Show("main_todo", transition=page_flip_or_none) style "todo_button_small" text_style "todo_button_small_text"
        textbutton "Agregar tarea" action [SetVariable("show_list_dropdown", False), SetVariable("new_task_list", current_list), SetVariable("new_task_list_locked", True), SetVariable("show_rec_dropdown", False), SetVariable("show_add_task_list_dropdown", False), Show("add_task_screen", transition=page_flip_or_none)] style "todo_button" text_style "todo_button_text"

    # Panel desplegable de listas (al final para que pinte encima de la lista)
    if show_list_dropdown:
        frame:
            background Solid(themes[current_theme]["accent"])
            padding (6, 6)
            xalign 0.5
            ypos 265
            xmaximum 560

            frame:
                background Solid(themes[current_theme]["bg"])
                padding (16, 16)
                xmaximum 548

                viewport:
                    xsize 500
                    ysize 380
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

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    $ t = tasks[i] if 0 <= i < len(tasks) else None

    frame:
        background Solid(themes[current_theme]["accent"])
        padding (6, 6)
        xalign 0.5
        yalign 0.4
        xmaximum 640

        frame:
            background Solid(themes[current_theme]["bg"])
            padding (24, 24)
            xmaximum 628

            vbox:
                spacing 14
                xalign 0.5

                text "Mover tarea a…" style "todo_text" size 40 xalign 0.5

                if t is None:
                    text "Esta tarea ya no existe." style "todo_text" xalign 0.5
                else:
                    viewport:
                        xsize 540
                        ysize 340
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

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    text "¿Qué quieres lograr?" style "todo_text" xalign 0.5 ypos 200

    hbox:
        xalign 0.5
        ypos 280
        spacing 16

        frame:
            background Solid("#00000040")
            padding (20, 15)
            xmaximum 600
            yminimum 90

            input:
                value VariableInputValue("new_title")
                length 40
                size 40
                color "#FFFFFF"
                xalign 0.0
                yalign 0.5

        textbutton "✓" action [Function(add_new_task, new_title, new_task_list, {"freq": new_rec_freq, "days": sorted(new_rec_days), "time": "%02d:%02d" % (new_rec_h, new_rec_m)} if new_rec_freq != "ninguna" else None), SetVariable("new_title", ""), SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), SetVariable("new_rec_freq", "ninguna"), SetVariable("new_rec_days", []), SetVariable("new_rec_h", 8), SetVariable("new_rec_m", 0), SetVariable("show_rec_dropdown", False), SetVariable("show_add_task_list_dropdown", False), Hide("add_task_screen", transition=page_flip_back_or_none)]:
            style "todo_button_small"
            text_style "todo_button_icon_text"
            yminimum 90
        textbutton "✕" action [SetVariable("new_title", ""), SetVariable("new_task_list", task_lists[0]), SetVariable("new_task_list_locked", False), SetVariable("new_rec_freq", "ninguna"), SetVariable("new_rec_days", []), SetVariable("new_rec_h", 8), SetVariable("new_rec_m", 0), SetVariable("show_rec_dropdown", False), SetVariable("show_add_task_list_dropdown", False), Hide("add_task_screen", transition=page_flip_back_or_none)]:
            style "todo_button_small"
            text_style "todo_button_icon_text"
            yminimum 90

    if new_task_list_locked:
        text "Lista: [new_task_list.capitalize()]" style "todo_text" xalign 0.5 ypos 430
    else:
        text "¿En qué lista?" style "todo_text" xalign 0.5 ypos 430

        $ list_arrow = " ▴" if show_add_task_list_dropdown else " ▾"
        textbutton "[new_task_list.capitalize()][list_arrow]" action ToggleVariable("show_add_task_list_dropdown"):
            style "todo_button"
            text_style "todo_button_text"
            xalign 0.5
            ypos 490
            xminimum 460
            yminimum 80

    text "¿Se repite?" style "todo_text" xalign 0.5 ypos 600

    $ freq = new_rec_freq
    $ time_y = 770 if freq == "diaria" else (850 if freq == "semanal" else 880)

    $ freq_label = {"ninguna": "Una vez", "diaria": "Diaria", "semanal": "Semanal", "mensual": "Mensual"}[new_rec_freq]
    $ rec_arrow = " ▴" if show_rec_dropdown else " ▾"
    textbutton "[freq_label][rec_arrow]" action ToggleVariable("show_rec_dropdown"):
        style "todo_button"
        text_style "todo_button_text"
        xalign 0.5
        ypos 650
        xminimum 460
        yminimum 80

    if freq == "semanal":
        hbox:
            xalign 0.5
            ypos 770
            spacing 12

            for wd in range(7):
                $ dbg = Frame(Solid("#FFD54F"), 12, 12) if wd in new_rec_days else Frame(Solid("#FFFFFF"), 12, 12)
                textbutton WD_SHORT_ES[wd].capitalize() action Function(toggle_new_rec_day, wd):
                    style "todo_button_rec"
                    text_style "todo_button_small_text"
                    xminimum 100
                    yminimum 58
                    background dbg

    if freq == "mensual":
        viewport:
            xalign 0.5
            ypos 770
            xsize 940
            ysize 96
            scrollbars "horizontal"
            draggable True
            mousewheel "horizontal"

            hbox:
                spacing 12

                for dd in range(1, 32):
                    $ dbg = Frame(Solid("#FFD54F"), 12, 12) if dd in new_rec_days else Frame(Solid("#FFFFFF"), 12, 12)
                    textbutton str(dd) action Function(toggle_new_rec_day, dd):
                        style "todo_button_rec"
                        text_style "todo_button_small_text"
                        xminimum 95
                        yminimum 62
                        background dbg

    if freq != "ninguna":
        $ hh = "%02d" % new_rec_h
        $ mm = "%02d" % new_rec_m
        hbox:
            xalign 0.5
            ypos time_y
            spacing 12

            text "Hora" style "todo_text" yalign 0.5
            textbutton "-" action Function(bump_new_rec_h, -1):
                style "todo_button_rec"
                text_style "todo_button_small_text"
                xminimum 90
                yminimum 62
            text "[hh]" style "todo_text" size 40 xminimum 100 textalign 0.5 yalign 0.5
            textbutton "+" action Function(bump_new_rec_h, 1):
                style "todo_button_rec"
                text_style "todo_button_small_text"
                xminimum 90
                yminimum 62
            text ":" style "todo_text" size 40 yalign 0.5
            textbutton "-" action Function(bump_new_rec_m, -5):
                style "todo_button_rec"
                text_style "todo_button_small_text"
                xminimum 90
                yminimum 62
            text "[mm]" style "todo_text" size 40 xminimum 100 textalign 0.5 yalign 0.5
            textbutton "+" action Function(bump_new_rec_m, 5):
                style "todo_button_rec"
                text_style "todo_button_small_text"
                xminimum 90
                yminimum 62

    # Panel desplegable de frecuencia (al final para que pinte encima)
    if show_rec_dropdown:
        frame:
            background Solid(themes[current_theme]["accent"])
            padding (6, 6)
            xalign 0.5
            ypos 745
            xmaximum 520

            frame:
                background Solid(themes[current_theme]["bg"])
                padding (16, 16)
                xmaximum 508

                vbox:
                    spacing 10
                    xalign 0.5

                    for f, flabel in [("ninguna", "Una vez"), ("diaria", "Diaria"), ("semanal", "Semanal"), ("mensual", "Mensual")]:
                        $ fbg = Frame(Solid("#FFD54F"), 12, 12) if f == new_rec_freq else Frame(Solid("#FFFFFF"), 12, 12)
                        textbutton flabel action [SetVariable("new_rec_freq", f), SetVariable("new_rec_days", []), SetVariable("show_rec_dropdown", False)]:
                            style "todo_button_rec_panel"
                            text_style "todo_button_small_text"
                            xminimum 400
                            background fbg

    # Panel desplegable de listas (al final para que pinte encima)
    if show_add_task_list_dropdown:
        frame:
            background Solid(themes[current_theme]["accent"])
            padding (6, 6)
            xalign 0.5
            ypos 575
            xmaximum 560

            frame:
                background Solid(themes[current_theme]["bg"])
                padding (16, 16)
                xmaximum 548

                viewport:
                    xsize 500
                    ysize 300
                    scrollbars "vertical"
                    mousewheel True
                    draggable True

                    vbox:
                        spacing 10
                        xalign 0.5

                        for lname in task_lists:
                            $ lbg3 = Frame(Solid("#FFD54F"), 12, 12) if lname == new_task_list else Frame(Solid("#FFFFFF"), 12, 12)
                            textbutton lname.capitalize() action [SetVariable("new_task_list", lname), SetVariable("show_add_task_list_dropdown", False)]:
                                style "todo_button"
                                text_size 32
                                xminimum 440
                                yminimum 70
                                background lbg3

################################################################################
## Pantalla: Cambiar tema
################################################################################

screen theme_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Elige tu mundo" style "todo_title" xalign 0.5 ypos 60

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        for theme_name in themes:
            textbutton theme_name.capitalize() action [SetVariable("current_theme", theme_name), Hide("theme_screen")] style "todo_button" text_style "todo_button_text"

    textbutton "↩" action Hide("theme_screen", transition=page_flip_back_or_none):
        style "todo_button_small"
        text_style "todo_button_small_text"
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Progreso
################################################################################

screen progress_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mi Progreso" style "todo_title" xalign 0.5 ypos 60

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

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

    textbutton "↩" action Hide("progress_screen", transition=page_flip_back_or_none):
        style "todo_button_small"
        text_style "todo_button_small_text"
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Popup de recompensa (fruta + guía)
################################################################################

screen reward_popup():
    zorder 100

    # Solo pinta si hay recompensa pendiente (al desmarcar no molesta)
    if last_reward:
        button:
            style "blank_button"
            xfill True yfill True
            action Hide("reward_popup")

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

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    $ t = tasks[i] if 0 <= i < len(tasks) else None

    if t is None:
        text "Esta tarea ya no existe." style "todo_text" xalign 0.5 yalign 0.45
        textbutton "↩" action Hide("task_detail_screen", transition=page_flip_back_or_none):
            style "todo_button_small"
            text_style "todo_button_small_text"
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
                                    button:
                                        style "blank_button"
                                        action [Function(toggle_subtask, i, j), Show("reward_popup")]
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
                                    xminimum 340
                                if valid_date(sdl):
                                    text date_tuple_to_string(sdl) style "subtask_text" size 28 color (sdc or "#81C784") xalign 0.5 xminimum 110
                                textbutton "Fecha" action Show("deadline_pick_screen", i=i, j=j, transition=page_flip_or_none):
                                    style "todo_button_detail"
                                    text_style "todo_button_small_text"
                                    xminimum 120
                                textbutton "✕" action Function(remove_subtask, i, j):
                                    style "todo_button_detail"
                                    text_style "todo_button_small_text"
                                    xminimum 90

        # Entrada para agregar subtarea
        hbox:
            xalign 0.5
            ypos 760
            spacing 16

            frame:
                background Solid("#00000040")
                padding (20, 15)
                xmaximum 560
                yminimum 90

                input:
                    value VariableInputValue("new_subtask")
                    length 60
                    size 40
                    color "#FFFFFF"
                    xalign 0.0
                    yalign 0.5

            textbutton "✓" action [Function(add_subtask, i, new_subtask), SetVariable("new_subtask", "")]:
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90
            textbutton "✕" action SetVariable("new_subtask", ""):
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90

        $ rec_txt = recurrence_description(t)
        if rec_txt:
            text "Se repite: [rec_txt]" style "todo_text" size 36 xalign 0.5 ypos 1000
            textbutton "Quitar repetición" action Function(clear_recurrence, i):
                style "todo_button_small"
                text_style "todo_button_small_text"
                xalign 0.5
                ypos 1070

        textbutton "↩" action Hide("task_detail_screen", transition=page_flip_back_or_none):
            style "todo_button_small"
            text_style "todo_button_small_text"
            xalign 0.5
            ypos 0.90

################################################################################
## Pantalla: Gestión de listas
################################################################################

screen lists_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mis Listas" style "todo_title" xalign 0.5 ypos 50

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

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
                                style "todo_button_small"
                                text_style "todo_button_small_text"
                                xminimum 190
                                yminimum 64
                            textbutton "✕" action Function(delete_task_list, lname):
                                style "todo_button_small"
                                text_style "todo_button_small_text"
                                xminimum 110
                                yminimum 64

    if renaming_list:
        text "Renombrando: [renaming_list]" style "todo_text" size 32 xalign 0.5 ypos 620

        hbox:
            xalign 0.5
            ypos 680
            spacing 16

            frame:
                background Solid("#00000040")
                padding (20, 15)
                xmaximum 560
                yminimum 90

                input:
                    value VariableInputValue("new_list_name")
                    length 30
                    size 36
                    color "#FFFFFF"
                    xalign 0.0
                    yalign 0.5

            textbutton "✓" action [Function(rename_task_list, renaming_list, new_list_name), SetVariable("renaming_list", None), SetVariable("new_list_name", "")]:
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90
            textbutton "✕" action [SetVariable("renaming_list", None), SetVariable("new_list_name", "")]:
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90
    else:
        text "Crea una nueva lista" style "todo_text" size 32 xalign 0.5 ypos 620

        hbox:
            xalign 0.5
            ypos 680
            spacing 16

            frame:
                background Solid("#00000040")
                padding (20, 15)
                xmaximum 560
                yminimum 90

                input:
                    value VariableInputValue("new_list_name")
                    length 30
                    size 36
                    color "#FFFFFF"
                    xalign 0.0
                    yalign 0.5

            textbutton "✓" action [Function(add_task_list, new_list_name), SetVariable("new_list_name", "")]:
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90
            textbutton "✕" action SetVariable("new_list_name", ""):
                style "todo_button_small"
                text_style "todo_button_icon_text"
                yminimum 90

    textbutton "↩" action Hide("lists_screen", transition=page_flip_back_or_none):
        style "todo_button_small"
        text_style "todo_button_small_text"
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Elegir fecha límite
################################################################################

screen deadline_pick_screen(i, j=None):
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Elige la fecha límite" style "todo_title" xalign 0.5 ypos 40

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 115

    hbox:
        xalign 0.5
        ypos 190
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "Hoy" action Function(set_pick_today) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "▶" action Function(month_move, 1) style "todo_button_nav" text_style "todo_button_nav_text"

    grid 7 1:
        xalign 0.5
        ypos 275
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                ysize 50
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

    textbutton "↩" action Hide("deadline_pick_screen", transition=page_flip_back_or_none):
        style "todo_button_small"
        text_style "todo_button_small_text"
        xalign 0.5
        ypos 0.90

################################################################################
## Pantalla: Calendario
################################################################################

screen calendar_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Mi Calendario" style "todo_title" xalign 0.5 ypos 40

    textbutton "☰" action Show("navigation_drawer"):
        style "todo_button_detail"
        text_style "todo_button_small_text"
        xpos 30
        ypos 30

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)
    $ sel = cal_selected if valid_date(cal_selected) else today_tuple()

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 115

    hbox:
        xalign 0.5
        ypos 190
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "Hoy" action Function(set_pick_today) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "▶" action Function(month_move, 1) style "todo_button_nav" text_style "todo_button_nav_text"

    grid 7 1:
        xalign 0.5
        ypos 270
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                ysize 50
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
                    $ n_dl = count_deadlines_on(dkey) + count_recurring_on(dkey)
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
            if is_recurrence_on(t, sel) and not any(x[0] == idx for x in sel_tasks):
                sel_tasks.append((idx, None, " (recurrente)"))

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
                            text "[dlabel2]" style "task_item" color c_status xmaximum 400
                            text "· [t.get('list', task_lists[0]).capitalize()]" style "task_item" size 30 color "#B9F6CA" xmaximum 180
                            textbutton "Abrir" action Show("task_detail_screen", i=idx, transition=page_flip_or_none):
                                style "todo_button_small"
                                text_style "todo_button_small_text"

    textbutton "↩" action Hide("calendar_screen", transition=page_flip_back_or_none):
        style "todo_button_small"
        text_style "todo_button_small_text"
        xalign 0.5
        ypos 0.90
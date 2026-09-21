################################################################################
## Pantallas del ToDo (estilos, menú principal, tareas, temas y progreso)
################################################################################

init offset = -1

default new_title = ""

################################################################################
## Estilos base amigables para niños
################################################################################

style todo_button:
    background Frame(Solid("#FFFFFF"), 12, 12)
    hover_background Frame(Solid("#E8F5E9"), 12, 12)
    padding (30, 20)
    xminimum 400
    yminimum 70
    size_group "todo_buttons"

style todo_button_text:
    size 32
    color "#212121"
    hover_color "#1B5E20"
    font "DejaVuSans.ttf"          # Cambia por la fuente que uses
    textalign 0.5
    xalign 0.5
    yalign 0.5

style todo_title:
    size 48
    color "#FFFFFF"
    bold True
    textalign 0.5
    outlines [(3, "#00000080", 0, 0)]

style todo_text:
    size 30
    color "#FFFFFF"
    textalign 0.5
    outlines [(2, "#00000060", 0, 0)]

style task_item:
    size 28
    color "#FFFFFF"
    outlines [(2, "#00000050", 0, 0)]

################################################################################
## Pantalla principal (Main Menu ToDo)
################################################################################

screen main_todo():
    tag menu
    modal True

    # Fondo según tema actual
    add Solid(themes[current_theme]["bg"])

    # Título
    text "¡Mis Proyectos!" style "todo_title" xalign 0.5 ypos 60

    # Nombre del niño
    text "Hola [player_name]!" style "todo_text" xalign 0.5 ypos 130

    # Contador de estrellas
    hbox:
        xalign 0.5
        ypos 190
        spacing 15
        text "★" size 40 color "#FFD700"
        text "[completed_tasks] estrellas" style "todo_text" size 28

    # Botones principales
    vbox:
        xalign 0.5
        yalign 0.55
        spacing 25

        textbutton "Ver mis tareas" action Show("view_tasks_screen") style "todo_button" text_style "todo_button_text"
        textbutton "Agregar nueva tarea" action Show("add_task_screen") style "todo_button" text_style "todo_button_text"
        textbutton "Cambiar tema" action Show("theme_screen") style "todo_button" text_style "todo_button_text"
        textbutton "Ver mi progreso" action Show("progress_screen") style "todo_button" text_style "todo_button_text"

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

    text "Mis Tareas" style "todo_title" xalign 0.5 ypos 50

    if not tasks:
        text "¡Todavía no tienes tareas!\nAgrega una para empezar tu aventura." style "todo_text" xalign 0.5 yalign 0.45
    else:
        viewport:
            xalign 0.5
            ypos 140
            xsize 900
            ysize 550
            scrollbars "vertical"
            mousewheel True
            draggable True

            vbox:
                spacing 18
                xalign 0.5

                for i, t in enumerate(tasks):
                    $ status = "✓  " if t["done"] else "○  "
                    $ color_status = "#A5D6A7" if t["done"] else "#FFFFFF"

                    frame:
                        background Solid("#FFFFFF22")
                        padding (25, 18)
                        xminimum 850

                        hbox:
                            spacing 20
                            text "[status][t['title']]" style "task_item" color color_status
                            if not t["done"]:
                                textbutton "Completar" action Function(complete_task, i):
                                    style "todo_button"
                                    text_size 24
                                    xminimum 160
                                    yminimum 50

    # Botones inferiores
    hbox:
        xalign 0.5
        ypos 0.90
        spacing 40

        textbutton "Volver" action Hide("view_tasks_screen") style "todo_button" text_style "todo_button_text"
        textbutton "Agregar tarea" action Show("add_task_screen") style "todo_button" text_style "todo_button_text"

################################################################################
## Pantalla: Agregar tarea
################################################################################

screen add_task_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    text "Nueva Tarea / Proyecto" style "todo_title" xalign 0.5 ypos 80

    text "¿Qué quieres lograr?" style "todo_text" xalign 0.5 ypos 180

    frame:
        background Solid("#00000040")
        padding (20, 15)
        xalign 0.5
        ypos 260
        xmaximum 700

        input:
            value VariableInputValue("new_title")
            length 40
            size 34
            color "#FFFFFF"
            xalign 0.0
            yalign 0.5

    hbox:
        xalign 0.5
        ypos 400
        spacing 50

        textbutton "Guardar":
            action [Function(add_new_task, new_title), SetVariable("new_title", ""), Hide("add_task_screen")]
            style "todo_button"
            text_style "todo_button_text"

        textbutton "Cancelar":
            action [SetVariable("new_title", ""), Hide("add_task_screen")]
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

    textbutton "Volver" action Hide("theme_screen") style "todo_button" text_style "todo_button_text":
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
        text "Estrellas ganadas: [completed_tasks]" style "todo_text" size 36

        # Barra de progreso simple
        fixed:
            xsize 600
            ysize 40
            xalign 0.5

            add Solid("#FFFFFF40")
            add Solid(themes[current_theme]["accent"]) xsize int(600 * percent / 100)

        text "[percent]%" style "todo_text" size 40

        if percent == 100 and total > 0:
            text "¡Eres un campeón de los proyectos!" style "todo_text" color "#FFD700"
        elif percent >= 50:
            text "¡Vas muy bien! Sigue así." style "todo_text"
        else:
            text "Cada tarea te acerca a tu meta." style "todo_text"

    textbutton "Volver" action Hide("progress_screen") style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 0.90
screen theme_screen():
    modal True

    add get_theme_bg()

    key "game_menu" action Function(quest_navigate)
    use quest_header("Elige tu mundo")

    viewport:
        xalign 0.5
        ypos 300
        xsize 920
        ysize 1390
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            xalign 0.5
            xsize 900
            spacing 30
            for theme_name in quest_stage_themes():
                textbutton quest_theme_label(theme_name) action [Function(select_quest_theme, theme_name), Hide("theme_screen")] style "todo_button" text_style "todo_button_text" xalign 0.5 selected current_theme == theme_name


################################################################################
## Pantalla: Progreso
################################################################################

screen progress_screen():
    modal True
    on "show" action Function(guide_progress)

    add get_theme_bg()

    key "game_menu" action Function(quest_navigate)
    use quest_header(_("Mis logros"))

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
            text "¡Completaste todas estas tareas!" style "todo_text" color "#FFD700"
        elif percent >= 50:
            text "¡Vas muy bien! Sigue así." style "todo_text"
        else:
            text "Cada tarea te acerca a tu meta." style "todo_text"

    use quest_guide


################################################################################
## Pantalla: Detalles de tarea (subtareas)
################################################################################

screen theme_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    key "game_menu" action Function(quest_navigate)
    use quest_header("Elige tu mundo")

    vbox:
        xalign 0.5
        yalign 0.5
        spacing 30

        for theme_name in themes:
            textbutton theme_name.capitalize() action [Function(select_quest_theme, theme_name), Hide("theme_screen")] style "todo_button" text_style "todo_button_text"


################################################################################
## Pantalla: Progreso
################################################################################

screen progress_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    key "game_menu" action Function(quest_navigate)
    use quest_header("Mis logros")

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

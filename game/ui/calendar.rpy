screen deadline_pick_screen(i, j=None):
    modal True

    add Solid(themes[current_theme]["bg"])

    key "game_menu" action Hide("deadline_pick_screen")
    text "Elige una fecha" style "todo_title" size 54 xalign 0.5 ypos 50
    textbutton "Volver" style "todo_button_small" text_style "todo_button_small_text" xpos 30 ypos 140 action Hide("deadline_pick_screen")

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 270

    hbox:
        xalign 0.5
        ypos 350
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "Hoy" action Function(set_pick_today) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "▶" action Function(month_move, 1) style "todo_button_nav" text_style "todo_button_nav_text"

    grid 7 1:
        xalign 0.5
        ypos 460
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                ysize 50
                text wd style "todo_text" size 34 xalign 0.5 yalign 0.5

    vbox:
        xalign 0.5
        ypos 530
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
                        action [d_action, Hide("deadline_pick_screen")]
                        background d_bg
                        style "cal_day"
                        text_style "cal_day_text"
                        text_color d_tcolor
                        xsize 120
                        ysize 100

    $ clear_dl_action = [Function(set_subtask_deadline, i, j, None) if j is not None else Function(set_deadline, i, None), Hide("deadline_pick_screen")]

    textbutton "Quitar fecha" action clear_dl_action style "todo_button" text_style "todo_button_text":
        xalign 0.5
        ypos 1250


################################################################################
## Pantalla: Calendario
################################################################################

screen calendar_screen():
    modal True

    add Solid(themes[current_theme]["bg"])

    key "game_menu" action Function(quest_navigate)
    use quest_header("Mi calendario")

    $ cy = pick_year if pick_year else today_tuple()[0]
    $ cm = pick_month if pick_month else today_tuple()[1]
    $ grid = month_grid(cy, cm)
    $ sel = cal_selected if valid_date(cal_selected) else today_tuple()

    text "[MONTHS_ES[cm-1]] [cy]" style "todo_text" size 42 bold True xalign 0.5 ypos 270

    hbox:
        xalign 0.5
        ypos 350
        spacing 30

        textbutton "◀" action Function(month_move, -1) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "Hoy" action Function(set_pick_today) style "todo_button_nav" text_style "todo_button_nav_text"
        textbutton "▶" action Function(month_move, 1) style "todo_button_nav" text_style "todo_button_nav_text"

    grid 7 1:
        xalign 0.5
        ypos 460
        xspacing 8

        for wd in WEEKDAYS_ES:
            fixed:
                xsize 120
                ysize 50
                text wd style "todo_text" size 34 xalign 0.5 yalign 0.01

    vbox:
        xalign 0.5
        ypos 530
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
                    $ n_dl = len(calendar_entries(dkey))
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
                        ysize 100

    $ sel_title = "Tareas del %d de %s" % (sel[2], MONTHS_ES[sel[1] - 1])

    text "[sel_title]" style "todo_text" size 36 xalign 0.5 ypos 1210

    $ sel_tasks = calendar_entries(sel)

    if not sel_tasks:
        text "No hay tareas para este día." style "todo_text" xalign 0.5 ypos 1280
    else:
        viewport:
            xalign 0.5
            ypos 1280
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

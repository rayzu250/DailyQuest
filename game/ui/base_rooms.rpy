screen quest_base_room(world, number):
    modal True
    zorder 185
    default board_status = "planned"
    key "game_menu" action Hide("quest_base_room")
    on "show" action Function(quest_pomodoro_sync_drafts, world)
    add get_theme_bg()
    if quest_base_available(world, number):
        $ role = quest_base_role(world, number)
        text QUEST_EXPEDITIONS[world]["upgrades"][number] style "todo_title" size 46 xalign 0.5 ypos 65 xmaximum 960 textalign 0.5
        textbutton "Volver a mi base" style "todo_button_small" xpos 60 ypos 180 action Hide("quest_base_room")
        viewport:
            xpos 60 ypos 320 xsize 960 ysize 1370
            mousewheel True
            draggable True
            scrollbars "vertical"
            vbox:
                xsize 900 spacing 24
                add ("images/base_rooms/" + role + ".png") xysize (300, 200) fit "contain" xalign 0.5
                text QUEST_BASE_DESCRIPTIONS[role] size 34 color "#FFFFFF" xmaximum 880
                if role == "planning":
                    grid 2 2:
                        spacing 16
                        for status, caption in [("planned", "Por hacer"), ("active", "En marcha"), ("paused", "En pausa"), ("finished", "Completado")]:
                            textbutton caption style "todo_button_small" xsize 420 text_size 32 selected board_status == status action SetScreenVariable("board_status", status)
                    $ indices = quest_base_indices(world, board_status)
                    if not indices:
                        text "No hay proyectos en esta sección." size 32 color "#FFFFFF"
                    for index in indices:
                        $ item = tasks[index]
                        frame:
                            background get_theme_panel()
                            padding (24, 22)
                            xfill True
                            vbox:
                                spacing 16
                                text item["title"] size 34 color "#FFFFFF" substitute False
                                text ("Prioridad: " + ("Alta", "Media", "Baja")[item.get("priority", 1)]) size 28 color "#D5EEE4"
                                textbutton "Abrir proyecto" style "todo_button_small" text_size 30 action Function(quest_base_task, item["id"])
                    text "Abre un proyecto para cambiar su prioridad, iniciarlo, pausarlo o completar sus pasos." size 28 color "#D5EEE4"
                elif role == "library":
                    $ indices = quest_base_indices(world, "finished")
                    if not indices:
                        text "Aquí aparecerán tus proyectos terminados." size 32 color "#FFFFFF"
                    for index in indices:
                        $ item = tasks[index]
                        $ plan = item["expedition"]
                        frame:
                            background get_theme_panel()
                            padding (24, 22)
                            xfill True
                            vbox:
                                spacing 16
                                text item["title"] size 34 color "#FFFFFF" substitute False
                                text ("Objetivo: " + (plan.get("goal") or "Sin objetivo escrito")) size 30 color "#FFFFFF" substitute False
                                text ("Aprendizaje: " + (plan.get("reflection") or "Puedes escribir una reflexión al abrir el proyecto.")) size 30 color "#D5EEE4" substitute False
                                if plan.get("notes"):
                                    text ("Notas: " + plan["notes"]) size 28 color "#FFFFFF" substitute False
                                textbutton "Consultar proyecto" style "todo_button_small" text_size 30 action Function(quest_base_task, item["id"])
                                textbutton "Crear proyecto similar" style "todo_button_small" text_size 30 action Function(quest_base_reuse, world, number, item["id"])
                else:
                    $ remaining = quest_base_rest_remaining(world)
                    $ started = world_progress.get(world, {}).get("rest_until")
                    if started:
                        if remaining:
                            text ("%02d:%02d" % (remaining // 60, remaining % 60)) size 80 color "#FFFFFF" xalign 0.5
                            text "Puedes dejar el teléfono a un lado. Al regresar, el tiempo estará actualizado." size 32 color "#FFFFFF"
                        else:
                            text "Tu pausa terminó. Retoma cuando te sientas listo." size 38 color "#FFFFFF"
                        textbutton ("Terminar pausa" if remaining else "Cerrar pausa") style "todo_button_small" action Function(quest_base_end_rest, world)
                    else:
                        for minutes in (5, 10, 15):
                            textbutton ("Descansar %d minutos" % minutes) style "todo_button_small" action Function(quest_base_start_rest, world, number, minutes)
                        # Pomodoro personalizado: N bloques de trabajo de X minutos
                        # y descansos de M minutos. Por defecto 4 / 25 / 5.
                        $ pom = quest_pomodoro_state(world)
                        if pom:
                            $ pstate = pom["state"]
                            $ phase_caption = ("Trabajo" if pstate["phase"] == "work" else "Descanso")
                            text ("Bloque %d de %d · %s" % (pstate["block"], pstate["blocks"], phase_caption)) size 36 color "#FFFFFF"
                            text ("%02d:%02d" % (pom["remaining"] // 60, pom["remaining"] % 60)) size 80 color "#FFFFFF" xalign 0.5
                            if pstate["phase"] == "work":
                                text "Concéntrate en un solo paso hasta que suene el descanso." size 30 color "#D5EEE4"
                            else:
                                text "Levántate, estira y bebe agua. Vuelve para el siguiente bloque." size 30 color "#D5EEE4"
                            textbutton "Terminar pomodoro" style "todo_button_small" action Function(quest_pomodoro_stop_action, world)
                        else:
                            hbox:
                                spacing 16
                                textbutton "−" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_blocks", -1)
                                text "Bloques: [pomodoro_blocks]" size 32 color "#FFFFFF"
                                textbutton "+" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_blocks", 1)
                            hbox:
                                spacing 16
                                textbutton "−" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_work", -5)
                                text "Trabajo: [pomodoro_work] min" size 32 color "#FFFFFF"
                                textbutton "+" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_work", 5)
                            hbox:
                                spacing 16
                                textbutton "−" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_rest", -1)
                                text "Descanso: [pomodoro_rest] min" size 32 color "#FFFFFF"
                                textbutton "+" style "todo_button_small" text_style "todo_button_small_text" action Function(quest_pomodoro_bump, "pomodoro_rest", 1)
                            textbutton "Empezar pomodoro" style "todo_button" text_style "todo_button_text" action Function(quest_pomodoro_start_action, world, number)
                    text "La música respeta tu volumen actual. Esta pausa no envía notificaciones al teléfono ni cambia tus misiones." size 28 color "#D5EEE4"
        if role == "rest":
            timer 1.0 repeat True action Function(quest_pomodoro_poll, world)
    else:
        timer 0.01 action Hide("quest_base_room")

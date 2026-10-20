transform quest_departure:
    xoffset -130 alpha 0.3
    ease 0.8 xoffset 0 alpha 1.0

transform quest_return:
    xoffset 130 alpha 0.3
    ease 0.8 xoffset 0 alpha 1.0

screen quest_expedition_controls(index, task):
    $ expedition = quest_task_expedition(task)
    frame:
        background get_theme_panel()
        padding (24, 22)
        xfill True
        vbox:
            spacing 18
            if expedition:
                $ world = expedition["world"]
                text (quest_theme_label(world) + " · " + quest_expedition_state(task)) size 30 color "#D5EEE4"
                hbox:
                    spacing 18
                    add quest_expedition_image(task) xysize (100, 130) fit "contain"
                    vbox:
                        spacing 12
                        text QUEST_EXPEDITIONS[world]["crew"][expedition["crew"]] size 34 color "#FFFFFF"
                        if expedition.get("goal"):
                            text expedition["goal"] size 30 color "#FFFFFF" xmaximum 700 substitute False
                if expedition["state"] == "planned" and not task["done"]:
                    text "Elige el mundo de esta misión:" size 28 color "#D5EEE4"
                    for world_key in QUEST_EXPEDITIONS:
                        textbutton quest_theme_label(world_key) style "todo_button_small" text_size 28 selected world == world_key action Function(quest_assign_expedition, index, world_key)
                    hbox:
                        spacing 14
                        for crew_index, crew_name in enumerate(QUEST_EXPEDITIONS[world]["crew"]):
                            textbutton crew_name style "todo_button_small" text_size 28 selected expedition["crew"] == crew_index action Function(quest_assign_expedition, index, crew=crew_index)
            else:
                text "Convierte este proyecto en una expedición." size 32 color "#FFFFFF"
            if not task["done"]:
                if not expedition or expedition["state"] == "planned":
                    textbutton "Iniciar misión" style "todo_button_small" text_size 32 action Function(quest_begin_expedition, index)
                elif expedition["state"] == "paused":
                    textbutton "Continuar misión" style "todo_button_small" text_size 32 action Function(quest_begin_expedition, index)
                else:
                    textbutton "Pausar misión" style "todo_button_small" text_size 30 action Function(quest_pause_expedition, index)
            textbutton "Plan y reflexión" style "todo_button_small" text_size 30 action Function(quest_open_plan, index)

screen quest_expedition_scene(task_id, returning=False):
    modal True
    zorder 180
    $ scene_task = next((task for task in tasks if task.get("id") == task_id), None)
    key "game_menu" action Hide("quest_expedition_scene")
    if scene_task and quest_task_expedition(scene_task) and quest_secondary():
        $ world = scene_task["expedition"]["world"]
        add QUEST_THEME_BACKGROUNDS[world]
        text ("Misión completada" if returning else "Misión en marcha") style "todo_title" xalign 0.5 ypos 70 size 52
        text scene_task["title"] size 38 color "#FFFFFF" xalign 0.5 ypos 170 xmaximum 930 textalign 0.5 substitute False
        add quest_expedition_image(scene_task):
            xalign 0.5 ypos 300 xysize (760, 850) fit "contain"
            if persistent.quest_motion == "normal":
                if returning:
                    at quest_return
                else:
                    at quest_departure
            elif persistent.quest_motion == "reduced":
                at quest_guide_fade
        frame:
            xpos 70 ypos 1190 xsize 940 padding (30, 28)
            background Solid(QUEST_THEME_ART[world]["panel"])
            vbox:
                spacing 20
                text QUEST_EXPEDITIONS[world]["return" if returning else "departure"] size 36 color "#FFFFFF" layout "subtitle"
                $ summary_steps = subtask_progress(scene_task)
                if summary_steps:
                    text ("Pasos completados: %d de %d" % summary_steps) size 32 color "#D5EEE4"
                text ("Base: " + QUEST_EXPEDITIONS[world]["home"]) size 30 color "#D5EEE4"
                if returning:
                    text "Revisa lo que funcionó en Plan y reflexión." size 28 color "#D5EEE4"
        textbutton "Continuar" style "todo_button" text_style "todo_button_text" xalign 0.5 ypos 1640 action Hide("quest_expedition_scene")
    else:
        timer 0.01 action Hide("quest_expedition_scene")

screen quest_expedition_plan(index):
    modal True
    zorder 180
    key "game_menu" action Hide("quest_expedition_plan")
    add get_theme_bg()
    text "Plan y reflexión" style "todo_title" xalign 0.5 ypos 65
    viewport:
        xpos 60 ypos 240 xsize 960 ysize 1290
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            xsize 900 spacing 30
            text "¿Qué quieres lograr?" style "todo_text" size 38
            use quest_text_field("expedition_goal_draft", "Objetivo del proyecto", 120)
            text "Prioridad" style "todo_text" size 36
            hbox:
                spacing 16
                for value, caption in [(0, "Alta"), (1, "Media"), (2, "Baja")]:
                    textbutton caption style "todo_button_small" text_size 30 selected tasks[index].get("priority", 1) == value action Function(quest_set_priority, index, value)
            text "¿Qué funcionó y qué cambiarías?" style "todo_text" size 36
            use quest_text_field("expedition_reflection_draft", "Reflexión opcional", 180)
            text "Puedes dejarlo vacío. Las listas pueden representar tus materias." style "todo_text" size 30
    hbox:
        xalign 0.5 ypos 1610 spacing 24
        textbutton "Guardar" style "todo_button_small" text_size 34 action Function(quest_save_plan, index)
        textbutton "Volver" style "todo_button_small" text_size 34 action Hide("quest_expedition_plan")

screen quest_world_hub():
    modal True
    default tab = "missions"
    default page = 0
    key "game_menu" action Function(quest_navigate)
    add get_theme_bg()
    use quest_header("Mis expediciones")
    if quest_secondary():
        hbox:
            xalign 0.5 ypos 285 spacing 14
            for value, caption in [("missions", "Mapa"), ("history", "Historial"), ("resources", "Mi base")]:
                textbutton caption style "todo_button_small" text_size 30 selected tab == value action [SetScreenVariable("tab", value), SetScreenVariable("page", 0)]
        if tab in ("missions", "history"):
            $ mission_indices = quest_expedition_indices(tab == "history")
            $ max_page = max(0, (len(mission_indices) - 1) // 4)
            $ visible_page = min(page, max_page)
            text ("Misiones: %d" % len(mission_indices)) style "todo_text" size 32 xalign 0.5 ypos 420
            if not mission_indices:
                text "Inicia una misión desde Ver pasos." style "todo_text" xalign 0.5 ypos 650 xmaximum 900
            else:
                # Cuatro nodos por página: objetivos amplios y sin animaciones simultáneas.
                grid 2 2:
                    xpos 65 ypos 500 spacing 26
                    for slot in range(4):
                        $ position = visible_page * 4 + slot
                        if position < len(mission_indices):
                            $ task_index = mission_indices[position]
                            $ mission = tasks[task_index]
                            button:
                                xsize 460 ysize 470
                                padding (24, 20)
                                background get_theme_panel()
                                action [Function(quest_navigate), Show("task_detail_screen", i=task_index)]
                                vbox:
                                    spacing 12
                                    add quest_expedition_image(mission) xysize (210, 220) fit "contain" xalign 0.5
                                    text mission["title"] size 32 color "#FFFFFF" xmaximum 412 layout "subtitle" substitute False
                                    text quest_expedition_state(mission) size 27 color "#D5EEE4"
                        else:
                            null width 460 height 470
                hbox:
                    xalign 0.5 ypos 1530 spacing 24
                    textbutton "Anterior" style "todo_button_small" text_size 28 sensitive visible_page > 0 action SetScreenVariable("page", visible_page - 1)
                    text ("%d / %d" % (visible_page + 1, max_page + 1)) size 30 color "#FFFFFF" yalign 0.5
                    textbutton "Siguiente" style "todo_button_small" text_size 28 sensitive visible_page < max_page action SetScreenVariable("page", visible_page + 1)
        else:
            $ world = quest_theme_key()
            $ earned = len(world_progress.get(world, {}).get("earned", []))
            $ unlocked = world_progress.get(world, {}).get("upgrades", [])
            viewport:
                xpos 60 ypos 440 xsize 970 ysize 1270
                mousewheel True
                draggable True
                scrollbars "vertical"
                vbox:
                    xsize 900 spacing 26
                    text QUEST_EXPEDITIONS[world]["home"] style "todo_title" size 46
                    add quest_reward_image(None, world) xysize (120, 120) fit "contain" xalign 0.5
                    text (QUEST_EXPEDITIONS[world]["resource"] + ": %d disponibles" % quest_world_balance(world)) style "todo_text" size 34
                    text ("Conseguidos: %d · Mejoras: %d de 3" % (earned, len(unlocked))) style "todo_text" size 30
                    text "Cada paso nuevo aporta un recurso. Elige una mejora por 3 recursos." style "todo_text" size 30
                    for number, caption in enumerate(QUEST_EXPEDITIONS[world]["upgrades"]):
                        frame:
                            background get_theme_panel()
                            padding (24, 24)
                            xfill True
                            vbox:
                                spacing 16
                                $ room_role = quest_base_role(world, number)
                                add ("images/base_rooms/" + room_role + ".png") xysize (180, 120) fit "contain"
                                text caption size 36 color "#FFFFFF"
                                text QUEST_BASE_DESCRIPTIONS[room_role] size 28 color "#D5EEE4"
                                if number in unlocked:
                                    text "✓ Disponible en tu base" size 30 color "#A9E8C4"
                                    textbutton "Entrar" style "todo_button_small" text_size 32 action Function(quest_base_open, world, number)
                                else:
                                    textbutton "Desbloquear · 3" style "todo_button_small" text_size 30 sensitive quest_world_balance(world) >= 3 action Function(quest_unlock_upgrade, world, number)
                    text "Tus recursos y mejoras se conservan al cambiar de etapa o mundo." style "todo_text" size 28
    else:
        text "Esta vista está disponible en Secundaria." style "todo_text" xalign 0.5 yalign 0.5

# Una sola intervención a la vez. El texto permanece para leerlo sin prisa.
default guide_message = "Elige una tarea o toca Ayuda para empezar."
default guide_pose = "guia_happy"
default guide_fruit = None
default guide_event_serial = 0
default guide_animated = False
default guide_session_greeted = False

init python:
    def guide_event(message, pose="guia_encouraging", fruit=None, celebrate=False):
        store.guide_message = message
        store.guide_pose = pose
        store.guide_fruit = fruit
        store.guide_event_serial += 1
        store.guide_animated = True
        # La preferencia del mezclador controla también las celebraciones.
        if celebrate and persistent.quest_guide_enabled:
            renpy.sound.play("audio/reward_ding.ogg")

    def guide_greet():
        if not store.guide_session_greeted:
            store.guide_session_greeted = True
            guide_event("¡Hola, %s! ¿Qué quieres hacer hoy?" % store.player_name, "guia_happy")

    def guide_help():
        guide_event(quest_profile()["help"], "guia_encouraging")

    def guide_progress():
        done = sum(1 for task in store.tasks if task.get("done"))
        guide_event("Has completado %d de %d tareas. Cada paso cuenta." % (done, len(store.tasks)), "guia_cheering")

    def guide_image():
        path = "images/guias/%s.png" % store.guide_pose
        if not renpy.loadable(path):
            path = "images/guias/red.png"
        # Encuadrar el personaje en pantalla sin modificar los PNG originales.
        return Crop((170, 22, 315, 331), path)

transform quest_guide_bounce:
    yoffset 0
    easein 0.20 yoffset -12
    easeout 0.20 yoffset 0
    easein 0.18 yoffset -6
    easeout 0.18 yoffset 0

transform quest_guide_fade:
    alpha 0.4
    linear 0.18 alpha 1.0

screen quest_guide():
    if persistent.quest_guide_enabled and "guide" in quest_profile()["features"]:
        frame:
            xpos 50 ypos 1460 xsize 980 ysize 210
            padding (18, 14)
            background Solid("#17352D")
            hbox:
                spacing 16
                # Cambiar de evento reinicia solo esta breve reacción, no el mensaje.
                for event_id in [guide_event_serial]:
                    add guide_image():
                        xysize (110, 130)
                        fit "contain"
                        if guide_animated and persistent.quest_motion == "normal":
                            at quest_guide_bounce
                        elif guide_animated and persistent.quest_motion == "reduced":
                            at quest_guide_fade
                    if guide_animated:
                        timer 1.2 action SetVariable("guide_animated", False)
                vbox:
                    xsize 590
                    spacing 4
                    text "Guía" size 28 bold True color "#FFD54F"
                    text guide_message size 30 color "#FFFFFF" layout "subtitle" substitute False
                vbox:
                    spacing 8
                    textbutton "Ayuda" style "todo_button_small" text_size 28 xminimum 130 yminimum 70 action Function(guide_help)
                    if guide_fruit:
                        add ("images/fruits/%s.png" % guide_fruit):
                            xysize (52, 52)
                            fit "contain"

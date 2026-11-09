# script.rpy
define e = Character("Guía", color="#4CAF50")

default player_name = "Amigo"
default completed_tasks = 0
default current_theme = "bosque"

# Placeholders visuales hasta que exista arte real
image bg_room = Solid("#1B5E20")
image guia happy = "images/guias/red.png"
image guia_happy = "images/guias/guia_happy.png"
image guia_encouraging = "images/guias/guia_encouraging.png"
image guia_cheering = "images/guias/guia_cheering.png"
image guia_star = "images/guias/guia_star.png"

transform guia_center:
    xalign 0.5
    yalign 1.0
    yoffset -240
    zoom 1.5

# Pequeño salto de alegría para la mascota Guía al lograr un objetivo
transform guia_happy_bounce:
    on show:
        xoffset -450 alpha 0.0
        easein 0.25 xoffset 0 alpha 1.0
    on hide:
        easeout 0.20 xoffset -450 alpha 0.0

# Entrar por la acción oficial para salir correctamente del contexto de menú.
label main_menu:
    $ renpy.run(Start())
    return

label start:
    $ quick_menu = False
    $ _game_menu_screen = None
    # El idioma elegido sobrevive al reinicio de la app.
    $ quest_apply_language()
    if restore_quest_data():
        jump main_menu_todo
    $ migrate_quest_data()
    $ quest_sync_theme_music()

    scene expression get_theme_bg()
    show expression Transform(guide_image(), xysize=(400, 600), fit="contain", xalign=0.5, yalign=0.65) as introduction_guide

    e "¡Hola! Soy tu guía. ¿Cómo te llamas?"
    call screen quest_text_editor("player_name", "¿Cómo te llamas?", 30, onboarding=True)
    $ player_name = player_name.strip() or "Amigo"
    $ save_quest_data()

    if quest_secondary():
        e "[player_name], prepara tu primer proyecto. Tú eliges el objetivo y el ritmo."
    else:
        e "¡Genial, [player_name]! Vamos a aprender a organizar tus proyectos de forma divertida."

    jump main_menu_todo

label main_menu_todo:
    $ quick_menu = False
    $ _game_menu_screen = None
    $ migrate_quest_data()
    $ quest_sync_theme_music()
    # Aviso de inicio (Fase 5): tareas de hoy / atrasadas, una vez por día.
    $ quest_maybe_show_startup_notices()
    call screen view_tasks_screen
    return

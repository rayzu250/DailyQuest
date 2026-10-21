# script.rpy
define e = Character("Guía", color="#4CAF50")

default player_name = "Amigo"
default completed_tasks = 0
default current_theme = "bosque"

# Preferencia antigua conservada únicamente por compatibilidad.
default persistent.page_flip_enabled = False

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

# Animación de estrella/fruta que aparece, sube y se desvanece (Pop-up de Dopamina)
transform reward_pop_up:
    anchor (0.5, 0.5)
    zoom 0.3 alpha 0.0
    parallel:
        easein 0.25 zoom 1.3 alpha 1.0
        easeout 0.15 zoom 1.0
    parallel:
        easeout 0.7 yoffset -80
    linear 0.3 alpha 0.0

# Pequeño salto de alegría para la mascota Guía al lograr un objetivo
transform guia_happy_bounce:
    xalign 0.5 yalign 1.0 yoffset -240 zoom 1.5
    easein 0.12 yoffset -275
    easeout 0.12 yoffset -240
    easein 0.08 yoffset -255
    easeout 0.08 yoffset -240

# Variante del salto para la guía en miniatura dentro del popup de recompensa
transform guia_reward_bounce:
    zoom 0.45
    easein 0.12 yoffset -40
    easeout 0.12 yoffset 0
    easein 0.08 yoffset -20
    easeout 0.08 yoffset 0

# Animación de entrada y salida suave para el panel lateral
transform drawer_slide:
    on show:
        xoffset -450 alpha 0.0
        easein 0.25 xoffset 0 alpha 1.0
    on hide:
        easeout 0.20 xoffset -450 alpha 0.0

init python:
    # Compatibilidad con llamadas antiguas: la navegación ya no aplica el efecto.
    def page_flip_or_none(old_widget=None, new_widget=None):
        return None

    def page_flip_back_or_none(old_widget=None, new_widget=None):
        return None

# Entrar por la acción oficial para salir correctamente del contexto de menú.
label main_menu:
    $ renpy.run(Start())
    return

label start:
    $ quick_menu = False
    $ _game_menu_screen = None
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
    call screen view_tasks_screen
    return

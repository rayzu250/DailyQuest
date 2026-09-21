# script.rpy
define e = Character("Guía", color="#4CAF50")

default player_name = "Amigo"
default completed_tasks = 0
default current_theme = "bosque"

# Placeholders visuales hasta que exista arte real
image bg_room = Solid("#1B5E20")
image guia happy = "images/guias/red.png"

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

label start:
    if not renpy.music.get_playing():
        play music "audio/Little_Notes_for_Big_Tasks.ogg" fadein 1.0

    scene bg_room
    show guia happy at guia_center

    e "¡Hola! Soy tu guía. ¿Cómo te llamas?"
    $ player_name = renpy.input("Escribe tu nombre:", default="Amigo")
    $ player_name = player_name.strip() or "Amigo"

    e "¡Genial, [player_name]! Vamos a aprender a organizar tus proyectos de forma divertida."

    jump main_menu_todo

label main_menu_todo:
    call screen main_todo
    return   
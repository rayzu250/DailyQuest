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
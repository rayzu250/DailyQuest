# Pantallas de aviso de la Fase 5. Imagen dedicada si el usuario la coloca
# en images/comandante/; en su defecto se usan poses del tema Comandante.

init python:
    def quest_startup_picture(custom, pose):
        # Imagen dedicada si existe; si no, una pose del tema Comandante.
        if renpy.loadable(custom):
            return custom
        fallback = "images/themes/comandante/%s.png" % pose
        if renpy.loadable(fallback):
            return fallback
        return "images/themes/comandante/guide.png"

screen quest_startup_overdue(count=0):
    modal True
    zorder 190
    add Solid("#0E131055")
    frame:
        xalign 0.5 yalign 0.5 xsize 900 padding (40, 36)
        background get_theme_panel()
        vbox:
            spacing 26
            xalign 0.5
            add quest_startup_picture("images/comandante/tareas_atrasadas.png", "pose_serious"):
                xysize (420, 420)
                fit "contain"
                xalign 0.5
            text ("Dejaste %d tareas sin terminar." % count):
                style "todo_text"
                size 42
                color "#FFFFFF"
                substitute False
                textalign 0.5
            text "Comandante no está contento. Hoy las retomamos, sin excusas.":
                size 30
                color "#D5EEE4"
                textalign 0.5
            hbox:
                spacing 22
                xalign 0.5
                textbutton _("Ver tareas") style "todo_button_small" text_style "todo_button_small_text" action [Function(quest_startup_close_all), SetVariable("task_filter", "all"), Function(quest_navigate)]
                textbutton _("Ahora no") style "todo_button_small" text_style "todo_button_small_text" action Hide("quest_startup_overdue")

screen quest_startup_due_today(count=0):
    modal True
    zorder 190
    add Solid("#0E131055")
    frame:
        xalign 0.5 yalign 0.5 xsize 900 padding (40, 36)
        background get_theme_panel()
        vbox:
            spacing 26
            xalign 0.5
            add quest_startup_picture("images/comandante/tareas_hoy.png", "pose_greeting"):
                xysize (420, 420)
                fit "contain"
                xalign 0.5
            text ("Hoy tienes %d tareas por completar." % count):
                style "todo_text"
                size 42
                color "#FFFFFF"
                substitute False
                textalign 0.5
            text "Un paso pequeño es suficiente para empezar.":
                size 30
                color "#D5EEE4"
                textalign 0.5
            hbox:
                spacing 22
                xalign 0.5
                textbutton _("Ver tareas") style "todo_button_small" text_style "todo_button_small_text" action [Function(quest_startup_close_all), SetVariable("task_filter", "today"), Function(quest_navigate)]
                textbutton _("Ahora no") style "todo_button_small" text_style "todo_button_small_text" action Hide("quest_startup_due_today")

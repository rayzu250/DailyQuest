# Consejos opcionales: el usuario decide qué leer y cuándo salir.
init python:
    QUEST_HELP = {
        "primaria": (
            ("Elegir una tarea", "Piensa en una cosa que quieras hacer hoy. Por ejemplo, preparar tu mochila.", "Elige una tarea para empezar. Las demás pueden esperar su turno."),
            ("Pasos pequeños", "Si una tarea parece grande, divídela. Para preparar tu mochila: guarda libros, guarda cuadernos y revisa tu estuche.", "Puedes agregar esos pasos como subtareas. Marca cada uno cuando lo termines."),
            ("Una cosa a la vez", "Elige un paso y dale tu atención. No necesitas hacer todo al mismo tiempo.", "Si no sabes cómo seguir, pide ayuda a una persona de confianza."),
            ("Descansar", "Si estás cansado, puedes hacer una pausa, estirarte o tomar agua.", "Descansar también cuenta. Vuelve cuando estés listo; no es una carrera."),
            ("Revisar tu día", "Mira lo que hiciste hoy. ¿Qué paso te gustó más?", "Si algo quedó pendiente, puedes intentarlo después. Tu esfuerzo vale aunque no termines todo.")
        ),
        "secundaria": (
            ("Agile: ajustar el plan", "Agile propone avanzar en partes pequeñas, revisar el resultado y adaptar el plan. No significa hacerlo todo más rápido.", "Para una exposición: prepara un borrador, pide comentarios y mejora una sección. Ajusta los pasos de tu misión con lo que aprendiste."),
            ("Kanban: ver el trabajo", "Organiza tu trabajo en Por hacer, En proceso y Terminado. Limitar lo que tienes en proceso ayuda a terminar antes de empezar más cosas.", "Prueba con una tarea en proceso. DailyQuest aún no tiene un tablero Kanban: puedes dibujarlo en papel y usar tus tareas como referencia."),
            ("Kaizen: mejorar poco a poco", "Kaizen significa mejora continua. Observa qué te cuesta y prueba un cambio pequeño, sin exigirte perfección.", "Si olvidas materiales, prueba revisar tu mochila por la tarde durante unos días. Después decide si ese cambio te ayuda o necesitas otro."),
            ("Elegir prioridades", "Revisa qué tiene una fecha cercana y qué es importante para tu objetivo. No todo necesita resolverse hoy.", "Si mañana entregas un trabajo, elige primero un paso de ese trabajo. Si hay demasiados pendientes, pide apoyo para ajustar el plan."),
            ("Tiempo y pausas", "Calcula cuánto puede tomar un paso y deja espacio para descansar. Una estimación es una idea, no una promesa.", "Prueba un bloque breve que te resulte cómodo. Al terminar, revisa si necesitas más tiempo o dividir el paso. Equivocarte al calcular es normal."),
            ("Revisión semanal", "Pregúntate: ¿qué funcionó?, ¿qué fue difícil?, ¿qué puedo cambiar la próxima semana?", "Elige una sola mejora para probar. Puedes conversar con un docente o tu familia; la organización debe ayudarte, no añadir presión.")
        ),
    }

    def quest_help_topics():
        return QUEST_HELP["secundaria" if quest_secondary() else "primaria"]

screen quest_help():
    modal True
    zorder 190
    default topic = None
    default tip = 0
    key "game_menu" action Hide("quest_help")
    add get_theme_options_bg()
    text "Ayuda para organizarte" size 50 bold True color "#FFFFFF" xalign 0.5 ypos 50
    textbutton "Volver al juego" style "quest_option_button" xpos 50 ypos 140 action Hide("quest_help")
    viewport:
        xpos 50 ypos 280 xsize 980 ysize 1500
        mousewheel True
        draggable True
        scrollbars "vertical"
        vbox:
            xsize 910
            spacing 26
            if topic is None:
                text "Elige un consejo. Puedes leerlo a tu ritmo." style "quest_option_text"
                for index, entry in enumerate(quest_help_topics()):
                    textbutton entry[0] style "quest_option_button" action [SetScreenVariable("topic", index), SetScreenVariable("tip", 0)]
            else:
                $ entry = quest_help_topics()[min(topic, len(quest_help_topics()) - 1)]
                add guide_image() xysize (260, 280) fit "contain" xalign 0.5
                text entry[0] style "quest_option_heading"
                frame:
                    xfill True
                    padding (28, 28)
                    background get_theme_panel()
                    text entry[tip + 1] size 40 color "#FFFFFF"
                textbutton ("Ver ejemplo" if tip == 0 else "Leer consejo") style "quest_option_button" action SetScreenVariable("tip", 1 - tip)
                textbutton "Otro tema de ayuda" style "quest_option_button" action SetScreenVariable("topic", None)

# Ejecutar con --savedir tests/runtime-saves para no tocar datos del usuario.
testsuite quest:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/"), "Usa --savedir tests/runtime-saves"
        run Jump("main_menu_todo")
        # El `call screen` necesita una interacción para colocar la pantalla;
        # los asserts de pantalla pueden fallar si se comprueban en el mismo fotograma.
        pause 1.0
        assert screen "view_tasks_screen"
        python:
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.completed_tasks = 0
            store.new_title = ""
            store.new_subtask = ""
            store.new_list_name = ""
            store.renaming_list = None
            store.task_filter = "all"
            persistent.quest_document = None
            # Aislamiento hermético: etapas y mundos personalizados del jugador
            # real nunca deben influir en la suite.
            persistent.school_stage = "primaria"
            persistent.quest_document_backup = None
            store.world_progress = {}
            store.stage_themes = {}
            store.current_theme = "bosque"
            # El idioma de las pruebas es siempre el original: un cambio de
            # idioma persistido no puede envenenar futuros runs.
            persistent.quest_language = "es"
            quest_apply_language()

    testcase data_integrity:
        python:
            assert not valid_date((2026, 2, 30))
            assert valid_date((2028, 2, 29))
            assert not valid_date((2026, "2", 1))
            monthly = {"recurrence": {"freq": "mensual", "days": [31]}}
            assert next_occurrence(monthly, (2028, 2, 1)) == (2028, 2, 29)
            assert next_occurrence({"recurrence": {"freq": "semanal", "days": []}}, (2026, 1, 1)) is None
            add_new_task("Leer", recurrence={"freq": "diaria", "days": [], "time": ""})
            add_subtask(0, "Una página")
            complete_task(0)
            assert len(tasks) == 2, ("copia recurrente", len(tasks), [t["title"] for t in tasks])
            complete_task(0)
            complete_task(0)
            assert len(tasks) == 2 and completed_tasks == 1, ("recompletar", len(tasks), completed_tasks)
            assert tasks[0]["next_task_id"] == tasks[1]["id"], ("next_id", tasks[0].get("next_task_id"), tasks[1].get("id"))
            assert len(calendar_entries(tasks[1]["deadline"])) == 1, ("calendario", tasks[1].get("deadline"))
            # El globo del calendario es la misma lista que el día abre.
            assert count_deadlines_on(tuple(tasks[1]["deadline"])) == 1
            assert count_deadlines_on(tuple(tasks[1]["deadline"])) == len(calendar_entries(tuple(tasks[1]["deadline"])))
            add_task_list("Escuela")
            move_task(1, "Escuela")
            before_title_change = quest_document()
            assert rename_task(1, "Leer cada día")
            assert tasks[1]["title"] == "Leer cada día"
            assert tasks[1]["id"] == before_title_change["tasks"][1]["id"]
            assert tasks[1]["recurrence"] == before_title_change["tasks"][1]["recurrence"]
            assert tasks[1]["deadline"] == before_title_change["tasks"][1]["deadline"]
            assert not rename_task(1, "   ") and tasks[1]["title"] == "Leer cada día"
            rename_task_list("Escuela", "Colegio")
            assert tasks[1]["list"] == "Colegio"
            delete_task_list("Colegio")
            assert tasks[1]["list"] == "General"
            migrate_quest_data()
            migrate_quest_data()
            before = quest_document()
            migrate_quest_data()
            assert quest_document() == before, (quest_document(), before)
            save_quest_data()
            store.tasks = []
            _r = restore_quest_data()
            assert _r, "restore falló"
            assert quest_document() == before, ("post-restore", quest_document(), before)
            store.tasks = [{"title": "Antigua", "done": False, "priority": 1}]
            migrate_quest_data()
            assert tasks[0]["id"] and tasks[0]["subtasks"] == []

    testcase long_names:
        python:
            _long_title = "T" * 120
            add_new_task(_long_title)
            assert tasks[0]["title"] == _long_title, ("title", len(tasks[0]["title"]))
            add_subtask(0, "p" * 120)
            assert tasks[0]["subtasks"][0]["text"] == "p" * 120, ("subtask", len(tasks[0]["subtasks"][0]["text"]))
            save_quest_data()
            migrate_quest_data()
            assert quest_document()["tasks"][0]["title"] == _long_title

    testcase long_names_editor:
        # La UI real debe aceptar más de los ~34 caracteres que recortaba
        # pixel_width (bug detectado en Android). 60 reales superan ese tope
        # con margen y no dependen del límite del modelo.
        python:
            _test.timeout = 30.0
        click "Agregar tarea"
        assert screen "add_task_screen"
        screenshot "long-names-add-screen"
        click "Toca para escribir…"
        assert screen "quest_text_editor"
        type "Tarea de prueba con nombre realmente largo para el editor"
        screenshot "long-names-editor"
        click "Listo"
        click "Guardar tarea"
        assert screen "view_tasks_screen"
        python:
            _typed = "Tarea de prueba con nombre realmente largo para el editor"
            # save_task_form vacía el borrador al guardar: se valida la tarea.
            assert len(tasks) == 1, ("guardada", len(tasks))
            assert tasks[0]["title"] == _typed, ("titulo", tasks[0]["title"], len(tasks[0]["title"]))

    testcase document_safety:
        python:
            saved_document = quest_document()
            store.tasks = []
            # Un documento ilegible nunca rompe el arranque ni lanza excepción.
            for broken in ({}, {"version": 3},
                           {"version": 1, "tasks": {}},
                           {"version": 2, "tasks": "x", "lists": []},
                           {"version": 2, "tasks": [], "lists": []}):
                persistent.quest_document = broken
                assert not restore_quest_data()
                assert persistent.quest_document_backup == broken
            # Tareas ilegibles se descartan sin perder el resto.
            persistent.quest_document = {"version": 2,
                "tasks": [1, {"title": "Renombrada"}], "lists": [7, "General"],
                "stage": "inventado"}
            assert restore_quest_data()
            assert [task["title"] for task in tasks] == ["Renombrada"]
            assert task_lists == ["General"] and persistent.school_stage == "primaria"
            # El último documento ilegible sigue disponible en la copia.
            assert persistent.quest_document_backup == {"version": 2, "tasks": [], "lists": []}
            # Vuelta al estado correcto de la suite.
            persistent.quest_document = saved_document
            assert restore_quest_data()
            persistent.quest_document_backup = None
        run Hide("notify")

    testcase calendar_single_source:
        python:
            # Estas tareas de calibración no deben sobrescribir el documento
            # que quest_restore espera encontrar de un run anterior.
            # Normalizar antes del snapshot: save_quest_data() vuelve a
            # normalizar y añadiría stage_themes, rompiendo la comparación.
            migrate_quest_data()
            saved_document = quest_document()
            store.tasks = []
            add_new_task("Pagar la luz")
            add_subtask(0, "Revisar la factura")
            set_subtask_deadline(0, 0, (2031, 3, 15))
            day = (2031, 3, 15)
            assert count_deadlines_on(day) == len(calendar_entries(day)) == 1
            toggle_subtask(0, 0)
            # Los pasos completados no inflan el contador del día.
            assert count_deadlines_on(day) == len(calendar_entries(day)) == 0
            assert len(tasks) == 1
            persistent.quest_document = saved_document
            assert restore_quest_data()
            # Deja el documento coherente tras la calibración; el testcase
            # text_and_navigation es ahora el último y produce el estado
            # que quest_restore hereda en su propio proceso.
            save_quest_data()
            assert quest_document() == saved_document

    testcase calendar_open_task:
        python:
            add_new_task("Revisar el calendario")
            set_deadline(0, today_tuple())
            assert len(calendar_entries(today_tuple())) == 1
        click "Menú"
        click "Calendario"
        assert screen "calendar_screen"
        # Regresión: "Abrir" pasaba una transición que devolvía None y rompía
        # la interacción al instanciarla.
        click "Abrir"
        assert screen "task_detail_screen"
        screenshot "calendar-open"

    testcase delete_task:
        # El testcase anterior deja abiertos el calendario y el detalle:
        # ocultarlos antes de reordenar la lista evita clics perdidos.
        run Hide("task_detail_screen")
        run Hide("calendar_screen")
        pause 0.5
        python:
            store.tasks = []
            store.completed_tasks = 0
            add_new_task("Regar jardín")
            add_new_task("Contar estrellas")
            assert len(tasks) == 2
            # La mutación de store.tasks no reinicia la interacción: sin un
            # restart la lista de foco queda congelada y el click falla.
            renpy.restart_interaction()
        pause 1.0
        click "Contar estrellas"
        assert screen "task_detail_screen"
        click "Eliminar tarea"
        assert screen "confirm"
        screenshot "confirm-delete"
        click "Sí"
        assert not screen "task_detail_screen"
        python:
            assert [t["title"] for t in tasks] == ["Regar jardín"]
            # Un índice que ya no existe se ignora sin romper nada.
            assert not delete_task(7) and len(tasks) == 1
            # Los logros de vida no se quitan al borrar una tarea completada.
            complete_task(0)
            assert completed_tasks == 1
            assert delete_task(0) and not tasks
            assert completed_tasks == 1, ("logros vitales", completed_tasks)

    testcase close_series:
        run Hide("task_detail_screen")
        pause 0.5
        python:
            store.tasks = []
            store.completed_tasks = 0
            add_new_task("Meditar", recurrence={"freq": "diaria", "days": [], "time": ""})
            complete_task(0)
            assert len(tasks) == 2, ("copia del día siguiente", len(tasks))
            complete_task(1)
            assert len(tasks) == 3, ("la copia también genera la suya", len(tasks))
            assert tasks[0]["next_task_id"] == tasks[1]["id"]
            assert tasks[1]["next_task_id"] == tasks[2]["id"]
            # La familia completa se alcanza desde cualquier copia.
            assert [t["id"] for t in quest_series_members(tasks[2])] == [t["id"] for t in tasks]
            assert len(quest_series_members(tasks[1])) == 3
        click "Meditar"
        assert screen "task_detail_screen"
        click "Cerrar serie"
        assert screen "confirm"
        click "Sí"
        assert not screen "task_detail_screen"
        python:
            assert not tasks, "la cadena completa desapareció"
            assert completed_tasks == 2, ("logros de la serie", completed_tasks)

    testcase language_toggle:
        run Hide("task_detail_screen")
        pause 0.5
        python:
            # Blindaje: si este caso aborta a mitad, el siguiente run
            # arranca igual en el idioma original.
            persistent.quest_language = "es"
            quest_apply_language()
        click "Menú"
        click "Opciones"
        assert screen "quest_options"
        click "Idioma: Español / English"
        python:
            assert renpy.game.preferences.language == "english", ("idioma", renpy.game.preferences.language)
        click "Language: Español / English"
        python:
            assert renpy.game.preferences.language is None, ("idioma revertido", renpy.game.preferences.language)
        click "Volver"

    testcase pending_filter_and_order:
        # "Pendientes" sustituye a "7 días": muestra solo las tareas abiertas.
        python:
            add_new_task("Tarea abierta")
            add_new_task("Tarea cerrada")
            tasks[1]["done"] = True
        click "Pendientes"
        python:
            assert store.task_filter == "open", ("filtro", store.task_filter)
            assert [tasks[i]["title"] for i in visible_task_indices()] == ["Tarea abierta"], \
                ("pendientes", [tasks[i]["title"] for i in visible_task_indices()])
        click "Todas"
        python:
            assert store.task_filter == "all", ("filtro", store.task_filter)
            assert len(visible_task_indices()) == 2, ("todas", len(visible_task_indices()))
            assert {tasks[i]["title"] for i in visible_task_indices()} == {"Tarea abierta", "Tarea cerrada"}
            # Orden ascendente A→Z sin acentos; las completadas al final.
            tasks[0]["title"] = "Zeta"
            tasks[0]["subtasks"] = []
            add_subtask(0, "Paso Z")
            add_subtask(0, "Paso A")
            add_new_task("Árbol")
            add_new_task("Alfa")
            tasks[1]["done"] = True
            _orden = [tasks[i]["title"] for i in visible_task_indices()]
            assert _orden == ["Alfa", "Árbol", "Zeta", "Tarea cerrada"], ("orden", _orden)
            # Los pasos de Zeta conservan su orden manual.
            _pasos = [s["text"] for s in tasks[0]["subtasks"]]
            assert _pasos == ["Paso Z", "Paso A"], ("pasos", _pasos)

    testcase mi_base_button:
        # El botón "Mi base" de Mis tareas abre el hub de expediciones en
        # la pestaña Mi base (recursos), no la pantalla de estadísticas.
        python:
            quest_setting("school_stage", "secundaria")
            renpy.restart_interaction()
        pause 0.5
        click "Mi base"
        assert screen "quest_world_hub"
        python:
            _hub = renpy.get_screen("quest_world_hub")
            assert _hub.scope["hub_tab"] == "resources", ("tab", _hub.scope["hub_tab"])
        screenshot "mi-base-tab"
        # Las pestañas siguen respondiendo dentro del hub.
        click "Mapa"
        python:
            _hub = renpy.get_screen("quest_world_hub")
            assert _hub.scope["hub_tab"] == "missions", ("tab mapa", _hub.scope["hub_tab"])
        click "Mi base"
        python:
            _hub = renpy.get_screen("quest_world_hub")
            assert _hub.scope["hub_tab"] == "resources", ("tab base", _hub.scope["hub_tab"])
        run Function(quest_navigate)

    testcase text_and_navigation:
        click "Agregar tarea"
        assert screen "add_task_screen"
        click "Toca para escribir…"
        assert screen "quest_text_editor"
        type "Preparar mochila"
        screenshot "text-editor"
        click "Listo"
        assert not screen "quest_text_editor"
        python:
            assert new_title == "Preparar mochila"
            assert renpy.get_editable_input_value()[0] is None
        click "Guardar tarea"
        assert screen "view_tasks_screen"
        python:
            assert len(tasks) == 1
        screenshot "tasks"
        click "Ver pasos"
        click "Renombrar tarea"
        assert screen "rename_task_screen"
        click "Toca para escribir…"
        type "Preparar mochila escolar"
        click "Listo"
        click "Guardar nombre"
        assert not screen "rename_task_screen"
        python:
            assert tasks[0]["title"] == "Preparar mochila escolar"
        click "Toca para escribir…"
        type "Guardar libros"
        click "Cancelar"
        python:
            assert new_subtask == ""
        click "Toca para escribir…"
        type "Guardar libros"
        click "Listo"
        click "Agregar paso"
        python:
            assert len(tasks[0]["subtasks"]) == 1
        screenshot "steps"
        click "Menú"
        click "Mis listas"
        assert not screen "task_detail_screen"
        click "Toca para escribir…"
        type "Escuela"
        click "Listo"
        click "Guardar lista"
        python:
            assert "Escuela" in task_lists
        screenshot "lists"
        click "Menú"
        click "Calendario"
        assert screen "calendar_screen"
        screenshot "calendar"
        click "Menú"
        click "Cambiar mundo"
        click "Océano"
        python:
            assert current_theme == "océano"
        click "Menú"
        click "Mi base"
        assert screen "progress_screen"
        screenshot "progress"
        click "Menú"
        click "Nueva tarea"
        click "Repetir esta tarea…"
        click "Elegir días del mes"
        screenshot "recurrence"

testcase quest_restore:
    python:
        assert "runtime-saves" in config.savedir.replace("\\", "/")
        assert restore_quest_data()
        assert tasks[0]["title"] == "Preparar mochila"
        assert tasks[0]["subtasks"][0]["text"] == "Guardar libros"
        assert "Escuela" in task_lists
        assert current_theme == "océano"

# Ejecutar con --savedir tests/runtime-saves para no tocar datos del usuario.
testsuite quest:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/"), "Usa --savedir tests/runtime-saves"
        run Jump("main_menu_todo")
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
            assert len(tasks) == 2
            complete_task(0)
            complete_task(0)
            assert len(tasks) == 2 and completed_tasks == 1
            assert tasks[0]["next_task_id"] == tasks[1]["id"]
            assert len(calendar_entries(tasks[1]["deadline"])) == 1
            add_task_list("Escuela")
            move_task(1, "Escuela")
            rename_task_list("Escuela", "Colegio")
            assert tasks[1]["list"] == "Colegio"
            delete_task_list("Colegio")
            assert tasks[1]["list"] == "General"
            before = quest_document()
            migrate_quest_data()
            migrate_quest_data()
            assert quest_document() == before, (quest_document(), before)
            save_quest_data()
            store.tasks = []
            assert restore_quest_data()
            assert quest_document() == before, (quest_document(), before)
            store.tasks = [{"title": "Antigua", "done": False, "priority": 1}]
            migrate_quest_data()
            assert tasks[0]["id"] and tasks[0]["subtasks"] == []

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
        click "Mis logros"
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

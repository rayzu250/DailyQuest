# Validar el cambio de título sin tocar partidas personales.
testsuite rename_task:
    testcase preserve_task_data:
        python:
            assert "runtime-saves" in config.savedir.replace("\\\\", "/")
            _test.timeout = 20.0
        run Jump("main_menu_todo")
        run Function(quest_navigate)
        python:
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            add_new_task("Preparar exposición", recurrence={"freq": "semanal", "days": [0, 2], "time": "17:30"})
            task = tasks[0]
            task["deadline"] = (2026, 11, 4)
            task["time"] = "17:30"
            task["reminder"] = True
            add_subtask(0, "Investigar el tema")
            original_id = task["id"]
            original_recurrence = dict(task["recurrence"])
            original_step_id = task["subtasks"][0]["id"]
        run Show("task_detail_screen", i=0)
        click "Renombrar tarea"
        assert screen "rename_task_screen"
        click "Toca para escribir…"
        type "Exposición de ciencias"
        click "Listo"
        click "Guardar nombre"
        python:
            assert not renpy.get_screen("rename_task_screen")
            renamed = tasks[0]
            assert renamed["title"] == "Exposición de ciencias"
            assert renamed["id"] == original_id
            assert renamed["deadline"] == (2026, 11, 4)
            assert renamed["recurrence"] == original_recurrence
            assert renamed["time"] == "17:30" and renamed["reminder"]
            assert renamed["subtasks"][0]["id"] == original_step_id
            saved = quest_document()
            store.tasks = []
            assert restore_quest_data() and quest_document() == saved
            task_title_draft = "   "
            assert not rename_task(0, task_title_draft)
            assert tasks[0]["title"] == "Exposición de ciencias"
            _test.timeout = 5.0

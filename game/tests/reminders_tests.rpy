testsuite reminders:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
        run Jump("main_menu_todo")
        python:
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.completed_tasks = 0

    testcase schedules:
        python:
            store.tasks = [{"title": "Antigua", "done": False, "recurrence": {"freq": "diaria", "days": [], "time": "09:30"}}]
            migrate_quest_data()
            assert quest_task_time(tasks[0]) == "09:30" and not tasks[0]["reminder"]
            assert quest_reminder_payload() == []
            save_task_reminder(0, True, 9, 30, True)
            assert quest_reminder_payload()[0]["hour"] == 9
            set_recurrence(0, "diaria", [], "10:15")
            assert quest_task_time(tasks[0]) == "10:15"
            save_task_reminder(0, True, 9, 30, True)
            complete_task(0)
            assert len(quest_reminder_payload()) == 1
            assert quest_reminder_payload()[0]["id"] == tasks[1]["id"]
            assert tasks[1]["time"] == "09:30" and tasks[1]["reminder"]
            complete_task(0)
            assert len(quest_reminder_payload()) == 1
            save_task_reminder(1, True, 10, 0, False)
            assert quest_reminder_payload() == []
            store.tasks = []
            add_new_task("Una vez")
            save_task_reminder(0, True, 10, 0, True)
            assert not tasks[0]["reminder"]
            set_deadline(0, (2030, 1, 1))
            save_task_reminder(0, True, 10, 0, True)
            assert quest_reminder_payload()[0]["start"] == "2030-01-01"
            saved = quest_document()
            store.tasks = []
            assert restore_quest_data() and quest_document() == saved
            complete_task(0)
            assert quest_reminder_payload() == []
            complete_task(0)
            set_deadline(0, None)
            assert not tasks[0]["reminder"] and quest_reminder_payload() == []

    testcase schedule_editor:
        python:
            add_new_task("Leer un cuento", recurrence={"freq": "diaria", "days": [], "time": ""})
        run Show("task_detail_screen", i=0)
        click "Hora y recordatorio"
        click "Asignar una hora"
        click "Hora +"
        click "Minuto +"
        click "Recordarme en el teléfono"
        screenshot "reminder-editor"
        click "Guardar horario"
        python:
            assert tasks[0]["time"] == "09:01" and tasks[0]["reminder"]
        click "Hora y recordatorio"
        click "Hora +"
        click "Cancelar"
        python:
            assert tasks[0]["time"] == "09:01"

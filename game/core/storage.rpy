# El documento persistente es el último estado confirmado; store es su copia de trabajo.
default persistent.quest_document = None
# Copia de un documento ilegible, conservada para su análisis.
default persistent.quest_document_backup = None

init -2 python:
    import uuid as _quest_uuid
    import builtins as _quest_builtins
    import json as _quest_json
    import functools as _quest_functools

    def new_quest_id():
        return _quest_uuid.uuid4().hex

    def migrate_quest_data():
        # Las partidas antiguas pueden contener el catálogo anterior de cuatro mundos.
        for name, art in QUEST_THEME_ART.items():
            store.themes.setdefault(name, {"bg": art["panel"][:7], "accent": art["selection"], "text": "#FFFFFF"})
        if store.current_theme not in QUEST_THEME_ART:
            store.current_theme = "bosque"
        quest_normalize_stage_theme()
        if not store.task_lists:
            store.task_lists = ["General"]
        for task in store.tasks:
            task.setdefault("id", new_quest_id())
            task.setdefault("next_task_id", None)
            task.setdefault("list", store.task_lists[0])
            task.setdefault("subtasks", [])
            task.setdefault("deadline", None)
            task.setdefault("recurrence", None)
            task.setdefault("last_completed", None)
            task.setdefault("celebrated", task.get("done", False))
            task.setdefault("time", (task.get("recurrence") or {}).get("time", ""))
            task.setdefault("reminder", False)
            expedition = task.get("expedition")
            if isinstance(expedition, dict):
                # Una partida migrada o editada no debe romper el detalle por un
                # mundo o índice de tripulación inválido.
                if expedition.get("world") not in QUEST_EXPEDITIONS:
                    # Un mundo fuera del catálogo vuelve a un mundo de misión válido.
                    expedition["world"] = "mecha"
                    expedition["crew"] = 0
                else:
                    names = QUEST_EXPEDITIONS[expedition["world"]]["crew"]
                    if not isinstance(expedition.get("crew"), int) or not 0 <= expedition["crew"] < len(names):
                        expedition["crew"] = 0
            for step in task["subtasks"]:
                step.setdefault("id", new_quest_id())
                step.setdefault("deadline", None)
                step.setdefault("fruit", None)
        if store.current_list not in store.task_lists:
            store.current_list = store.task_lists[0]
        store.data_version = 2

    def quest_document():
        # Convertir contenedores de Ren'Py a valores simples, sin referencias compartidas.
        return _quest_json.loads(_quest_json.dumps({
            "version": 2, "tasks": store.tasks, "lists": store.task_lists,
            "current_list": store.current_list, "player_name": store.player_name,
            "completed_tasks": store.completed_tasks, "theme": store.current_theme,
            "stage": persistent.school_stage, "stage_themes": stage_themes,
            "world_progress": world_progress,
        }, ensure_ascii=False))

    def save_quest_data():
        migrate_quest_data()
        store.persistent.quest_document = quest_document()
        renpy.save_persistent()
        quest_sync_reminders()

    def quest_valid_document(document):
        # Devuelve una copia limpia del documento, o None si no es legible.
        if not isinstance(document, _quest_builtins.dict) or document.get("version") not in (1, 2):
            return None
        tasks = document.get("tasks")
        names = document.get("lists")
        # En Ren'Py `list` es RevertableList: comparar con los builtins reales.
        if not isinstance(tasks, _quest_builtins.list) or not isinstance(names, _quest_builtins.list):
            return None
        if not [name for name in names if isinstance(name, _quest_builtins.str)]:
            return None
        try:
            # Copiar para que editar un borrador nunca modifique el documento guardado.
            copied = _quest_json.loads(_quest_json.dumps(document, ensure_ascii=False))
        except (TypeError, ValueError):
            return None
        # Descartar tareas ilegibles sin perder el resto de la colección.
        copied["tasks"] = [task for task in copied["tasks"]
            if isinstance(task, _quest_builtins.dict) and isinstance(task.get("title"), _quest_builtins.str)]
        copied["lists"] = [name for name in copied["lists"] if isinstance(name, _quest_builtins.str)]
        stage = copied.get("stage", "primaria")
        copied["stage"] = stage if stage in QUEST_SCHOOL_PROFILES else "primaria"
        return copied

    def restore_quest_data():
        raw = store.persistent.quest_document
        document = quest_valid_document(raw)
        if document is None:
            if raw is not None:
                # Conservar el documento dañado para poder revisarlo más tarde.
                store.persistent.quest_document_backup = raw
                renpy.log("DailyQuest: documento de tareas ilegible, se conservó la copia")
                renpy.notify("No se pudo leer el archivo de tareas. Empezamos de nuevo.")
            return False
        store.tasks = document["tasks"]
        store.task_lists = document["lists"]
        store.current_list = document.get("current_list", store.task_lists[0])
        if store.current_list not in store.task_lists:
            store.current_list = store.task_lists[0]
        store.player_name = document.get("player_name", "Amigo")
        store.completed_tasks = document.get("completed_tasks", 0)
        store.current_theme = document.get("theme", "bosque")
        store.stage_themes = document.get("stage_themes", {})
        persistent.school_stage = document.get("stage", "primaria")
        store.world_progress = document.get("world_progress", {})
        if store.current_theme not in QUEST_THEME_ART:
            store.current_theme = "bosque"
        migrate_quest_data()
        quest_sync_reminders(force=True)
        return True

    def quest_autosaved(operation):
        @_quest_functools.wraps(operation)
        def apply(*args, **kwargs):
            result = operation(*args, **kwargs)
            save_quest_data()
            return result
        return apply

    def select_quest_theme(name):
        if name not in quest_stage_themes():
            return
        store.current_theme = name
        store.stage_themes[persistent.school_stage] = name
        save_quest_data()
        quest_sync_theme_music()

    config.after_load_callbacks.append(migrate_quest_data)

init 10 python:
    # Un único límite de guardado para operaciones que cambian los pendientes.
    for _operation_name in ("add_new_task", "rename_task", "complete_task", "add_subtask", "toggle_subtask",
            "remove_subtask", "delete_task", "close_recurrence_series", "add_task_list", "rename_task_list",
            "delete_task_list", "move_task", "set_deadline", "set_subtask_deadline", "set_recurrence"):
        setattr(store, _operation_name, quest_autosaved(getattr(store, _operation_name)))

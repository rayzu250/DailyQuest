# El documento persistente es el último estado confirmado; store es su copia de trabajo.
default persistent.quest_document = None

init -2 python:
    import uuid as _quest_uuid
    import builtins as _quest_builtins
    import json as _quest_json
    import functools as _quest_functools

    def new_quest_id():
        return _quest_uuid.uuid4().hex

    def migrate_quest_data():
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
            for step in task["subtasks"]:
                step.setdefault("id", new_quest_id())
                step.setdefault("deadline", None)
                step.setdefault("fruit", None)
        if store.current_list not in store.task_lists:
            store.current_list = store.task_lists[0]
        store.data_version = 1

    def quest_document():
        # Convertir contenedores de Ren'Py a valores simples, sin referencias compartidas.
        return _quest_json.loads(_quest_json.dumps({
            "version": 1, "tasks": store.tasks, "lists": store.task_lists,
            "current_list": store.current_list, "player_name": store.player_name,
            "completed_tasks": store.completed_tasks, "theme": store.current_theme,
        }, ensure_ascii=False))

    def save_quest_data():
        migrate_quest_data()
        store.persistent.quest_document = quest_document()
        renpy.save_persistent()

    def restore_quest_data():
        document = store.persistent.quest_document
        if not isinstance(document, _quest_builtins.dict) or document.get("version") != 1:
            return False
        # Copiar para que editar un borrador nunca modifique el documento guardado.
        document = _quest_json.loads(_quest_json.dumps(document))
        store.tasks = document["tasks"]
        store.task_lists = document["lists"]
        store.current_list = document.get("current_list", store.task_lists[0])
        store.player_name = document.get("player_name", "Amigo")
        store.completed_tasks = document.get("completed_tasks", 0)
        store.current_theme = document.get("theme", "bosque")
        if store.current_theme not in store.themes:
            store.current_theme = "bosque"
        migrate_quest_data()
        return True

    def quest_autosaved(operation):
        @_quest_functools.wraps(operation)
        def apply(*args, **kwargs):
            result = operation(*args, **kwargs)
            save_quest_data()
            return result
        return apply

    def select_quest_theme(name):
        store.current_theme = name
        save_quest_data()

    config.after_load_callbacks.append(migrate_quest_data)

init 10 python:
    # Un único límite de guardado para operaciones que cambian los pendientes.
    for _operation_name in ("add_new_task", "complete_task", "add_subtask", "toggle_subtask",
            "remove_subtask", "add_task_list", "rename_task_list", "delete_task_list",
            "move_task", "set_deadline", "set_subtask_deadline", "set_recurrence"):
        setattr(store, _operation_name, quest_autosaved(getattr(store, _operation_name)))

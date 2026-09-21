################################################################################
## modelo de datos y funciones auxiliares del ToDo
################################################################################

init offset = -3

# Listas de tareas (etiquetas) y lista seleccionada actualmente
default task_lists = ["General"]
default current_list = "General"

init python:
    # Crea una nueva tarea con todos los campos del modelo
    def new_task(title, task_list=None, priority=1):
        return {
            "title": title,
            "done": False,
            "priority": priority,
            "list": task_list if task_list else store.task_lists[0],
            "subtasks": [],
            "deadline": None,
        }

    def add_new_task(title, task_list=None):
        title = title.strip()
        if title:
            store.tasks.append(new_task(title, task_list))
            renpy.notify("¡Tarea agregada!")

    def complete_task(index):
        if 0 <= index < len(store.tasks) and not store.tasks[index]["done"]:
            store.tasks[index]["done"] = True
            store.completed_tasks += 1
            renpy.notify("¡Bien hecho! +1 estrella ★")

    # --- Subtareas ---

    # Devuelve (completadas, total) o None si la tarea no tiene subtareas
    def subtask_progress(task):
        steps = task.get("subtasks", [])
        if not steps:
            return None
        done = sum(1 for s in steps if s.get("done", False))
        return (done, len(steps))

    def add_subtask(task_index, text):
        text = text.strip()
        if text and 0 <= task_index < len(store.tasks):
            store.tasks[task_index].setdefault("subtasks", []).append({"text": text, "done": False})
            renpy.notify("¡Subtarea agregada!")

    def toggle_subtask(task_index, subtask_index):
        steps = store.tasks[task_index].get("subtasks", [])
        if 0 <= subtask_index < len(steps):
            steps[subtask_index]["done"] = not steps[subtask_index]["done"]

    def remove_subtask(task_index, subtask_index):
        steps = store.tasks[task_index].get("subtasks", [])
        if 0 <= subtask_index < len(steps):
            steps.pop(subtask_index)
            renpy.notify("Subtarea eliminada")
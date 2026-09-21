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
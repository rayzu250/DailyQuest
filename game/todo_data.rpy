################################################################################
## modelo de datos y funciones auxiliares del ToDo
################################################################################

init offset = -3

# Listas de tareas (etiquetas) y lista seleccionada actualmente
default task_lists = ["General"]
default current_list = "General"

init python:
    import datetime as _dt
    import calendar as _cal

    # Nombres de los meses en español
    MONTHS_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    MONTHS_SHORT_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    WEEKDAYS_ES = ["L", "M", "X", "J", "V", "S", "D"]

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

    # --- Listas de tareas ---

    def add_task_list(name):
        name = name.strip()
        if name and name not in store.task_lists:
            store.task_lists.append(name)
            renpy.notify("¡Lista creada!")

    def rename_task_list(old, new):
        new = new.strip()
        if new and new != old and new not in store.task_lists and old in store.task_lists:
            idx = store.task_lists.index(old)
            store.task_lists[idx] = new
            for t in store.tasks:
                if t.get("list", store.task_lists[0]) == old:
                    t["list"] = new
            if store.current_list == old:
                store.current_list = new
            renpy.notify("Lista renombrada")

    def delete_task_list(name):
        if len(store.task_lists) <= 1:
            renpy.notify("No puedes borrar la única lista")
            return
        if name in store.task_lists:
            store.task_lists.remove(name)
            default_list = store.task_lists[0]
            for t in store.tasks:
                if t.get("list", default_list) == name:
                    t["list"] = default_list
            if store.current_list == name:
                store.current_list = default_list
            renpy.notify("Lista eliminada")

    # --- Fechas y deadlines ---

    def today_tuple():
        today = _dt.date.today()
        return (today.year, today.month, today.day)

    def valid_date(d):
        return isinstance(d, (tuple, list)) and len(d) == 3

    def date_tuple_to_string(d):
        if not valid_date(d):
            return "Sin fecha"
        return "%d %s" % (d[2], MONTHS_SHORT_ES[d[1] - 1])

    # Devuelve una matriz de semanas (cada semana es una fila de 7 fechas)
    def month_grid(year, month):
        return _cal.Calendar(firstweekday=0).monthdatescalendar(year, month)

    def set_deadline(task_index, dtuple):
        if 0 <= task_index < len(store.tasks):
            store.tasks[task_index]["deadline"] = dtuple
            renpy.notify("Fecha límite actualizada" if dtuple else "Fecha límite eliminada")

    def is_overdue(task):
        d = task.get("deadline")
        if not valid_date(d):
            return False
        t = today_tuple()
        return (d[0], d[1], d[2]) < (t[0], t[1], t[2])

    def deadline_color(task):
        d = task.get("deadline")
        if not valid_date(d):
            return None
        if is_overdue(task):
            return "#EF5350"
        if d == today_tuple():
            return "#FFD54F"
        return "#81C784"

    # --- Navegación del selector/calendario ---

    def month_move(delta):
        y = store.pick_year if store.pick_year else today_tuple()[0]
        m = store.pick_month if store.pick_month else today_tuple()[1]
        m += delta
        while m < 1:
            m += 12
            y -= 1
        while m > 12:
            m -= 12
            y += 1
        store.pick_year = y
        store.pick_month = m

    def set_pick_today():
        t = today_tuple()
        store.pick_year = t[0]
        store.pick_month = t[1]
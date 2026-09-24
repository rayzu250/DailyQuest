init offset = -3
init python:
    import builtins as _date_builtins
    # --- Fechas y deadlines ---

    def today_tuple():
        today = _dt.date.today()
        return (today.year, today.month, today.day)

    def valid_date(d):
        if not isinstance(d, (_date_builtins.tuple, _date_builtins.list)) or len(d) != 3:
            return False
        try:
            _dt.date(*d)
            return True
        except (TypeError, ValueError, OverflowError):
            return False

    def date_tuple_to_string(d):
        if not valid_date(d):
            return "Sin fecha"
        return "%d %s" % (d[2], MONTHS_SHORT_ES[d[1] - 1])

    # Devuelve una matriz de semanas (cada semana es una fila de 7 fechas)
    def month_grid(year, month):
        return _cal.Calendar(firstweekday=0).monthdatescalendar(year, month)

    def set_deadline(task_index, dtuple):
        if dtuple is not None and not valid_date(dtuple):
            return
        if 0 <= task_index < len(store.tasks):
            store.tasks[task_index]["deadline"] = dtuple
            renpy.notify("Fecha límite actualizada" if dtuple else "Fecha límite eliminada")

    def set_subtask_deadline(task_index, subtask_index, dtuple):
        if dtuple is not None and not valid_date(dtuple):
            return
        steps = store.tasks[task_index].get("subtasks", []) if 0 <= task_index < len(store.tasks) else []
        if 0 <= subtask_index < len(steps):
            steps[subtask_index]["deadline"] = dtuple
            renpy.notify("Fecha límite actualizada" if dtuple else "Fecha límite eliminada")

    def deadline_date_color(d):
        if not valid_date(d):
            return None
        t = today_tuple()
        if (d[0], d[1], d[2]) < (t[0], t[1], t[2]):
            return "#EF5350"
        if (d[0], d[1], d[2]) == (t[0], t[1], t[2]):
            return "#FFD54F"
        return "#81C784"

    def subtask_deadline_color(sub):
        return deadline_date_color(sub.get("deadline"))

    # Fechas relevantes de una tarea: las de sus subtareas o, a modo de
    # compatibilidad, la fecha que existía a nivel de tarea si esta no tiene
    # subtareas.
    def _task_deadlines(task):
        ds = [tuple(s["deadline"]) for s in task.get("subtasks", []) if not s.get("done") and valid_date(s.get("deadline"))]
        if not ds and valid_date(task.get("deadline")):
            ds = [tuple(task["deadline"])]
        return ds

    # Devuelve la fecha límite más próxima (None si no hay ninguna)
    def next_deadline(task):
        ds = _task_deadlines(task)
        return min(ds) if ds else None

    # Cuenta cuántas fechas límite (de subtareas o de tarea legada) caen en un día
    def count_deadlines_on(dkey):
        n = 0
        for t in store.tasks:
            for s in t.get("subtasks", []):
                if valid_date(s.get("deadline")) and tuple(s["deadline"]) == dkey:
                    n += 1
            steps = t.get("subtasks", [])
            if not steps and valid_date(t.get("deadline")) and tuple(t["deadline"]) == dkey:
                n += 1
        return n

    def calendar_entries(dkey):
        entries = []
        for index, task in enumerate(store.tasks):
            if task.get("done"):
                continue
            found = False
            for j, step in enumerate(task.get("subtasks", [])):
                if not step.get("done") and valid_date(step.get("deadline")) and tuple(step["deadline"]) == tuple(dkey):
                    entries.append((index, j, step.get("text", "")))
                    found = True
            if not found:
                deadline = task.get("deadline")
                if (valid_date(deadline) and tuple(deadline) == tuple(dkey)) or is_recurrence_on(task, dkey):
                    entries.append((index, None, ""))
        return entries

    # Migra fechas de nivel tarea a sus subtareas al cargar una partida guardada
    def _migrate_deadlines():
        for t in store.tasks:
            d = t.get("deadline")
            steps = t.get("subtasks", [])
            if d and valid_date(d) and steps:
                for s in steps:
                    if not s.get("deadline"):
                        s["deadline"] = tuple(d)

    config.after_load_callbacks.append(_migrate_deadlines)

    # Asegura los campos nuevos de subtarea en partidas guardadas viejas
    def _migrate_subtask_fields():
        for t in store.tasks:
            for s in t.get("subtasks", []):
                s.setdefault("deadline", None)
                s.setdefault("fruit", None)

    config.after_load_callbacks.append(_migrate_subtask_fields)

    def is_overdue(task):
        d = task.get("deadline")
        if not valid_date(d):
            return False
        t = today_tuple()
        return (d[0], d[1], d[2]) < (t[0], t[1], t[2])

    def deadline_color(task):
        return deadline_date_color(task.get("deadline"))

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

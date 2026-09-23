################################################################################
## modelo de datos y funciones auxiliares del ToDo
################################################################################

init offset = -3

# Listas de tareas (etiquetas) y lista seleccionada actualmente
default task_lists = ["General"]
default current_list = "General"

# Última fruta ganada (recompensa pendiente de mostrar en el popup)
default last_reward = None

init python:
    import datetime as _dt
    import calendar as _cal
    import random

    # Frutas de recompensa (iconos en game/images/fruits/)
    FRUITS = ["apple", "banana", "coconut", "grapes", "strawberry", "watermelon"]

    # Nombres de los meses en español
    MONTHS_ES = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    MONTHS_SHORT_ES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    WEEKDAYS_ES = ["L", "M", "X", "J", "V", "S", "D"]
    WD_SHORT_ES = ["lun", "mar", "mié", "jue", "vie", "sáb", "dom"]

    # Calcula el progreso y devuelve (avatar, mensaje) con refuerzo positivo:
    # nunca regaña, solo anima
    def get_guia_greeting():
        total = 0
        completed = 0
        for task in store.tasks:
            total += 1
            if task.get("done", False):
                completed += 1
        if total == 0:
            return ("guia_happy", "¡Hola! Crea tu primera tarea para empezar la aventura.")
        ratio = completed / float(total)
        if ratio == 0.0:
            return ("guia_happy", "¡Un nuevo día! ¿Qué meta cumpliremos primero?")
        elif ratio < 0.5:
            return ("guia_encouraging", "¡Excelente inicio! Cada pequeño paso cuenta.")
        elif ratio < 1.0:
            return ("guia_cheering", "¡Llevas más de la mitad! ¡Eres genial!")
        else:
            return ("guia_star", "¡Misión cumplida por hoy! ¡A disfrutar el descanso!")

    # Crea una nueva tarea con todos los campos del modelo
    def new_task(title, task_list=None, priority=1, recurrence=None):
        return {
            "title": title,
            "done": False,
            "priority": priority,
            "list": task_list if task_list else store.task_lists[0],
            "subtasks": [],
            "deadline": None,
            "recurrence": recurrence,
            "last_completed": None,
        }

    def add_new_task(title, task_list=None, recurrence=None):
        title = title.strip()
        if title:
            store.tasks.append(new_task(title, task_list, recurrence=recurrence))
            renpy.notify("¡Tarea agregada!")

    def complete_task(index):
        if 0 <= index < len(store.tasks):
            t = store.tasks[index]
            if not t["done"]:
                t["done"] = True
                t["last_completed"] = today_tuple()
                store.completed_tasks += 1
                if t.get("recurrence"):
                    # Genera la copia del próximo ciclo (las copias solo nacen al completar)
                    base = today_tuple()
                    ref = (_dt.date(base[0], base[1], base[2]) + _dt.timedelta(days=1))
                    nxt = next_occurrence(t, (ref.year, ref.month, ref.day))
                    if nxt is not None:
                        subs = [{"text": s.get("text", ""), "done": False, "deadline": None, "fruit": None} for s in t.get("subtasks", [])]
                        store.tasks.append({
                            "title": t["title"],
                            "done": False,
                            "priority": t.get("priority", 1),
                            "list": t.get("list", store.task_lists[0]),
                            "subtasks": subs,
                            "deadline": tuple(nxt),
                            "recurrence": t.get("recurrence"),
                            "last_completed": None,
                        })
                        renpy.notify("¡Misión lista! +1 estrella ★ Ya generé la próxima")
                    else:
                        renpy.notify("¡Misión lista! +1 estrella ★")
                else:
                    renpy.notify("¡Bien hecho! +1 estrella ★")
            else:
                # Reabre la tarea (la copia generada queda como historial)
                t["done"] = False
                t["last_completed"] = None
                if store.completed_tasks > 0:
                    store.completed_tasks -= 1
                renpy.notify("Tarea reabierta")

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
            store.tasks[task_index].setdefault("subtasks", []).append({"text": text, "done": False, "deadline": None, "fruit": None})
            renpy.notify("¡Subtarea agregada!")

    def toggle_subtask(task_index, subtask_index):
        if not (0 <= task_index < len(store.tasks)):
            return
        steps = store.tasks[task_index].get("subtasks", [])
        if 0 <= subtask_index < len(steps):
            st = steps[subtask_index]
            new_state = not st.get("done", False)
            st["done"] = new_state
            if new_state:
                # Asigna fruta si no tiene una previa
                if not st.get("fruit"):
                    st["fruit"] = random.choice(FRUITS)
                store.last_reward = st["fruit"]
                renpy.notify("¡Conseguiste una fruta!")
                renpy.sound.play("audio/reward_ding.ogg")
            else:
                store.last_reward = None

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

    def move_task(task_index, new_list):
        if 0 <= task_index < len(store.tasks) and new_list in store.task_lists:
            store.tasks[task_index]["list"] = new_list
            renpy.notify("Tarea movida a %s" % new_list.capitalize())

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

    def set_subtask_deadline(task_index, subtask_index, dtuple):
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
        ds = [tuple(s["deadline"]) for s in task.get("subtasks", []) if valid_date(s.get("deadline"))]
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

    # --- Tareas recurrentes ---

    # Próxima ocurrencia (año, mes, día) en/tras ref, o None si no aplica
    def next_occurrence(task, ref=None):
        r = task.get("recurrence")
        if not r or r.get("freq", "ninguna") == "ninguna":
            return None
        if ref is None:
            ref = today_tuple()
        ref = tuple(ref)
        freq = r["freq"]
        days = [d for d in r.get("days", []) if isinstance(d, int)]
        if freq == "diaria":
            return ref
        if freq == "semanal":
            if not days:
                return None
            base = _dt.date(ref[0], ref[1], ref[2])
            for k in range(8):
                d = base + _dt.timedelta(days=k)
                if d.weekday() in days:
                    return (d.year, d.month, d.day)
            return None
        if freq == "mensual":
            if not days:
                return None
            y, m = ref[0], ref[1]
            for _ in range(13):
                last = _cal.monthrange(y, m)[1]
                # Los días inexistentes caen en el último día del mes
                cand = sorted(set(min(x, last) for x in days if x >= 1))
                for dd in cand:
                    if (y, m, dd) >= ref:
                        return (y, m, dd)
                m += 1
                if m > 12:
                    m = 1
                    y += 1
            return None
        return None

    def is_recurrence_on(task, dkey):
        r = task.get("recurrence")
        if not r or task.get("done"):
            return False
        nxt = next_occurrence(task, dkey)
        return nxt is not None and tuple(nxt) == tuple(dkey)

    def count_recurring_on(dkey):
        return sum(1 for t in store.tasks if is_recurrence_on(t, dkey))

    def recurrence_description(task):
        r = task.get("recurrence")
        if not r:
            return ""
        freq = r.get("freq", "ninguna")
        time_txt = r.get("time", "")
        base = ""
        if freq == "diaria":
            base = "Todos los días"
        elif freq == "semanal":
            names = [WD_SHORT_ES[d] for d in sorted(r.get("days", [])) if 0 <= d <= 6]
            base = "Cada " + (", ".join(names) if names else "semana")
        elif freq == "mensual":
            ds = sorted(set(d for d in r.get("days", []) if d >= 1))
            base = "Días " + (", ".join(str(d) for d in ds) if ds else "del mes")
        if time_txt:
            base += " · " + time_txt
        return base

    def set_recurrence(task_index, freq, days, time_txt):
        if 0 <= task_index < len(store.tasks):
            if freq == "ninguna":
                store.tasks[task_index]["recurrence"] = None
                renpy.notify("Repetición eliminada")
            else:
                store.tasks[task_index]["recurrence"] = {"freq": freq, "days": sorted(days), "time": time_txt}
                renpy.notify("Repetición guardada")

    def clear_recurrence(task_index):
        set_recurrence(task_index, "ninguna", [], "")

    # Alterna un día en el selector del formulario (reasigna para refrescar)
    def toggle_new_rec_day(d):
        days = list(store.new_rec_days)
        if d in days:
            days.remove(d)
        else:
            days.append(d)
        store.new_rec_days = days

    def bump_new_rec_h(d):
        store.new_rec_h = (store.new_rec_h + d) % 24

    def bump_new_rec_m(d):
        store.new_rec_m = (store.new_rec_m + d) % 60

    # Asegura los campos de recurrencia en partidas guardadas viejas
    def _migrate_recurrence():
        for t in store.tasks:
            t.setdefault("recurrence", None)
            t.setdefault("last_completed", None)

    config.after_load_callbacks.append(_migrate_recurrence)

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
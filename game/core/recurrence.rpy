init offset = -3
init python:
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
        if valid_date(task.get("deadline")) and tuple(dkey) < tuple(task["deadline"]):
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

    # Asegura los campos de recurrencia en partidas guardadas viejas
    def _migrate_recurrence():
        for t in store.tasks:
            t.setdefault("recurrence", None)
            t.setdefault("last_completed", None)

    config.after_load_callbacks.append(_migrate_recurrence)

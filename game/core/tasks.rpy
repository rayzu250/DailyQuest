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
    import random

    # Identificadores históricos: la imagen visible depende del mundo seleccionado.
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
            "id": new_quest_id(),
            "title": title,
            "done": False,
            "priority": priority,
            "list": task_list if task_list else store.task_lists[0],
            "subtasks": [],
            "deadline": None,
            "recurrence": recurrence,
            "last_completed": None,
            "next_task_id": None,
            "time": (recurrence or {}).get("time", ""),
            "reminder": False,
            "expedition": quest_new_expedition() if quest_secondary() else None,
        }

    def add_new_task(title, task_list=None, recurrence=None):
        title = title.strip()
        if title:
            store.tasks.append(new_task(title, task_list, recurrence=recurrence))
            guide_event("Ya anotaste lo que quieres hacer.")

    def complete_task(index):
        if 0 <= index < len(store.tasks):
            t = store.tasks[index]
            if not quest_allow_completion(t):
                return
            if not t["done"]:
                first_completion = not t.get("celebrated", False)
                t["done"] = True
                t["celebrated"] = True
                t["last_completed"] = today_tuple()
                store.completed_tasks += 1
                if t.get("recurrence") and not t.get("next_task_id"):
                    # Genera la copia del próximo ciclo (las copias solo nacen al completar)
                    base = max(today_tuple(), tuple(t["deadline"])) if valid_date(t.get("deadline")) else today_tuple()
                    ref = (_dt.date(base[0], base[1], base[2]) + _dt.timedelta(days=1))
                    nxt = next_occurrence(t, (ref.year, ref.month, ref.day))
                    if nxt is not None:
                        child_id = new_quest_id()
                        t["next_task_id"] = child_id
                        # Los pasos copiados nacen con identidad propia para que
                        # sus recursos y recompensas no compartan serie con el padre.
                        subs = [{"id": new_quest_id(), "text": s.get("text", ""), "done": False,
                            "deadline": None, "fruit": None} for s in t.get("subtasks", [])]
                        store.tasks.append({
                            "id": child_id,
                            "next_task_id": None,
                            "title": t["title"],
                            "done": False,
                            "priority": t.get("priority", 1),
                            "list": t.get("list", store.task_lists[0]),
                            "subtasks": subs,
                            "deadline": tuple(nxt),
                            "recurrence": dict(t["recurrence"]),
                            "last_completed": None,
                            "time": quest_task_time(t),
                            "reminder": t.get("reminder", False),
                            "expedition": quest_new_expedition(t["expedition"]["world"]) if quest_task_expedition(t) else None,
                        })
                        renpy.notify("¡Misión lista! +1 estrella ★ Ya generé la próxima")
                    else:
                        renpy.notify("¡Misión lista! +1 estrella ★")
                else:
                    renpy.notify("¡Bien hecho! +1 estrella ★")
                guide_event("¡Terminaste esta tarea!" if first_completion else "La tarea vuelve a estar completada.",
                    "guia_star", celebrate=first_completion)
                if not first_completion:
                    store.guide_animated = False
            else:
                # Reabre la tarea (la copia generada queda como historial)
                t["done"] = False
                t["last_completed"] = None
                if store.completed_tasks > 0:
                    store.completed_tasks -= 1
                renpy.notify("Tarea reabierta")
                guide_event("Puedes revisar los pasos que faltan.")
            quest_update_expedition_completion(t)

    # --- Eliminar tareas ---

    def delete_task(index):
        # Borrar es seguro: la pantalla pide confirmación antes de llegar aquí.
        # Los logros ya ganados no se quitan cuando la tarea desaparece.
        if not 0 <= index < len(store.tasks):
            renpy.notify("Esa tarea ya no está en la lista.")
            return False
        store.tasks.pop(index)
        renpy.notify("Tarea eliminada")
        guide_event("Borrar lo que ya no necesitas también es organizar.")
        return True

    def _quest_task_by_id(task_id):
        # Las copias de una serie se reconocen por id, no por posición.
        for task in store.tasks:
            if task.get("id") == task_id:
                return task
        return None

    def quest_series_members(task):
        # Toda la familia de copias a la que pertenece `task`: la copia
        # original y cada una de las recurrencias generadas.
        inside = any(member is task for member in store.tasks)
        if not task.get("recurrence") or not inside:
            return [task] if inside else []
        # Subir por los enlaces hasta la copia original de la serie.
        root = task
        for _ in range(len(store.tasks) + 1):
            parent = None
            for member in store.tasks:
                if member is not root and member.get("next_task_id") == root.get("id"):
                    parent = member
                    break
            if parent is None:
                break
            root = parent
        # Bajar por la cadena completa, copia por copia, sin bucles.
        members = []
        current = root
        while current is not None:
            if any(current is member for member in members):
                break
            members.append(current)
            current = _quest_task_by_id(current.get("next_task_id"))
        return members

    def close_recurrence_series(index):
        # Deja la copia actual fuera de la lista y también las demás
        # de su cadena: la recurrencia no genera otra nunca más.
        if not 0 <= index < len(store.tasks):
            renpy.notify("Esa tarea ya no está en la lista.")
            return False
        members = quest_series_members(store.tasks[index])
        gone = set(member.get("id") for member in members)
        store.tasks = [task for task in store.tasks if task.get("id") not in gone]
        renpy.notify("Serie cerrada: %d tareas eliminadas" % len(members))
        guide_event("Las tareas repetidas también pueden terminar.")
        return True

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
            if store.tasks[task_index].get("done") and quest_task_expedition(store.tasks[task_index]):
                renpy.notify("Reabre la misión para agregar pasos.")
                return
            store.tasks[task_index].setdefault("subtasks", []).append({"id": new_quest_id(), "text": text, "done": False, "deadline": None, "fruit": None})
            guide_event("Dividir una tarea en pasos puede ayudarte a empezar.")

    def toggle_subtask(task_index, subtask_index):
        if not (0 <= task_index < len(store.tasks)):
            return
        if not quest_allow_step(store.tasks[task_index]):
            return
        steps = store.tasks[task_index].get("subtasks", [])
        if 0 <= subtask_index < len(steps):
            st = steps[subtask_index]
            new_state = not st.get("done", False)
            st["done"] = new_state
            if new_state:
                # Asigna fruta si no tiene una previa
                first_completion = not st.get("fruit")
                if first_completion:
                    st["fruit"] = random.choice(FRUITS)
                    quest_record_resource(store.tasks[task_index], st)
                completed = sum(1 for step in steps if step.get("done"))
                guide_event("Completaste %d de %d pasos." % (completed, len(steps)),
                    "guia_cheering", fruit=st["fruit"] if first_completion else None, celebrate=first_completion,
                    world=st.get("reward_world"))
                if not first_completion:
                    store.guide_animated = False
            else:
                guide_event("Este paso queda pendiente para revisarlo.")

    def remove_subtask(task_index, subtask_index):
        if not 0 <= task_index < len(store.tasks):
            return
        if store.tasks[task_index].get("done") and quest_task_expedition(store.tasks[task_index]):
            renpy.notify("Reabre la misión para borrar pasos.")
            return
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

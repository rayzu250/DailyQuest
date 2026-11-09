# Herramientas compartidas; cada mundo conserva sus recursos y desbloqueos.
# Borradores de la configuración del pomodoro (Fase 5): por defecto
# 4 bloques de 25 minutos de trabajo y 5 de descanso.
default pomodoro_blocks = 4
default pomodoro_work = 25
default pomodoro_rest = 5

init -2 python:
    import time as _base_time
    import math as _base_math
    # En Ren'Py el `dict` del store es RevertableDict; para validar tanto
    # contenedores revertables como dicts planos (JSON restaurado) usamos
    # el builtin real, igual que hace quest_valid_document.
    import builtins as _base_builtins

    QUEST_BASE_ROLES = {
        "mecha": ("planning", "library", "rest"),
        "arcane": ("library", "planning", "rest"),
        "stage": ("planning", "rest", "library"),
    }
    QUEST_BASE_DESCRIPTIONS = {
        "planning": "Organiza tus proyectos y elige el siguiente paso.",
        "library": "Consulta lo que terminaste y reutiliza tus mejores planes.",
        "rest": "Haz una pausa de 5, 10 o 15 minutos, sin presión.",
    }

    def quest_base_role(world, number):
        return QUEST_BASE_ROLES.get(world, ("planning", "library", "rest"))[number]

    def quest_base_available(world, number):
        return (quest_secondary() and world in quest_stage_themes()
            and world in QUEST_EXPEDITIONS and number in (0, 1, 2)
            and number in world_progress.get(world, {}).get("upgrades", []))

    def quest_base_open(world, number):
        if quest_base_available(world, number):
            renpy.show_screen("quest_base_room", world=world, number=number)

    def quest_base_indices(world, status=None):
        result = []
        for i, task in enumerate(tasks):
            expedition = quest_task_expedition(task)
            if not expedition or expedition["world"] != world:
                continue
            state = "finished" if task.get("done") else expedition.get("state", "planned")
            if status is None or state == status:
                result.append(i)
        return sorted(result, key=lambda i: tasks[i].get("priority", 1))

    def quest_base_task(task_id):
        index = next((i for i, task in enumerate(tasks) if task["id"] == task_id), None)
        if index is not None:
            renpy.hide_screen("quest_base_room")
            quest_navigate()
            renpy.show_screen("task_detail_screen", i=index)

    def quest_base_reuse(world, number, task_id):
        if not quest_base_available(world, number) or quest_base_role(world, number) != "library":
            return
        original = next((task for task in tasks if task["id"] == task_id), None)
        if not original or not original.get("done"):
            return
        expedition = quest_task_expedition(original)
        if not expedition or expedition["world"] != world:
            return
        # Crear un plan limpio: nunca heredar fechas, avisos, logros ni recursos.
        task = new_task(original["title"] + " · nuevo proyecto", original["list"], original.get("priority", 1))
        task["expedition"] = quest_new_expedition(world)
        task["expedition"]["goal"] = expedition.get("goal", "")
        task["subtasks"] = [{"id": new_quest_id(), "text": step.get("text", ""),
            "done": False, "deadline": None, "fruit": None} for step in original.get("subtasks", [])]
        store.tasks.append(task)
        save_quest_data()
        renpy.notify("Nuevo proyecto creado. Puedes encontrarlo en Por hacer.")

    def quest_base_start_rest(world, number, minutes):
        if (not quest_base_available(world, number) or quest_base_role(world, number) != "rest"
                or minutes not in (5, 10, 15)):
            return
        # Fecha absoluta: suspender Android no detiene el tiempo transcurrido.
        world_progress[world]["rest_until"] = _base_time.time() + minutes * 60
        save_quest_data()
        renpy.restart_interaction()

    def quest_base_rest_remaining(world, now=None):
        deadline = world_progress.get(world, {}).get("rest_until", 0)
        return max(0, int(_base_math.ceil(deadline - (_base_time.time() if now is None else now))))

    def quest_base_end_rest(world):
        if world in world_progress:
            world_progress[world].pop("rest_until", None)
            save_quest_data()
        renpy.restart_interaction()

    # --- Pomodoro personalizado (Fase 5) ---
    # Las pausas rápidas 5/10/15 quedan intactas; este estado aparte usa un
    # reloj absoluto (ends_at) para sobrevivir a la suspensión de Android y
    # al "Forzar detención". OJO: descanso solo ENTRE bloques; el último
    # bloque de trabajo cierra el ciclo ya.
    QUEST_POMODORO_DEFAULTS = {"blocks": 4, "work": 25, "rest": 5}
    QUEST_POMODORO_LIMITS = {"blocks": (1, 8), "work": (5, 90), "rest": (1, 30)}

    def quest_pomodoro_room(world, number):
        return (quest_base_available(world, number)
            and quest_base_role(world, number) == "rest")

    def quest_pomodoro_start(world, number, blocks, work, rest):
        if not quest_pomodoro_room(world, number):
            return False
        try:
            cfg = {"blocks": int(blocks), "work": int(work), "rest": int(rest)}
        except (TypeError, ValueError):
            return False
        for key, value in cfg.items():
            lo, hi = QUEST_POMODORO_LIMITS[key]
            if not lo <= value <= hi:
                renpy.notify(_("Pomodoro: valores fuera de rango."))
                return False
        # Una pausa simple en curso se termina para no mezclar relojes.
        world_progress[world].pop("rest_until", None)
        world_progress[world]["pomodoro_config"] = cfg
        world_progress[world]["pomodoro"] = {
            "blocks": cfg["blocks"], "work": cfg["work"], "rest": cfg["rest"],
            "block": 1, "phase": "work",
            "ends_at": _base_time.time() + cfg["work"] * 60,
        }
        save_quest_data()
        renpy.restart_interaction()
        return True

    def quest_pomodoro_state(world, now=None):
        # Estado fresco tras avanzar todas las fases vencidas: al volver de la
        # suspensión, el tiempo transcurrido con la app cerrada cuenta igual.
        state = world_progress.get(world, {}).get("pomodoro")
        if not isinstance(state, _base_builtins.dict) or "ends_at" not in state:
            return None
        seconds = _base_time.time() if now is None else float(now)
        events = []
        while state["ends_at"] <= seconds:
            if state["phase"] == "work":
                if state["block"] >= state["blocks"]:
                    del world_progress[world]["pomodoro"]
                    events.append("finished")
                    return {"state": None, "remaining": 0, "events": events}
                state["phase"] = "rest"
                state["ends_at"] += state["rest"] * 60
                events.append("work_done")
            else:
                state["block"] += 1
                state["phase"] = "work"
                state["ends_at"] += state["work"] * 60
                events.append("rest_done")
        # Sin I/O aquí: guardar es responsabilidad del caller (poll), para que
        # esta función sea predecible con el reloj simulado de los tests.
        remaining = max(0, int(_base_math.ceil(state["ends_at"] - seconds)))
        return {"state": state, "remaining": remaining, "events": events}

    def quest_pomodoro_stop(world):
        if world in world_progress and world_progress[world].pop("pomodoro", None) is not None:
            save_quest_data()
        renpy.restart_interaction()
        return True

    def quest_pomodoro_bump(key, delta):
        # Steppers de la pantalla: se recorta al rango permitido, nunca lanza.
        value = int(getattr(store, key) + delta)
        lo, hi = QUEST_POMODORO_LIMITS[key]
        setattr(store, key, max(lo, min(hi, value)))
        renpy.restart_interaction()

    def quest_pomodoro_start_action(world, number):
        # Acción de pantalla: si una acción devolviera True (el contrato de la
        # API para tests), renpy terminaría la interacción y cerraría el cuarto.
        quest_pomodoro_start(world, number, store.pomodoro_blocks,
            store.pomodoro_work, store.pomodoro_rest)

    def quest_pomodoro_stop_action(world):
        quest_pomodoro_stop(world)

    def quest_pomodoro_sync_drafts(world):
        # Arranque de pantalla: los steppers muestran la última configuración
        # usada en ese cuarto; si no hubo, los valores por defecto.
        cfg = dict(QUEST_POMODORO_DEFAULTS)
        saved = world_progress.get(world, {}).get("pomodoro_config")
        if isinstance(saved, _base_builtins.dict):
            for key in cfg:
                lo, hi = QUEST_POMODORO_LIMITS[key]
                value = saved.get(key, cfg[key])
                cfg[key] = value if lo <= value <= hi else cfg[key]
        store.pomodoro_blocks = cfg["blocks"]
        store.pomodoro_work = cfg["work"]
        store.pomodoro_rest = cfg["rest"]

    def quest_pomodoro_poll(world):
        # El temporizador de pantalla llama esto cada segundo; también cumple
        # con el refresco de las pausas simples (rest_until). Las transiciones
        # detectadas se guardan aquí, no dentro de quest_pomodoro_state.
        result = quest_pomodoro_state(world)
        if result and result["events"]:
            save_quest_data()
        nodes = world_progress.get(world, {})
        if result:
            cfg = nodes.get("pomodoro_config") or QUEST_POMODORO_DEFAULTS
            for event in result["events"]:
                if event == "work_done":
                    renpy.notify((_("¡Bloque listo! Descansa %d minutos.")) % cfg["rest"])
                elif event == "rest_done":
                    renpy.notify(_("¡Descanso terminado! Turno de concentrarse."))
                elif event == "finished":
                    renpy.notify((_("¡Pomodoro completo! %d bloques.")) % cfg["blocks"])
        renpy.restart_interaction()

# Expediciones: el progreso se guarda antes de mostrar cualquier animación.
default world_progress = {}
default expedition_goal_draft = ""
default expedition_reflection_draft = ""

init -2 python:
    QUEST_EXPEDITIONS = {
        "mecha": {
            "home": "Hangar", "resource": "Núcleos de energía",
            "departure": "Sistemas listos. Tu equipo sale del hangar.",
            "return": "Operación completada. Tu equipo regresa al hangar.",
            "crew": ("Atlas", "Nova", "Vega"),
            "upgrades": ("Taller de mantenimiento", "Centro de navegación", "Jardín del hangar"),
        },
        "arcane": {
            "home": "Academia", "resource": "Runas",
            "departure": "La investigación comienza. Tu aprendiz sale de la academia.",
            "return": "Investigación completada. Regreso a la academia.",
            "crew": ("Ariel", "Luz", "Sol"),
            "upgrades": ("Biblioteca restaurada", "Observatorio", "Jardín de estudio"),
        },
        "stage": {
            "home": "Estudio", "resource": "Ideas musicales",
            "departure": "Proyecto en marcha. Tu artista prepara la presentación.",
            "return": "Proyecto completado. Es momento de volver al estudio.",
            "crew": ("Alex", "Río", "Sam"),
            "upgrades": ("Cabina de grabación", "Luces del escenario", "Sala de composición"),
        },
    }
    QUEST_CREW_TINTS = ("#FFFFFF", "#B8DDD5", "#DCC8F0")

    def quest_crew_index(expedition, pool):
        # Un índice de una partida migrada o editada no debe romper las pantallas.
        crew = expedition.get("crew", 0)
        if not isinstance(crew, int) or not 0 <= crew < len(pool):
            crew = 0
        return crew

    def quest_crew_name(expedition):
        world = expedition["world"]
        names = QUEST_EXPEDITIONS[world]["crew"]
        return names[quest_crew_index(expedition, names)]

    def quest_new_expedition(world=None):
        world = world or quest_theme_key()
        if world not in QUEST_EXPEDITIONS:
            world = "mecha"
        return {"world": world, "crew": 0, "state": "planned", "goal": "",
            "reflection": "", "finished_at": None}

    def quest_task_expedition(task):
        expedition = task.get("expedition")
        return expedition if isinstance(expedition, _quest_builtins.dict) and expedition.get("world") in QUEST_EXPEDITIONS else None

    def quest_expedition_state(task):
        expedition = quest_task_expedition(task)
        if not expedition:
            return "Sin iniciar"
        if task.get("done"):
            return "Completada"
        state = expedition.get("state", "planned")
        if state == "active" and quest_expedition_ready(task):
            return "Lista para finalizar"
        return {"planned": "Preparada", "active": "En misión", "paused": "En pausa"}.get(state, "Preparada")

    def quest_expedition_ready(task):
        return all(step.get("done") for step in task.get("subtasks", []))

    def quest_expedition_image(task):
        expedition = quest_task_expedition(task)
        world = expedition["world"] if expedition else quest_theme_key()
        crew = expedition.get("crew", 0) if expedition else 0
        return Transform("images/themes/%s/guide.png" % world,
            matrixcolor=TintMatrix(QUEST_CREW_TINTS[crew % len(QUEST_CREW_TINTS)]))

    def quest_begin_expedition(index):
        if not quest_secondary() or not 0 <= index < len(tasks) or tasks[index].get("done"):
            return
        task = tasks[index]
        expedition = quest_task_expedition(task)
        if not expedition:
            expedition = quest_new_expedition()
            task["expedition"] = expedition
        if expedition["state"] == "active":
            return
        expedition["state"] = "active"
        save_quest_data()
        renpy.show_screen("quest_expedition_scene", task_id=task["id"], returning=False)

    def quest_pause_expedition(index):
        if not quest_secondary() or not 0 <= index < len(tasks):
            return
        expedition = quest_task_expedition(tasks[index])
        if expedition and expedition["state"] == "active" and not tasks[index].get("done"):
            expedition["state"] = "paused"
            save_quest_data()
            renpy.notify("Misión en pausa. Puedes continuar cuando quieras.")

    def quest_assign_expedition(index, world=None, crew=None):
        if not quest_secondary() or not 0 <= index < len(tasks):
            return
        task = tasks[index]
        expedition = quest_task_expedition(task)
        if task.get("done") or (expedition and expedition["state"] != "planned"):
            return
        if not expedition:
            task["expedition"] = quest_new_expedition(world)
            expedition = task["expedition"]
        if world in QUEST_EXPEDITIONS:
            expedition["world"] = world
        if crew in (0, 1, 2):
            expedition["crew"] = crew
        save_quest_data()

    def quest_tasks_without_expedition():
        # Tareas creadas en otro perfil: convertibles en proyectos.
        return [task for task in tasks if not quest_task_expedition(task)]

    def quest_convert_all_tasks():
        if not quest_secondary():
            return 0
        converted = 0
        for task in quest_tasks_without_expedition():
            expedition = quest_new_expedition()
            if task.get("done"):
                # Lo ya logrado no se pierde ni reaparece como pendiente.
                expedition["state"] = "finished"
                expedition["finished_at"] = list(today_tuple())
            task["expedition"] = expedition
            converted += 1
        if converted:
            save_quest_data()
            guide_event("Convertí tus tareas en proyectos con misión y recursos.")
            renpy.notify("Proyectos listos")
        return converted

    def quest_allow_completion(task):
        if not quest_secondary() or task.get("done"):
            return True
        expedition = quest_task_expedition(task)
        if not expedition:
            # Tarea heredada de otro perfil: se completa como tarea normal.
            return True
        if expedition["state"] != "active":
            renpy.notify("Inicia o continúa la misión antes de finalizarla.")
            return False
        if not quest_expedition_ready(task):
            renpy.notify("Completa los pasos pendientes antes de finalizar.")
            return False
        return True

    def quest_allow_step(task):
        if task.get("done") and quest_task_expedition(task):
            renpy.notify("Reabre la misión para modificar sus pasos.")
            return False
        if not quest_secondary():
            return True
        expedition = quest_task_expedition(task)
        if expedition and expedition["state"] != "active":
            renpy.notify("Inicia o continúa la misión para completar sus pasos.")
            return False
        return True

    def quest_record_resource(task, step):
        expedition = quest_task_expedition(task)
        if not expedition or not quest_secondary() or expedition["state"] != "active":
            return
        world = expedition["world"]
        step["reward_world"] = world
        progress = store.world_progress.setdefault(world, {"earned": [], "upgrades": []})
        # Un identificador por paso; reabrir, cargar o tocar dos veces no duplica recursos.
        # Si un paso heredado no tiene identidad propia, nace aquí una sola vez.
        step_id = step.setdefault("id", new_quest_id())
        if step_id not in progress["earned"]:
            progress["earned"].append(step_id)

    def quest_update_expedition_completion(task):
        expedition = quest_task_expedition(task)
        if not expedition:
            return
        if task.get("done"):
            expedition["state"] = "finished"
            expedition["finished_at"] = list(today_tuple())
            if quest_secondary():
                renpy.show_screen("quest_expedition_scene", task_id=task["id"], returning=True)
        else:
            expedition["state"] = "paused"
            expedition["finished_at"] = None

    def quest_world_balance(world):
        progress = world_progress.get(world, {})
        return len(progress.get("earned", [])) - 3 * len(progress.get("upgrades", []))

    def quest_unlock_upgrade(world, number):
        if not quest_secondary() or world not in QUEST_EXPEDITIONS or number not in (0, 1, 2):
            return
        progress = store.world_progress.setdefault(world, {"earned": [], "upgrades": []})
        if number in progress["upgrades"] or quest_world_balance(world) < 3:
            return
        progress["upgrades"].append(number)
        save_quest_data()
        renpy.notify("Mejora desbloqueada.")

    def quest_open_plan(index):
        expedition = quest_task_expedition(tasks[index])
        store.expedition_goal_draft = expedition.get("goal", "") if expedition else ""
        store.expedition_reflection_draft = expedition.get("reflection", "") if expedition else ""
        renpy.show_screen("quest_expedition_plan", index=index)

    def quest_save_plan(index):
        if quest_secondary() and 0 <= index < len(tasks):
            task = tasks[index]
            if not quest_task_expedition(task):
                task["expedition"] = quest_new_expedition()
            task["expedition"]["goal"] = expedition_goal_draft.strip()
            task["expedition"]["reflection"] = expedition_reflection_draft.strip()
            save_quest_data()
        renpy.hide_screen("quest_expedition_plan")

    def quest_set_priority(index, priority):
        if quest_secondary() and 0 <= index < len(tasks) and priority in (0, 1, 2):
            tasks[index]["priority"] = priority
            save_quest_data()

    def quest_expedition_indices(completed=False):
        return [i for i, task in enumerate(tasks)
            if quest_task_expedition(task) and bool(task.get("done")) == completed]

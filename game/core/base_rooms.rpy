# Herramientas compartidas; cada mundo conserva sus recursos y desbloqueos.
init -2 python:
    import time as _base_time
    import math as _base_math

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

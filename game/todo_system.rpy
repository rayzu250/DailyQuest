# todo_system.rpy
default tasks = []          # Lista de diccionarios: {"title": "", "done": False, "priority": 1}
default max_tasks = 10

label view_tasks:
    if not tasks:
        e "¡Todavía no tienes tareas! Agrega una para empezar tu aventura."
        jump main_menu_todo

    $ task_text = ""
    python:
        for i, t in enumerate(tasks):
            status = "✓" if t["done"] else "○"
            task_text += f"{i+1}. {status} {t['title']}\n"

    e "[task_text]"

    menu:
        "Marcar tarea como completada":
            jump mark_done
        "Volver":
            jump main_menu_todo

label add_task:
    $ title = renpy.input("¿Cuál es tu nueva tarea/proyecto?", length=40)
    $ title = title.strip()
    if title:
        $ tasks.append({"title": title, "done": False, "priority": 1})
        e "¡Tarea agregada! Ahora puedes darle seguimiento."
    jump main_menu_todo

label mark_done:
    $ choice = renpy.input("Número de la tarea a completar:", allow="0123456789")
    python:
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(tasks) and not tasks[idx]["done"]:
                tasks[idx]["done"] = True
                store.completed_tasks += 1
                renpy.notify("¡Bien hecho! +1 estrella")
        except:
            pass
    jump view_tasks
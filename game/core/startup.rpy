# Avisos de inicio (Fase 5): una pantalla amable cuando quedan tareas para
# hoy y otra distinta (Comandante regañando) cuando hay tareas de días
# anteriores sin completar. Una sola vez al día y nunca en el onboarding.
default persistent.quest_startup_notice = None

init -1 python:
    import datetime as _startup_dt

    def quest_due_today_tasks():
        # Pendientes cuyo plazo vence HOY (incluye la próxima fecha
        # de tareas recurrentes pendientes).
        today = today_tuple()
        return [task for task in store.tasks
            if not task.get("done") and next_deadline(task) == today]

    def quest_overdue_tasks():
        # Pendientes vencidos: la fecha límite de la tarea es anterior a hoy.
        return [task for task in store.tasks
            if not task.get("done") and is_overdue(task)]

    def quest_startup_day_key():
        return "%04d-%02d-%02d" % today_tuple()

    def quest_maybe_show_startup_notices():
        # Las suites distintas de `startup` silencian los avisos: un Jump con
        # tareas heredadas mostraría un modal que rompería sus clicks.
        if getattr(store, "_quest_test_no_startup_notices", False):
            return False
        overdue = len(quest_overdue_tasks())
        due_today = len(quest_due_today_tasks())
        if not overdue and not due_today:
            return False
        key = quest_startup_day_key()
        # Una vez por día: al reabrir el mismo día no se repite el aviso.
        if persistent.quest_startup_notice == key:
            return False
        persistent.quest_startup_notice = key
        renpy.save_persistent()
        # De abajo hacia arriba: primero amable, arriba el regaño; cerrar
        # el aviso superior revela el segundo.
        if due_today:
            renpy.show_screen("quest_startup_due_today", count=due_today)
        if overdue:
            renpy.show_screen("quest_startup_overdue", count=overdue)
        renpy.restart_interaction()
        return True

    def quest_startup_close_all():
        renpy.hide_screen("quest_startup_overdue")
        renpy.hide_screen("quest_startup_due_today")

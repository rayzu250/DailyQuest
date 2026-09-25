# Puente opcional: las tareas siguen funcionando en PC o sin permisos Android.
default new_has_time = False
default new_reminder = False
default reminder_error = ""

init -1 python:
    def quest_time_parts(value):
        try:
            hour, minute = map(int, value.split(":"))
            if 0 <= hour <= 23 and 0 <= minute <= 59:
                return hour, minute
        except (AttributeError, ValueError, TypeError):
            pass
        return None

    def quest_task_time(task):
        return task.get("time", (task.get("recurrence") or {}).get("time", ""))

    def quest_reminder_payload():
        result = []
        for task in store.tasks:
            parts = quest_time_parts(quest_task_time(task))
            if task.get("done") or not task.get("reminder") or not parts:
                continue
            # Una copia reabierta no duplica la serie que ya continúa en su hija.
            recurrence = task.get("recurrence") or {}
            if recurrence and task.get("next_task_id"):
                continue
            date = task.get("deadline")
            if not recurrence and not valid_date(date):
                continue
            result.append({"id": task["id"], "title": task["title"],
                "hour": parts[0], "minute": parts[1],
                "start": "%04d-%02d-%02d" % tuple(date) if valid_date(date) else "",
                "freq": recurrence.get("freq", ""), "days": recurrence.get("days", [])})
        return result

    def quest_native_reminders():
        from jnius import autoclass
        return (autoclass("com.dailyquest.reminders.Reminders"),
            autoclass("org.renpy.android.PythonSDLActivity").mActivity)

    def quest_sync_reminders(force=False):
        if not renpy.android:
            return
        try:
            bridge, activity = quest_native_reminders()
            bridge.sync(activity, _quest_json.dumps(quest_reminder_payload(), ensure_ascii=False))
            if force:
                # Al abrir tras "Forzar detención", Android ya canceló las alarmas.
                bridge.reschedule(activity)
            store.reminder_error = ""
        except Exception as error:
            store.reminder_error = "No se pudieron programar los avisos. Revisa la instalación de Android."
            renpy.log("DailyQuest reminders: %s" % error)

    def quest_reminder_status():
        if not renpy.android:
            return "Los avisos del teléfono funcionan al instalar el juego en Android."
        if store.reminder_error:
            return store.reminder_error
        try:
            bridge, activity = quest_native_reminders()
            if not bridge.allowed(activity):
                return "Los avisos están bloqueados. Activa el permiso de notificaciones."
            if not bridge.exact(activity):
                return "Avisos aproximados: Android puede retrasarlos."
            return "Avisos puntuales permitidos por Android."
        except Exception:
            return "Esta instalación no incluye los avisos de Android."

    def quest_reminder_permission():
        if not renpy.android:
            return
        try:
            from jnius import autoclass
            bridge, activity = quest_native_reminders()
            bridge.channel(activity)
            if autoclass("android.os.Build$VERSION").SDK_INT >= 33 and not renpy.check_permission("android.permission.POST_NOTIFICATIONS"):
                renpy.request_permission("android.permission.POST_NOTIFICATIONS")
            else:
                bridge.notificationSettings(activity)
        except Exception as error:
            renpy.log("DailyQuest reminder permission: %s" % error)
            renpy.notify("No se pudo abrir el permiso de avisos.")

    def quest_exact_permission():
        try:
            bridge, activity = quest_native_reminders()
            bridge.exactSettings(activity)
        except Exception as error:
            renpy.log("DailyQuest exact permission: %s" % error)
            renpy.notify("No se pudo abrir la configuración de horarios.")

    def quest_poll_reminders():
        # El temporizador solo se instala en Android. También detecta permisos al volver.
        if not renpy.android:
            return
        try:
            bridge, activity = quest_native_reminders()
            state = (bool(bridge.allowed(activity)), bool(bridge.exact(activity)))
            if getattr(quest_poll_reminders, "last_state", None) != state:
                quest_sync_reminders()
                quest_poll_reminders.last_state = state
                renpy.restart_interaction()
            task_id = bridge.consumeTask(activity)
            if task_id:
                for i, task in enumerate(store.tasks):
                    if task["id"] == task_id:
                        store.current_list = task["list"]
                        quest_navigate()
                        renpy.show_screen("task_detail_screen", i=i)
                        renpy.restart_interaction()
                        break
        except Exception:
            pass

    def save_task_reminder(index, has_time, hour, minute, enabled):
        if not 0 <= index < len(store.tasks):
            return
        task = store.tasks[index]
        if enabled and (not has_time or (not task.get("recurrence") and not valid_date(task.get("deadline")))):
            renpy.notify("Elige una hora y una fecha, o una repetición.")
            return
        task["time"] = "%02d:%02d" % (hour, minute) if has_time else ""
        task["reminder"] = bool(enabled and has_time)
        if task.get("recurrence"):
            task["recurrence"]["time"] = task["time"]
        save_quest_data()
        renpy.hide_screen("task_reminder_screen")
        if enabled:
            renpy.notify(quest_reminder_status())

    config.after_load_callbacks.append(lambda: quest_sync_reminders(force=True))

init python:
    build.android_permissions += ["android.permission.POST_NOTIFICATIONS",
        "android.permission.RECEIVE_BOOT_COMPLETED", "android.permission.SCHEDULE_EXACT_ALARM"]

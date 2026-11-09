# Validar los avisos de inicio (Fase 5) sin tocar partidas personales:
# contadores, orden de pantallas y bandera de una vez por día.
testsuite startup:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            _test.timeout = 25.0
            persistent.quest_startup_notice = None
            # SOLO esta suite reactiva los avisos de inicio silenciados por
            # tests/hermetic.rpy; con las tareas vaciadas antes del Jump los
            # disparos fantasma quedan descartados.
            store._quest_test_no_startup_notices = False
            # Vaciar antes del Jump: main_menu_todo corre los avisos con lo
            # que exista al arrancar; heredar las tareas del testcase anterior
            # dispararía pantallas fantasma.
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
        run Jump("main_menu_todo")
        python:
            store.task_filter = "all"
            store.completed_tasks = 0

    after testcase:
        python:
            persistent.quest_startup_notice = None
            quest_startup_close_all()
            store.task_filter = "all"

    after testsuite:
        python:
            _test.timeout = 5.0

    testcase counters:
        python:
            import datetime as _startup_test_dt
            today = today_tuple()
            yesterday = tuple((_startup_test_dt.date(*today) - _startup_test_dt.timedelta(days=1)).timetuple()[:3])
            future = tuple((_startup_test_dt.date(*today) + _startup_test_dt.timedelta(days=5)).timetuple()[:3])
            add_new_task("Vence hoy")
            tasks[0]["deadline"] = today
            add_new_task("Atrasada")
            tasks[1]["deadline"] = yesterday
            add_new_task("Futura")
            tasks[2]["deadline"] = future
            add_new_task("Sin fecha")
            tasks[3]["deadline"] = None
            add_new_task("Hoy completada")
            tasks[4]["deadline"] = today
            tasks[4]["done"] = True
            add_new_task("Atrasada completada")
            tasks[5]["deadline"] = yesterday
            tasks[5]["done"] = True
            due = {t["title"] for t in quest_due_today_tasks()}
            late = {t["title"] for t in quest_overdue_tasks()}
            assert due == {"Vence hoy"}, due
            assert late == {"Atrasada"}, late

    testcase overdue_first_then_today:
        python:
            import datetime as _startup_test_dt
            today = today_tuple()
            yesterday = tuple((_startup_test_dt.date(*today) - _startup_test_dt.timedelta(days=1)).timetuple()[:3])
            store.persistent.quest_startup_notice = None
            add_new_task("Hoy pendiente")
            tasks[0]["deadline"] = today
            add_new_task("Ayer vencida")
            tasks[1]["deadline"] = yesterday
        python:
            assert quest_maybe_show_startup_notices()
            assert persistent.quest_startup_notice == quest_startup_day_key()
            assert renpy.get_screen("quest_startup_overdue")
            assert renpy.get_screen("quest_startup_due_today")
            # Segunda llamada el mismo día: no repite ni duplica pantallas.
            assert not quest_maybe_show_startup_notices()
        # Cerrar el regaño revela el aviso amable.
        click "Ahora no"
        python:
            assert not renpy.get_screen("quest_startup_overdue"), "regaño cerrado"
            assert renpy.get_screen("quest_startup_due_today"), "aviso amable visible"
        click "Ver tareas"
        python:
            assert not renpy.get_screen("quest_startup_due_today")
            assert store.task_filter == "today", store.task_filter

    testcase today_only_and_empty:
        python:
            import datetime as _startup_test_dt
            today = today_tuple()
            yesterday = tuple((_startup_test_dt.date(*today) - _startup_test_dt.timedelta(days=1)).timetuple()[:3])
            store.persistent.quest_startup_notice = None
            store.tasks = []
            add_new_task("Solo para hoy")
            tasks[0]["deadline"] = today
        run Function(quest_maybe_show_startup_notices)
        python:
            assert renpy.get_screen("quest_startup_due_today")
            assert not renpy.get_screen("quest_startup_overdue"), "no hay atrasadas"
        click "Ahora no"
        python:
            assert not renpy.get_screen("quest_startup_due_today")
            # Sin pendientes: nada aparece y la bandera no se marca.
            store.tasks = []
            store.persistent.quest_startup_notice = None
            assert not quest_maybe_show_startup_notices()
            assert persistent.quest_startup_notice is None, persistent.quest_startup_notice
            # Tareas pendientes sin fecha tampoco muestran avisos.
            add_new_task("Eterna")
            tasks[-1]["deadline"] = None
            assert not quest_maybe_show_startup_notices()
            _test.timeout = 5.0

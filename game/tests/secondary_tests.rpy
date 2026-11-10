# Usar un directorio aislado; nunca escribir pruebas sobre los datos personales.
testsuite secondary:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            _test.timeout = 25.0
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            quest_setting("school_stage", "primaria")
            store.tasks = []
            store.task_lists = ["General"]
            store.current_list = "General"
            store.task_filter = "all"
            store.completed_tasks = 0
            store.world_progress = {}
            store.stage_themes = {"primaria": "bosque", "secundaria": "mecha"}
            select_quest_theme("bosque")
            renpy.run(Preference("font size", 1.0))
            quest_setting("quest_motion", "off")
            quest_setting("quest_guide_enabled", True)

    after testcase:
        python:
            quest_navigate()
            quest_setting("school_stage", "primaria")
            renpy.run(Preference("font size", 1.0))

    after testsuite:
        python:
            _test.timeout = 5.0
            quest_setting("quest_motion", "normal")

    testcase migration_and_stage_memory:
        python:
            add_new_task("Tarea anterior")
            add_subtask(0, "Paso completado antes de actualizar")
            toggle_subtask(0, 0)
            old_tasks = quest_document()["tasks"]
            legacy = quest_document()
            legacy["version"] = 1
            legacy["theme"] = "océano"
            for field in ("stage", "stage_themes", "world_progress"):
                legacy.pop(field, None)
            persistent.quest_document = legacy
            assert restore_quest_data()
            assert current_theme == "océano" and not quest_secondary()
            quest_setting("school_stage", "secundaria")
            assert current_theme == "mecha"
            assert set(quest_stage_themes()) == {"mecha", "arcane", "stage"}
            select_quest_theme("arcane")
            select_quest_theme("bosque")
            assert current_theme == "arcane"
            quest_setting("school_stage", "primaria")
            assert current_theme == "océano" and len(quest_stage_themes()) == 7
            quest_setting("school_stage", "secundaria")
            assert current_theme == "arcane"
            assert quest_document()["tasks"] == old_tasks
            quest_begin_expedition(0)
            assert quest_world_balance("arcane") == 0
            assert tasks[0]["subtasks"][0]["fruit"]
            snapshot = quest_document()
            save_quest_data()
            store.tasks = []
            store.current_theme = "bosque"
            assert restore_quest_data()
            assert quest_document() == snapshot
            migrate_quest_data()
            migrate_quest_data()
            assert quest_document() == snapshot

    testcase lifecycle_resources_recurrence:
        python:
            quest_setting("school_stage", "secundaria")
            add_new_task("Proyecto de ciencias", recurrence={"freq": "diaria", "days": [], "time": ""})
            for title in ("Investigar", "Preparar", "Revisar"):
                add_subtask(0, title)
            # Cada paso nace con identidad propia, sin depender de la migración.
            assert all(step.get("id") for step in tasks[0]["subtasks"])
            complete_task(0)
            assert not tasks[0]["done"]
            toggle_subtask(0, 0)
            assert not tasks[0]["subtasks"][0]["done"]
            quest_begin_expedition(0)
            quest_pause_expedition(0)
            toggle_subtask(0, 0)
            assert not tasks[0]["subtasks"][0]["done"]
            quest_begin_expedition(0)
            complete_task(0)
            assert not tasks[0]["done"]
            select_quest_theme("stage")
            for j in range(3):
                toggle_subtask(0, j)
                assert tasks[0]["subtasks"][j]["reward_world"] == "mecha"
            assert quest_world_balance("mecha") == 3
            toggle_subtask(0, 0)
            toggle_subtask(0, 0)
            assert quest_world_balance("mecha") == 3
            quest_unlock_upgrade("mecha", 0)
            quest_unlock_upgrade("mecha", 0)
            quest_unlock_upgrade("mecha", 1)
            assert quest_world_balance("mecha") == 0
            assert world_progress["mecha"]["upgrades"] == [0]
            complete_task(0)
            assert tasks[0]["done"] and tasks[0]["expedition"]["state"] == "finished"
            assert len(tasks) == 2 and tasks[1]["expedition"]["state"] == "planned"
            assert tasks[1]["expedition"]["world"] == "mecha"
            assert all(not step.get("fruit") for step in tasks[1]["subtasks"])
            complete_task(0)
            assert tasks[0]["expedition"]["state"] == "paused"
            quest_begin_expedition(0)
            complete_task(0)
            assert len(tasks) == 2 and quest_world_balance("mecha") == 0
            save_quest_data()
            snapshot = quest_document()
            assert restore_quest_data() and quest_document() == snapshot
            quest_setting("school_stage", "primaria")
            assert world_progress["mecha"]["upgrades"] == [0]
            quest_setting("school_stage", "secundaria")
            assert world_progress["mecha"]["upgrades"] == [0]

    testcase startup_stage_preserves_document:
        python:
            add_new_task("Conservar desde el menú inicial")
            add_subtask(0, "No perder este paso")
            snapshot = quest_document()["tasks"]
            previous_menu = store.main_menu
            try:
                store.main_menu = True
                store.tasks = []
                quest_setting("school_stage", "secundaria")
                assert quest_document()["tasks"] == snapshot
                assert persistent.quest_document["tasks"] == snapshot
                assert current_theme == "mecha"
                quest_setting("school_stage", "primaria")
                assert persistent.quest_document["tasks"] == snapshot
                # Sin documento previo, elegir etapa no debe saltar la presentación.
                persistent.quest_document = None
                store.tasks = []
                quest_setting("school_stage", "secundaria")
                assert persistent.quest_document is None
            finally:
                store.main_menu = previous_menu

    testcase legacy_conversion:
        python:
            store.world_progress = {}
            add_new_task("Tarea de primaria")
            add_subtask(0, "Paso heredado")
            assert tasks[0].get("expedition") is None
            quest_select_stage("secundaria")
            # La pregunta aparece; sin conversión las tareas siguen usables.
            assert renpy.get_screen("quest_convert_tasks")
            assert quest_tasks_without_expedition() == [tasks[0]]
            toggle_subtask(0, 0)
            assert tasks[0]["subtasks"][0]["done"]
            complete_task(0)
            assert tasks[0]["done"]
            # La conversión explícita respeta lo ya logrado.
            quest_convert_all_tasks()
            assert tasks[0]["expedition"]["state"] == "finished"
            assert not quest_tasks_without_expedition()
            renpy.hide_screen("quest_convert_tasks")

    testcase mecha_flow:
        click "Menú"
        click "Opciones"
        click "Secundaria · 12 a 15 años"
        screenshot "secondary-options"
        click "Volver"
        python:
            add_new_task("Preparar exposición")
            add_subtask(0, "Elegir el tema")
        click "Ver pasos"
        screenshot "secondary-mecha-planning"
        click "Iniciar misión"
        assert screen "quest_expedition_scene"
        screenshot "secondary-mecha-departure"
        click "Continuar"
        click "Completar"
        python:
            assert tasks[0]["subtasks"][0]["done"]
        screenshot "secondary-mecha-resource"
        click "Finalizar misión"
        assert screen "quest_expedition_scene"
        screenshot "secondary-mecha-return"
        click "Continuar"
        click "Menú"
        click "Expediciones"
        click "Historial"
        screenshot "secondary-history"
        click "Mi base"
        screenshot "secondary-base"

    testcase arcane_flow:
        python:
            quest_setting("school_stage", "secundaria")
        click "Menú"
        click "Cambiar mundo"
        screenshot "secondary-world-selector"
        click "Academia Arcana"
        python:
            assert current_theme == "arcane"
            assert quest_music_track() == QUEST_THEME_MUSIC["arcane"]
            add_new_task("Proyecto de historia")
            add_subtask(0, "Revisar mis fuentes")
            renpy.restart_interaction()
        pause 0.3
        screenshot "secondary-arcane-tasks"
        click "Ver pasos"
        click "Iniciar misión"
        screenshot "secondary-arcane-departure"
        click "Continuar"
        click "Completar"
        screenshot "secondary-arcane-resource"
        click "Plan y reflexión"
        screenshot "secondary-arcane-plan"
        click "Guardar"
        click "Menú"
        click "Expediciones"
        screenshot "secondary-arcane-map"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "secondary-arcane-options-large"

    testcase stage_flow:
        python:
            quest_setting("school_stage", "secundaria")
        click "Menú"
        click "Cambiar mundo"
        screenshot "secondary-world-selector"
        click "Camino al Escenario"
        python:
            assert current_theme == "stage"
            assert quest_music_track() == QUEST_THEME_MUSIC["stage"]
            add_new_task("Proyecto de historia")
            add_subtask(0, "Revisar mis fuentes")
            renpy.restart_interaction()
        pause 0.3
        screenshot "secondary-stage-tasks"
        click "Ver pasos"
        click "Iniciar misión"
        screenshot "secondary-stage-departure"
        click "Continuar"
        click "Completar"
        screenshot "secondary-stage-resource"
        click "Plan y reflexión"
        screenshot "secondary-stage-plan"
        click "Guardar"
        click "Menú"
        click "Expediciones"
        screenshot "secondary-stage-map"
        click "Menú"
        click "Opciones"
        click "Más grande"
        screenshot "secondary-stage-options-large"

    testcase plan_notes:
        python:
            quest_setting("school_stage", "secundaria")
        python:
            # La migración crea la clave vacía en expediciones antiguas.
            add_new_task("Proyecto de notas")
            add_subtask(0, "Primera nota")
            del tasks[0]["expedition"]["notes"]
            migrate_quest_data()
            assert tasks[0]["expedition"]["notes"] == "", "migracion notas"
        run Show("task_detail_screen", i=0)
        click "Plan y reflexión"
        assert screen "quest_expedition_plan"
        python:
            assert store.expedition_notes_draft == "", "borrador nace vacío"
            # Sin ambigüedad de placeholder: solo Notas queda por escribir.
            store.expedition_goal_draft = "Meta del proyecto"
            store.expedition_reflection_draft = "Retro del proyecto"
            renpy.restart_interaction()
        # Escritura real en el editor: debe llegar completa a la pantalla
        # (pixel_width recortaba la entrada a ~34 caracteres).
        click "Toca para escribir…"
        assert screen "quest_text_editor"
        python:
            _test.timeout = 30.0
        type "Notas escritas con teclado real para validar el tope largo"
        click "Listo"
        python:
            _notes_typed = "Notas escritas con teclado real para validar el tope largo"
            assert len(store.expedition_notes_draft) == len(_notes_typed), ("editor notas", len(store.expedition_notes_draft))
        python:
            store.expedition_notes_draft = "A" * 500
            renpy.restart_interaction()
        click "Guardar"
        python:
            assert tasks[0]["expedition"]["notes"] == "A" * 500, ("500 exactos", len(tasks[0]["expedition"]["notes"]))
            # Más de 500 se recorta al guardar (defensa por si otro camino edita el draft).
            store.expedition_notes_draft = "B" * 520
            quest_save_plan(0)
            assert tasks[0]["expedition"]["notes"] == "B" * 500, ("recorte", len(tasks[0]["expedition"]["notes"]))
            store.expedition_notes_draft = ""
            quest_open_plan(0)
            assert store.expedition_notes_draft == "B" * 500, ("recarga", len(store.expedition_notes_draft))
            renpy.hide_screen("quest_expedition_plan")
            # Las notas sobreviven guardar/restaurar.
            saved = quest_document()
            store.tasks = []
            assert restore_quest_data()
            assert quest_document() == saved, "restore notas"
            assert tasks[0]["expedition"]["notes"] == "B" * 500
        run Hide("task_detail_screen")

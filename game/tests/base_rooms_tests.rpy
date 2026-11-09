testsuite base_rooms:
    before testcase:
        python:
            assert "runtime-saves" in config.savedir.replace("\\", "/")
            _test.timeout = 25.0
        run Jump("main_menu_todo")
        python:
            quest_navigate()
            quest_setting("school_stage", "secundaria")
            select_quest_theme("mecha")
            store.tasks = []
            store.world_progress = {"mecha": {"earned": ["a", "b", "c", "d", "e", "f", "g", "h", "i"], "upgrades": []}}
            quest_setting("quest_motion", "off")

    testcase unlock_and_reuse:
        python:
            assert not quest_base_available("mecha", 1)
            quest_unlock_upgrade("mecha", 1)
            quest_unlock_upgrade("mecha", 1)
            assert quest_world_balance("mecha") == 6
            assert quest_base_available("mecha", 1)
            add_new_task("Proyecto [original]")
            add_subtask(0, "Un paso")
            tasks[0]["done"] = True
            tasks[0]["subtasks"][0]["done"] = True
            tasks[0]["expedition"]["goal"] = "Aprender"
            tasks[0]["expedition"]["reflection"] = "Funcionó dividir los pasos"
            save_quest_data()
            source = quest_document()["tasks"][0]
            quest_base_reuse("mecha", 1, source["id"])
            assert len(tasks) == 2
            assert tasks[1]["id"] != source["id"]
            assert tasks[1]["subtasks"][0]["id"] != source["subtasks"][0]["id"]
            assert not tasks[1]["subtasks"][0]["done"] and not tasks[1]["reminder"]
            assert tasks[1]["expedition"]["goal"] == "Aprender"
            assert tasks[1]["expedition"]["reflection"] == ""
            assert quest_world_balance("mecha") == 6
            assert quest_document()["tasks"][0] == source
            assert quest_base_indices("mecha", "planned") == [1]
            assert quest_base_indices("mecha", "finished") == [0]
            quest_unlock_upgrade("mecha", 0)
        run Function(quest_base_open, "mecha", 0)
        assert screen "quest_base_room"
        screenshot "base-planning"
        click "Volver a mi base"
        run Function(quest_base_open, "mecha", 1)
        screenshot "base-library"
        click "Volver a mi base"

    testcase rest_and_restore:
        python:
            quest_unlock_upgrade("mecha", 2)
            for minutes in (5, 10, 15):
                quest_base_start_rest("mecha", 2, minutes)
                assert minutes*60-1 <= quest_base_rest_remaining("mecha") <= minutes*60
                deadline = world_progress["mecha"]["rest_until"]
                assert quest_base_rest_remaining("mecha", deadline-30) == 30
                assert quest_base_rest_remaining("mecha", deadline+1) == 0
                snapshot = quest_document()
                store.world_progress = {}
                assert restore_quest_data() and quest_document() == snapshot
            before = world_progress["mecha"]["rest_until"]
            quest_base_start_rest("mecha", 2, 2)
            assert world_progress["mecha"]["rest_until"] == before
        run Function(quest_base_open, "mecha", 2)
        screenshot "base-rest"
        click "Terminar pausa"
        click "Descansar 5 minutos"
        click "Terminar pausa"
        click "Volver a mi base"
        python:
            assert "rest_until" not in world_progress["mecha"]
            assert quest_world_balance("mecha") == 6
            assert quest_base_role("arcane", 0) == "library"
            assert quest_base_role("stage", 1) == "rest"
            quest_setting("school_stage", "primaria")
            assert not quest_base_available("mecha", 2)
            _test.timeout = 5.0

    testcase pomodoro_cycle:
        python:
            quest_unlock_upgrade("mecha", 2)
            # Valores inválidos rechazados sin excepción (límites 1-8/5-90/1-30).
            assert not quest_pomodoro_start("mecha", 2, 0, 25, 5)
            assert not quest_pomodoro_start("mecha", 2, 9, 25, 5)
            assert not quest_pomodoro_start("mecha", 2, 4, 3, 5)
            assert not quest_pomodoro_start("mecha", 2, 4, 25, 45)
            # Config mínima para recorrer el ciclo con reloj simulado: 2 bloques
            # de 5 minutos de trabajo y 1 de descanso.
            assert quest_pomodoro_start("mecha", 2, 2, 5, 1)
            state = world_progress["mecha"]["pomodoro"]
            assert state["phase"] == "work" and state["block"] == 1
            deadline = state["ends_at"]
            fresh = quest_pomodoro_state("mecha", deadline - 30)
            assert fresh["state"]["phase"] == "work" and fresh["remaining"] == 30, fresh
            # 1) Termina el trabajo del bloque 1 → descanso.
            turn = quest_pomodoro_state("mecha", deadline)
            assert isinstance(turn, dict), ("turn no es dict", turn)
            assert turn["events"] == ["work_done"], ("turn", turn)
            assert turn["state"]["phase"] == "rest" and turn["state"]["block"] == 1, ("fase", turn)
            rest_end = turn["state"]["ends_at"]
            turn = quest_pomodoro_state("mecha", rest_end)
            assert turn["events"] == ["rest_done"], turn
            assert turn["state"]["block"] == 2 and turn["state"]["phase"] == "work"
            # El último bloque de trabajo cierra el ciclo (no hay descanso final).
            turn = quest_pomodoro_state("mecha", turn["state"]["ends_at"])
            assert turn["events"] == ["finished"], turn
            assert turn["state"] is None and "pomodoro" not in world_progress["mecha"]
        run Function(quest_base_open, "mecha", 2)
        screenshot "base-pomodoro-config"
        click "Empezar pomodoro"
        screenshot "base-pomodoro-active"
        python:
            state = world_progress["mecha"]["pomodoro"]
            assert state["block"] == 1 and state["phase"] == "work", state
            # La configuración usada quedó guardada para la próxima vez.
            assert world_progress["mecha"]["pomodoro_config"] == {"blocks": 2, "work": 5, "rest": 1}, state
        click "Terminar pomodoro"
        python:
            assert "pomodoro" not in world_progress["mecha"]
            # Las pausas 5/10/15 siguen intactas junto al pomodoro.
            quest_base_start_rest("mecha", 2, 10)
            assert world_progress["mecha"]["rest_until"] > 0
            quest_pomodoro_start("mecha", 2, 1, 5, 1)
            assert "rest_until" not in world_progress["mecha"] and "pomodoro" in world_progress["mecha"]
            quest_pomodoro_stop("mecha")
            assert "pomodoro" not in world_progress["mecha"]
            _test.timeout = 5.0

    testcase pomodoro_persistence:
        # El estado pomodoro sobrevive el round-trip JSON del documento.
        python:
            quest_unlock_upgrade("mecha", 2)
            assert quest_pomodoro_start("mecha", 2, 2, 5, 1)
            snapshot = quest_document()
            store.world_progress = {}
            assert restore_quest_data()
            state = world_progress["mecha"]["pomodoro"]
            assert state["phase"] == "work" and state["block"] == 1, state
            assert state["blocks"] == 2 and state["work"] == 5 and state["rest"] == 1, state
            # El reloj simulado sigue avanzando el ciclo tras restaurar.
            deadline = state["ends_at"]
            turn = quest_pomodoro_state("mecha", deadline)
            assert turn["events"] == ["work_done"], turn
            assert turn["state"]["phase"] == "rest" and turn["state"]["block"] == 1, turn
            # En el juego el poll del temporizador guarda cada transición; el
            # test lo replica antes del round-trip.
            save_quest_data()
            # La configuración usada quedó guardada para la próxima vez.
            assert world_progress["mecha"]["pomodoro_config"] == {"blocks": 2, "work": 5, "rest": 1}, state
            saved = quest_document()
            store.world_progress = {}
            assert restore_quest_data() and quest_document() == saved, "round trip"
            quest_pomodoro_stop("mecha")
            assert "pomodoro" not in world_progress["mecha"]
            _test.timeout = 5.0

    testcase world_mappings:
        python:
            for stage in QUEST_SCHOOL_PROFILES:
                quest_setting("school_stage", stage)
                if not quest_secondary():
                    continue
                for world in quest_stage_themes():
                    select_quest_theme(world)
                    store.world_progress[world] = {"earned": list(range(9)), "upgrades": [0, 1, 2]}
                    assert {quest_base_role(world, n) for n in range(3)} == {"planning", "library", "rest"}
                    for number in range(3):
                        assert quest_base_available(world, number)
                    save_quest_data()
                    saved = quest_document()
                    assert restore_quest_data() and quest_document() == saved
            _test.timeout = 5.0

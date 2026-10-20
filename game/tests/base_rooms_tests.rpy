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

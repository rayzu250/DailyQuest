# Aislamiento de pruebas: nunca tocar ni heredar los datos del jugador real.
#
# Ren'Py añade siempre dos ubicaciones de guardado: el --savedir indicado y
# <proyecto>/game/saves. La segunda se fusiona al arrancar con
# renpy.persistent.update(), que corre antes de los bloques init: un init 999
# llega tarde y las suites heredan el persistent de la corrida anterior.
# Este bloque se ejecuta al cargar el script y, en modo test, retira esa
# ubicación antes de cualquier fusión, dejando solo el --savedir aislado.
python early:
    import os
    import sys

    if "test" in sys.argv and "--savedir" in sys.argv:
        _real_persistent_update = renpy.persistent.update

        def _isolated_persistent_update(force_save=False):
            location = getattr(renpy.loadsave, "location", None)
            if location is not None:
                gamedir_saves = os.path.normcase(os.path.join(renpy.config.gamedir, "saves"))
                location.locations = [
                    item for item in location.locations
                    if os.path.normcase(item.directory) != gamedir_saves
                ]
            return _real_persistent_update(force_save)

        renpy.persistent.update = _isolated_persistent_update

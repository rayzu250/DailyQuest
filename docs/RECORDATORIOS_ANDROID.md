# Recordatorios de Android

Trabajo en `codex/android-reminders`, posterior al commit `fe7833c` de Opciones y Guía.

## Uso

- En una tarea, abrir **Hora y recordatorio**, activar **Asignar una hora** y ajustar hora/minuto con botones. No se abre el teclado.
- **Recordarme en el teléfono** activa el aviso. Guardar una hora sin activar este control solo organiza la tarea.
- Para una tarea de una sola vez, asignar también **Fecha** en Mis pasos. Para las recurrentes se usan los días de repetición; su fecha, si existe, indica desde cuándo pueden empezar los avisos.
- La creación de tareas permite recuperar la hora dentro de **Repetir esta tarea…**. Los horarios existentes de partidas antiguas se conservan, pero sus notificaciones empiezan desactivadas.
- En Android, usar **Permitir avisos**. **Permitir horarios puntuales** es opcional: sin ese permiso, Android puede retrasar los avisos. Estos controles también están en Opciones → Otras opciones.
- Tocar una notificación abre la tarea correspondiente. Completar una tarea cancela su aviso; si es recurrente, su próxima copia conserva hora y preferencia de aviso.

Los avisos recurrentes se repiten en los días elegidos aunque la tarea siga pendiente. No se crean copias adicionales hasta completarla. Reabrir una tarea histórica que ya tiene una copia siguiente no duplica los recordatorios de la serie.

Los horarios usan la zona horaria del teléfono. Los días mensuales 29–31 se ajustan al último día de los meses cortos, igual que el calendario del juego. No se envían avisos atrasados de fechas pasadas al arrancar o reiniciar. Android puede suspenderlos al forzar la detención; abrir otra vez la app vuelve a programar los futuros.

## Compilar con Ren’Py 8.5.3

El lanzador estándar no incorpora archivos Java del juego automáticamente. La integración incluye fuentes nativas en `android/native/` y un instalador reproducible de las dos plantillas necesarias:

```powershell
python tools/configure_android_reminders.py
```

El instalador lee el paquete desde el `android.json` local. Guarda los originales junto a las plantillas de RAPT y aplica los cambios solo a ese paquete. Incluye las fuentes desde su ruta absoluta; repetir al mover el proyecto o cambiar de SDK. Si una plantilla se modificó externamente, se detiene para no sobrescribirla.

Después se puede compilar desde el lanzador de Ren’Py o con la ruta completa del proyecto:

```powershell
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py ../../launcher android_build (Get-Location).Path --destination "$((Get-Location).Path)/dist"
```

Para restaurar las plantillas originales:

```powershell
python tools/configure_android_reminders.py --remove
```

Si Windows informa `WinError 32` al retirar una carpeta temporal del SDK, el siguiente lanzador reintenta esa operación durante un máximo de dos segundos por carpeta. No modifica el SDK ni oculta otros errores:

```powershell
& ../../lib/py3-windows-x86_64/python.exe tools/build_android.py
```

Las claves de firma y `android.json` se mantienen como archivos locales. No se incluyen en este cambio. Las carpetas `android`, `tools` y las pruebas se excluyen de los recursos del juego; Java y el icono se incorporan mediante Gradle.

## Diseño y persistencia

- `game/core/reminders.rpy`: validación, migración de horarios y puente Pyjnius; en PC no llama a Android.
- `game/ui/reminders.rpy`: editor accesible y controles de permisos.
- `Reminders.java`: canal, permisos, sincronización, alarmas y notificaciones. Un identificador estable por tarea evita colisiones de alarmas. El último aviso emitido evita duplicados.
- `ReminderClock.java`: calcula el próximo horario local, sin dependencia de Android.
- `ReminderReceiver.java`: atiende alarmas, reinicio, actualización y cambios de reloj/zona horaria.
- `ReminderOpenActivity.java`: lleva el identificador de la notificación a Ren’Py tanto en arranque frío como con el juego abierto.

La programación se guarda en preferencias privadas de Android, así que no requiere internet ni mantener Python activo. Las operaciones de guardado sincronizan los avisos. Cambiar o desactivar un horario elimina la alarma anterior; los avisos ya visibles se retiran cuando cambia o se completa su tarea. Una pantalla de error informa si falta el componente nativo o falla la programación.

## Validación

Pruebas automáticas incluidas: migración de horas antiguas, activación/desactivación, persistencia, transferencia a la siguiente tarea, reapertura sin duplicados y edición/cancelación del formulario. El cálculo Java cubre horario vencido, límites, lunes, mes corto bisiesto y fechas inválidas.

La comprobación en teléfono debe cubrir:

1. Una tarea con fecha de hoy y hora a unos minutos, app en segundo plano y pantalla bloqueada.
2. Permiso de notificaciones aceptado y rechazado; canal desactivado; horarios puntuales permitidos y desactivados.
3. Tocar el aviso con el juego cerrado y con otra pantalla abierta; debe mostrar la tarea correcta.
4. Editar, desactivar o completar antes de la hora; no debe aparecer el aviso antiguo.
5. Reiniciar el teléfono y comprobar que el siguiente aviso sigue programado.
6. Repetición diaria/semanal/mensual y cancelación de su repetición.
7. Actualizar sobre la versión instalada, conservando las tareas existentes.

El 24 de septiembre de 2026 el usuario confirmó que las notificaciones funcionan correctamente en su HONOR Magic6 Lite y autorizó el commit. Durante la revisión de sus capturas se identificaron desactivadas las opciones de visualización «Pantalla de bloqueo» y «Tiras». Además de permitir notificaciones, conviene habilitar esas opciones para ver los avisos en esas superficies. La confirmación del usuario no especifica cuáles de los escenarios anteriores se probaron individualmente.

Validación local: lint de Ren’Py, nueve pruebas del juego y once comprobaciones del reloj Java correctos; fuentes nativas compiladas contra Android 36. El intento de generación del APK desde el entorno del asistente llegó a Gradle pero quedó bloqueado por `Unable to establish loopback connection` / `Invalid argument: connect` en Java 21 sobre este Windows. La posterior prueba del usuario en su teléfono fue satisfactoria. Los manifiestos generados contienen el receptor, la actividad y los tres permisos necesarios. Los registros locales quedan en `tests/android-build.log` y `tests/android-gradle.log` (no versionados).

Referencias: [alarmas de Android](https://developer.android.com/develop/background-work/services/alarms), [notificaciones](https://developer.android.com/develop/ui/views/notifications/build-notification), [Pyjnius en Ren’Py](https://www.renpy.org/doc/html/android.html#pyjnius).

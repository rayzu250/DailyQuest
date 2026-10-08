# Cambios para revisión funcional

## Implementado

- Código separado en `game/core` y `game/ui`, manteniendo nombres de funciones y etiquetas de compatibilidad.
- Editor compartido para nombre, tarea, paso y lista. El borrador se confirma con Listo o se descarta con Cancelar. No usa interacciones anidadas de `renpy.input` en los formularios.
- La entrada se activa al abrir el editor o tocar el campo. Enter termina la edición; Listo confirma el texto. Atrás desactiva primero la edición y después permite cancelar el editor. El cierre en un teclado nativo requiere validación en Android.
- Formularios sin campos fuera del marco, botones con palabras, validación de nombres vacíos y listas duplicadas.
- Inicio de tareas con Todas, Hoy y Sin fecha, dentro de la lista seleccionada. Hoy incluye pendientes vencidos; las completadas quedan al final de Todas.
- Navegación común que cierra las páginas anteriores; editor y menús tienen prioridad visual explícita.
- Repetición opcional y selección de días; ya no se solicita una hora que no genera notificaciones.
- Tareas y pasos con IDs, enlace a la siguiente tarea recurrente para impedir duplicación al reabrir, fechas válidas y contador del calendario basado en las mismas entradas que muestra.
- Guardado automático después de cambios de tareas/listas/fechas/repetición/tema. Al iniciar se restaura el documento persistente. Rollback desactivado para evitar deshacer pendientes accidentalmente.
- Confirmación antes de borrar un paso o una lista; al borrar una lista sus tareas se conservan en otra.

## Pruebas realizadas

Con Ren'Py 8.5.3, en Windows y con guardados de prueba separados:

- Lint final del motor, sin errores.
- `quest.data_integrity`: fechas inválidas, año bisiesto, repetición mensual y semanal, completar/reabrir/recompletar, mover/renombrar/borrar listas, migración repetida y restauración del documento.
- `quest.text_and_navigation`: escritura real simulada, aceptar/cancelar, crear tarea/paso/lista, navegar, cambiar tema y renderizar calendario, progreso y repetición.
- `quest_restore`, en otro proceso: recuperación desde disco de tarea, paso, lista y tema.
- Capturas de las pantallas revisadas para detectar solapamientos. Se guardan localmente en `tests/screenshots/` y no se incluyen en Git ni en la distribución.

Comandos desde la carpeta DailyQuest (PowerShell):

```powershell
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py . lint
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py . test quest --savedir tests/runtime-saves --overwrite-screenshots
& ../../lib/py3-windows-x86_64/python.exe ../../renpy.py . test quest_restore --savedir tests/runtime-saves
```

Cerrar la ventana de pruebas después de ver el informe. La prueba de restauración se ejecuta después de la suite quest. Los tests se excluyen del paquete del juego y comprueban que se use una carpeta de prueba antes de modificar datos.

## Validación pendiente en el celular

1. Abrir y cancelar el editor en nombre, tarea, paso, creación de lista y cambio de nombre. Ninguno debe conservar cambios cancelados.
2. Escribir usando acentos y ñ. Pulsar Listo: el teclado debe desaparecer y el texto quedar en el formulario.
3. Probar el botón del teclado y Atrás de Android. Volver a tocar el campo debe permitir escribir de nuevo.
4. Abrir y cerrar el editor varias veces; pasar a calendario y menú. El teclado no debe reaparecer sin solicitar edición.
5. Crear una tarea, un paso y una lista. Cerrar la aplicación y volver a entrar: deben mantenerse.
6. Completar una tarea recurrente, reabrirla y volver a completarla: debe existir una sola copia siguiente.
7. Probar una lista larga, nombres largos y la selección de los últimos días del mes con desplazamiento.

No se ha generado ni instalado un APK en esta entrega. No se ha confirmado el cierre del teclado nativo en un dispositivo Android.

## Compatibilidad y límites

- Las partidas antiguas siguen disponibles mediante Cargar en el menú original de Ren'Py. Al cargar, se completan campos nuevos; la siguiente modificación guarda el estado de esa partida como documento actual.
- No se eliminan duplicados recurrentes ya existentes, porque podrían representar tareas distintas creadas intencionalmente.
- Los índices de pantalla se conservan mientras no hay ordenación destructiva de la colección; los IDs sirven para identidad y enlaces recurrentes. No se ha añadido reordenamiento manual.
- Las listas siguen identificadas por su nombre, con renombrado que actualiza sus tareas. Una migración a IDs de listas se reserva para funcionalidades que la necesiten.
- El diseño conserva el lienzo vertical 1080×1920 de Ren'Py; se reorganizaron sus espacios y zonas desplazables. No se ha implementado rotación horizontal.
- El documento persistente tiene versión 1. No se ha añadido sincronización con Google Tasks ni avisos del sistema.

Todos los cambios quedan sin commit para revisión del usuario.

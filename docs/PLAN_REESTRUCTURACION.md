# DailyQuest: análisis y plan de mejora

Fecha: 23 de septiembre de 2026.

## Objetivo y alcance

Ayudar a un niño a ver sus pendientes, dividirlos en pasos y completarlos con poca ayuda. Conservar tareas, listas, calendario, temas y recompensas, mostrando las opciones complejas solo cuando sean necesarias.

Este documento se basa en una revisión estática de los ocho archivos RPY, README y configuración Android. No se ha ejecutado el APK ni reproducido el fallo del teclado en un dispositivo. Las causas relacionadas con Android son hipótesis que deben verificarse; los problemas de estructura indicados abajo sí son observables en el código. Esta entrega es un plan, sin cambios al funcionamiento del juego.

## Hallazgos

| Prioridad | Evidencia | Implicación |
|---|---|---|
| Alta | `todo_data.rpy:381–394` abre `renpy.input()` desde funciones de acciones de pantalla. `screens.rpy:173–185` presenta únicamente el mensaje y el campo. | En móvil no hay una salida visible «Listo/Cancelar» en el editor. Revisar interacción, foco y cierre del teclado juntos. |
| Alta | `todo_screens.rpy:917`, `1032` y `1072`: el campo/botón está fuera del `frame` por su indentación; el marco queda vacío. | Los límites de ancho y el relleno previstos no contienen esos campos. Riesgo de desbordamiento y controles desplazados, especialmente con texto largo. |
| Alta | La navegación combina `Show`, `Hide`, pantallas modales y un único `tag menu` en `main_todo`. | No hay una política uniforme para sustituir páginas y volver. Una pantalla modal bloquea interacción, pero no equivale a retirar las anteriores. |
| Alta | `complete_task()` crea una copia recurrente al completar; reabrir conserva esa copia. | Completar → reabrir → completar vuelve a generar otra copia pendiente. |
| Alta | El estado de tareas usa `default`; no hay un servicio de guardado propio después de cada modificación. | Debe verificarse recuperación al cerrar/reabrir o al terminar Android el proceso. `default` por sí solo no garantiza persistencia inmediata. |
| Media | `todo_screens.rpy` tiene 1.318 líneas con estilos, navegación, formularios y calendario; `todo_data.rpy` mezcla datos, notificaciones, sonidos y entrada de texto. | Cambiar una función requiere tocar responsabilidades distintas y repetir lógica. |
| Media | `todo_system.rpy` conserva flujo por diálogos y define `tasks`; el flujo de inicio actual llama a `view_tasks_screen`. | No se puede retirar el archivo antiguo sin mover antes el estado compartido y buscar referencias a sus etiquetas. |
| Media | Formularios guardan borradores y selectores en variables globales; acciones de guardar/cancelar repiten listas extensas de cambios. | Riesgo de llevar texto o selección de una tarea a otra y de reinicios inconsistentes. |
| Media | El diseño base es vertical 1080×1920; abundan posiciones y tamaños fijos. La lista ocupa 480 unidades de alto mientras el botón inferior está a 90% de la pantalla. | Espacio desaprovechado y adaptación insuficiente al teclado y a distintas proporciones. |
| Media | Crear tarea cierra y limpia el formulario aunque el título esté vacío; la función simplemente no agrega nada. | Para el niño parece que guardó algo que desapareció. Se necesita validación visible. |
| Media | `valid_date()` solo valida contenedor y longitud, no una fecha real. | Fechas inválidas pueden llegar a formateo o cálculos de recurrencia. |
| Media | El calendario suma vencimientos y recurrencias por separado; luego evita algunas filas duplicadas. | El contador puede no coincidir con las tareas mostradas. Unificar la consulta y definir si se cuentan tareas o pasos. |
| Media | La hora de recurrencia se almacena y se muestra, sin un planificador de avisos observado. | No presentar la hora como promesa de notificación. Los avisos Android serían una función independiente. |

## Diseño propuesto para niños

- Inicio «Mis tareas», con accesos visibles a «Hoy», «Mis listas» y «Mis logros». Ajustes y calendario quedan como opciones secundarias.
- En «Hoy», mostrar pendientes de hoy y atrasados con lenguaje amable. Dar acceso explícito a «Sin fecha» para que ninguna tarea quede escondida.
- Tarjeta de tarea con título, progreso de pasos y una acción principal «Completar». Tocar el título abre el detalle; mover y otras opciones van en un menú secundario.
- Crear tarea: título y botón «Guardar tarea». «Fecha» y «Repetir» se despliegan a demanda; la lista actual se usa como valor inicial.
- Fechas rápidas «Hoy», «Mañana», «Elegir día». Repetición con opciones comprensibles, por ejemplo «Cada día» o «Elegir días».
- Usar «Pasos» en la interfaz en lugar de «Subtareas», y elegir un término consistente para tarea; evitar alternar entre proyecto, misión y tarea sin necesidad.
- Botones con icono y palabra, no solo ✓, ✕ o ↩. Las acciones de borrar deben permitir deshacer o pedir confirmación contextual.
- Reservar una zona inferior estable para la acción principal y usar el espacio central disponible con desplazamiento vertical.
- Mantener recompensas breves y no bloquear el siguiente paso. Evitar depender únicamente del color para representar estados. Revisar legibilidad en todos los temas y disponibilidad real de los iconos.
- Ajustar texto y densidad cuando se conozcan la edad y autonomía lectora del niño. No convertir todavía un «modo adulto» en requisito.

## Teclado Android: primer incremento

1. Registrar el caso exacto: dispositivo, versión Android, teclado, campo afectado y secuencia que deja el teclado abierto. Verificar que el APK corresponde al código revisado.
2. Crear un editor de texto reutilizable para nombre, tarea, paso y lista, con borrador local y botones visibles «Listo» y «Cancelar» por encima del teclado.
3. Activar edición solo al tocar el campo. Para entradas basadas en `InputValue`, usar activación/desactivación explícita y comprobar `DisableAllInputValues()` al salir. Esta acción no constituye por sí sola una garantía de cierre de cualquier teclado nativo.
4. Finalizar la interacción de entrada al aceptar/cancelar, retirar la pantalla correspondiente y comprobar que no queda otra entrada activa debajo. No limitar la solución a ocultar el teclado mientras el campo sigue reclamándolo.
5. Acordar comportamiento consistente: «Listo» confirma el texto; «Cancelar» descarta la edición; tocar fuera del campo termina la edición sin guardar una tarea; Atrás primero cierra el teclado si está visible y después permite salir del editor. Validar cómo entrega Android ese evento para evitar un doble retroceso.
6. Corregir los tres marcos vacíos y asegurar que textos largos no desplazan los botones. La acción para guardar una tarea completa será distinta de terminar de escribir su título.
7. Comprobar Enter/acción del teclado, volver a editar, abrir calendario y cambiar de pantalla. Evitar temporizadores o llamadas privadas al motor como primera solución.

La documentación oficial describe `InputValue.Enable/Disable` y `DisableAllInputValues`, y advierte de limitaciones de entrada en Android. La documentación web consultada corresponde a 8.5.4; contrastar cualquier implementación con el SDK local 8.5.3. No se requiere actualizar el motor como paso inicial.

## Estructura propuesta

```text
game/
  script.rpy                 # Inicio y flujo principal
  options.rpy                # Configuración del motor
  gui.rpy                    # Parámetros visuales generales
  screens.rpy                # Pantallas estándar que se conserven
  core/
    state.rpy                # Estado de usuario y versión de datos
    tasks.rpy                # Operaciones de tareas, pasos y listas
    dates.rpy                # Fechas y consultas de calendario
    recurrence.rpy           # Series y ocurrencias
    storage.rpy              # Guardar y recuperar estado
    migrations.rpy           # Compatibilidad con datos anteriores
  ui/
    styles.rpy               # Tamaños, colores y estilos compartidos
    components.rpy           # Tarjetas, cabecera y botones
    navigation.rpy           # Página activa y vuelta coherente
    text_editor.rpy          # Entrada de texto y foco
    tasks.rpy                # Inicio y detalle
    task_form.rpy            # Crear/editar tarea
    lists.rpy                # Gestión de listas
    calendar.rpy             # Calendario y selector de fecha
    progress.rpy             # Progreso y recompensas
  presentation/
    themes.rpy               # Temas
    guide.rpy                # Guía, animaciones y sonidos
```

Las carpetas organizan archivos, pero no crean espacios de nombres en Ren'Py. Conservar nombres existentes durante la extracción, declarar cada estado una sola vez y respetar las prioridades de inicialización. No mover todo y cambiar el comportamiento en el mismo incremento.

Las pantallas gestionarán borradores locales y llamarán operaciones del dominio. Estas devolverán resultados claros (éxito, error y recompensa) para que la presentación muestre mensajes. Introducir identificadores estables para tareas, pasos y listas antes de incorporar reordenamiento o borrado más amplio; los índices actuales son posiciones, no identidades.

## Orden de ejecución y criterios de aceptación

| Etapa | Entrega | Se considera terminada cuando… |
|---|---|---|
| 0. Referencia | Inventario, copia de datos de prueba y recorrido de las funciones actuales. | Se conoce la secuencia del fallo Android y existe una base para comparar sin borrar datos del usuario. |
| 1. Entrada móvil | Editor común, cierre de interacción, corrección de marcos y validación de vacíos. | Los cinco casos de entrada (nombre, tarea, paso, crear lista, renombrar lista) permiten aceptar/cancelar y no dejan teclado abierto al abandonar el editor. |
| 2. Separación interna | Extraer estado, operaciones, componentes y navegación por partes. | No quedan definiciones duplicadas ni referencias rotas; la funcionalidad previa sigue disponible. Retirar el flujo antiguo solo después de mover `tasks`. |
| 3. Integridad y guardado | IDs, migraciones versionadas, recurrencia sin duplicación y guardado automático. | Completar/reabrir no duplica la siguiente ocurrencia; guardar y restaurar conserva tareas y recompensas; una actualización carga datos anteriores. |
| 4. Interfaz infantil | Inicio simplificado, formularios progresivos y tarjetas legibles. | El niño puede encontrar, crear y completar una tarea sin instrucciones paso a paso; botones y texto no se tapan. |
| 5. Validación Android | APK de prueba y registro de resultados en dispositivos. | Pasa la matriz siguiente y el recorrido de escritorio no presenta regresiones. |

Para persistencia, elegir un único estado canónico y un punto de guardado después de cada operación válida. Evaluar un slot de aplicación controlado frente a un documento de datos versionado con escritura segura; comprobar restauración fuera de un formulario abierto. Evitar mantener copias divergentes en `store` y `persistent`. Definir cómo se desactiva o limita rollback para que no deshaga pendientes accidentalmente, manteniendo «Deshacer» explícito.

## Validación prevista

- Ejecutar lint de Ren'Py tras cambios de código, y recorridos de inicio, tareas, pasos, listas, calendario, temas y recompensas.
- Pruebas de lógica: mes de febrero y año bisiesto, día 31, semana sin días elegidos, completar/reabrir/recompletar, títulos vacíos, renombrar y eliminar listas con tareas.
- Cargar una partida anterior y ejecutar la migración dos veces sin duplicaciones ni pérdida de datos.
- Android: al menos el dispositivo reportado; si está disponible, otro tamaño de pantalla y otro teclado. Probar acentos, ñ, pegado, títulos largos, borrar todo, pulsar Listo, Cancelar y Atrás.
- Abrir/cerrar el editor repetidamente; pasar de escritura a calendario/listas; enviar la app al fondo y reanudar; terminar el proceso después de un guardado confirmado y recuperar los cambios.
- Prueba de uso acompañada: encontrar un pendiente, añadir un paso, completarlo y corregir un error. Registrar dónde pide ayuda antes de añadir nuevas funciones.

El emulador de variantes móviles en escritorio sirve para distribución visual, pero no demuestra que el teclado real de Android cierre correctamente. No se han ejecutado estas pruebas en esta entrega de análisis.

## Fuentes técnicas

- [Ren'Py: acciones e InputValue](https://www.renpy.org/doc/html/screen_actions.html#DisableAllInputValues).
- [Ren'Py: Android y sus limitaciones](https://www.renpy.org/doc/html/android.html).
- SDK local: `renpy/exports/inputexports.py` y `renpy/display/behavior.py`, revisados para ubicar interacción y estado editable.

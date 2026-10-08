# Opciones y acompañamiento para Primaria

## Cambios disponibles

- Opciones usa letras grandes, barras de volumen anchas y una sola columna desplazable. El contenido es el mismo desde el inicio y desde el menú de tareas.
- En el menú, Opciones aparece antes de Cerrar menú. Abrir y cerrar el panel conserva la página y los borradores.
- Música, efectos y Silenciar todo están al principio. El tamaño de letra tiene dos niveles independientes de la etapa escolar.
- La etapa disponible es Primaria (6 a 12 años). El registro `QUEST_SCHOOL_PROFILES` en `game/core/settings.rpy` permite incorporar nuevas etapas cuando tengan funciones implementadas. Cambiar esta preferencia no modifica tareas ni avances.
- Animaciones normales, reducidas o sin movimiento. La opción sin movimiento también desactiva transiciones del motor. El efecto de página requiere modo normal.
- Guía puede ocultarse. Su zona está separada de la lista y del botón principal. Los mensajes no desaparecen automáticamente, para permitir leerlos sin prisa.
- Guía saluda una vez al entrar a las tareas en una nueva sesión, reconoce la creación de tareas y pasos, celebra tareas completas, informa del progreso de pasos y ofrece ayuda a petición.
- Las frutas se conservan, pero desmarcar y volver a completar no vuelve a otorgar la fruta ni reproduce otra celebración. Las tareas ya completadas en partidas anteriores se migran como celebradas.
- Los cambios de preferencias se guardan separados del documento de tareas. Volumen y tamaño se guardan al salir de Opciones, además del guardado normal del motor.

## Criterio de acompañamiento

Se usa lenguaje concreto sobre acciones, esfuerzo y progreso: «Completaste 2 de 3 pasos», sin comparaciones ni castigos por pendientes. Las reacciones son breves; el texto permanece. Se reutilizan las imágenes del proyecto y se encuadran en pantalla sin alterar los archivos originales.

Referencia del enfoque: [CAST, comentarios orientados a la acción](https://udlguidelines.cast.org/engagement/effort-persistence/feedback/). Primaria define el público y el contexto; no implica certificación o alineación formal con el currículo de la SEP.

## Validación realizada

- Lint de Ren'Py 8.5.3.
- Suite general: 7 casos aprobados con `RENPY_VARIANT='small touch mobile'`, ejecutada en Windows con datos separados.
- Pruebas de entrada a Opciones desde inicio y tarea, silencio, modificación de volumen, tamaño de letra, movimiento, opciones secundarias y conservación del borrador.
- Pruebas de saludo único, mensajes de creación, tareas completas y prevención de celebraciones repetidas.
- Recuperación de preferencias y volumen comprobada en otra ejecución.
- Regresión de tareas, pasos, listas, recurrencia y guardado; revisión de capturas con letra ampliada.

## Revisión en Android

1. Inicio → Opciones: leer y ajustar Música y Efectos; probar Silenciar todo.
2. Crear una tarea sin guardarla → Menú → Opciones → Volver: conservar el título.
3. Activar Más grande y recorrer todas las opciones con el dedo.
4. Crear una tarea, agregar un paso y completar ambos; comprobar los mensajes de Guía y que los controles sigan accesibles.
5. Desmarcar y completar el mismo paso: conservar la fruta sin otra celebración.
6. Comparar Normales, Reducidas y Sin movimiento. Ocultar y mostrar a Guía.
7. Cerrar y abrir la aplicación: conservar las preferencias y recibir el saludo al entrar a las tareas.

La variante móvil en escritorio no sustituye la prueba en un teléfono físico. No se generó un APK ni un commit con estos cambios.

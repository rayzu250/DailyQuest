init offset = -1

style todo_button:
    background Frame(Solid("#FFFFFF"), 12, 12)
    hover_background Frame(Solid("#E8F5E9"), 12, 12)
    selected_background Solid("#FFD54F")
    insensitive_background Solid("#B0B8B4")
    padding (42, 28)
    xminimum 460
    yminimum 94
    size_group "todo_buttons"

style todo_button_text:
    size 42
    color "#212121"
    hover_color "#1B5E20"
    font "DejaVuSans.ttf"          # Cambia por la fuente que uses
    textalign 0.5
    xalign 0.5
    yalign 0.5

# Variante compacta para filas con varios botones (grupo propio para no
# heredar el tamaño de los botones grandes)
style todo_button_small is todo_button:
    padding (20, 14)
    xminimum 180
    yminimum 66
    size_group "todo_row_buttons"

style todo_button_small_text is todo_button_text:
    size 26

# Variante para navegación de mes (grupo propio para no heredar el
# tamaño de los botones grandes)
style todo_button_nav is todo_button:
    padding (16, 10)
    xminimum 130
    yminimum 70
    size_group "todo_nav_buttons"

style todo_button_nav_text is todo_button_text:
    size 34

# Variante para chips de recurrencia (grupo propio para no heredar el
# tamaño de los botones grandes)
style todo_button_rec is todo_button:
    padding (20, 12)
    xminimum 100
    yminimum 62
    size_group "todo_rec_buttons"

# Opciones del panel de frecuencia (uniformes entre sí, sin afectar a las chips)
style todo_button_rec_panel is todo_button_rec:
    size_group "todo_rec_panel"

# Botones Fecha/Quitar de detalle (uniformes entre sí)
style todo_button_detail is todo_button:
    padding (16, 10)
    xminimum 120
    yminimum 58
    size_group "todo_detail_buttons"

# Texto grande para botones de icono (✓ / ✕ junto a los inputs)
style todo_button_icon_text is todo_button_text:
    size 48

style todo_title:
    size 64
    color "#FFFFFF"
    bold True
    textalign 0.5
    outlines [(3, "#00000080", 0, 0)]

style todo_text:
    size 40
    color "#FFFFFF"
    textalign 0.5
    outlines [(2, "#00000060", 0, 0)]

style task_item:
    size 38
    color "#FFFFFF"
    outlines [(2, "#00000050", 0, 0)]

style subtask_button:
    background Solid("#FFFFFF22")
    hover_background Solid("#FFFFFF44")
    padding (22, 16)
    xminimum 640

style subtask_text:
    size 38
    color "#FFFFFF"

style cal_day:
    background Solid("#FFFFFF22")
    hover_background Solid("#FFFFFF55")

style cal_day_text:
    size 34
    color "#FFFFFF"

# Botón invisible para cerrar el drawer al tocar fuera
style blank_button is empty

# Botones del panel lateral (grupo propio para no heredar otros tamaños)
style drawer_button:
    background Frame(Solid("#FFFFFF"), 12, 12)
    hover_background Frame(Solid("#FFD54F"), 12, 12)
    padding (20, 12)
    xminimum 360
    yminimum 64
    size_group "todo_drawer_buttons"

style drawer_button_text:
    size 30
    color "#212121"
    hover_color "#1B5E20"
    textalign 0.5
    xalign 0.5
    yalign 0.5

style drawer_button_close is drawer_button

style drawer_button_close_text is drawer_button_text:
    color "#EF5350"


style todo_button_small:
    yminimum 100

style todo_button_rec:
    yminimum 96

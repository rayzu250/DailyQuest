init python:
    class QuestTextValue(ScreenVariableInputValue):
        def enter(self):
            renpy.run(self.Disable())
            renpy.restart_interaction()
            raise renpy.IgnoreEvent()

    def close_text_editor(target, text, accept, onboarding=False):
        renpy.run(DisableAllInputValues())
        if accept:
            setattr(store, target, text.strip())
        if onboarding:
            renpy.end_interaction(True)
        else:
            renpy.hide_screen("quest_text_editor")
        renpy.restart_interaction()

    def editor_back(value, target, onboarding):
        current, editing = renpy.get_editable_input_value()
        if current == value and editing:
            renpy.run(value.Disable())
        else:
            close_text_editor(target, "", False, onboarding)

    def quest_text_needs_break(text):
        # Una cadena sin espacios mรกs larga que esto no cabe en el campo
        # (850 px a size 40) y se sale del cuadro; con "anywhere" se parte
        # donde haga falta. El texto normal conserva el corte por palabras.
        return any(len(token) > 24 for token in (text or "").split())

screen quest_text_editor(target, prompt, limit=60, onboarding=False):
    modal True
    zorder 200
    default draft = getattr(store, target)
    default text_value = QuestTextValue("draft", default=False)
    on "show" action text_value.Enable()
    on "hide" action DisableAllInputValues()
    key "game_menu" action Function(editor_back, text_value, target, onboarding)

    button:
        style "blank_button"
        background Solid("#000000CC")
        xfill True
        yfill True
        action text_value.Disable()

    frame:
        xalign 0.5
        ypos 90
        xsize 980
        padding (32, 30)
        background get_theme_panel()
        vbox:
            spacing 24
            text prompt size 42 color "#FFFFFF"
            button:
                background Solid("#FFFFFF")
                padding (24, 24)
                xfill True
                action text_value.Enable()
                input:
                    value text_value
                    length limit
                    exclude "{}\n\r"
                    size 40
                    color "#152B24"
                    xsize 850
                    layout "subtitle"
                    language ("anywhere" if quest_text_needs_break(draft) else "western")
            text "Toca el texto para escribir." size 28 color "#D5EEE4"
            hbox:
                spacing 24
                textbutton "Listo" style "todo_button_small" text_style "todo_button_small_text" action Function(close_text_editor, target, draft, True, onboarding)
                textbutton "Cancelar" style "todo_button_small" text_style "todo_button_small_text" action Function(close_text_editor, target, draft, False, onboarding)

screen quest_text_field(target, prompt, limit=60):
    $ _field_text = getattr(store, target) or "Toca para escribir…"
    textbutton _field_text:
        substitute False
        background Solid("#FFFFFF")
        padding (24, 24)
        xfill True
        text_color "#152B24"
        text_size 38
        text_layout "subtitle"
        text_language ("anywhere" if quest_text_needs_break(_field_text) else "western")
        action Show("quest_text_editor", target=target, prompt=prompt, limit=limit)

init python:
    # Alterna un día en el selector del formulario (reasigna para refrescar)
    def toggle_new_rec_day(d):
        days = list(store.new_rec_days)
        if d in days:
            days.remove(d)
        else:
            days.append(d)
        store.new_rec_days = days

    def bump_new_rec_h(d):
        store.new_rec_h = (store.new_rec_h + d) % 24

    def bump_new_rec_m(d):
        store.new_rec_m = (store.new_rec_m + d) % 60

from datetime import date


class AppState:

    def __init__(self):

        heute = date.today()

        self.jahr = heute.year
        self.monat = heute.month

        self.standort = "Gesamt"

        self.monatsstatus = "In Bearbeitung"


app_state = AppState()
from datetime import date
d=date.today()
class AppState:
    def __init__(self):
        self.jahr=d.year
        self.monat=d.month
        self.standort="Gesamt"
        self.monatsstatus="In Bearbeitung"
app_state=AppState()

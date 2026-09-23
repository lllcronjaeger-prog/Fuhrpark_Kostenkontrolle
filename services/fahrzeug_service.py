
from database.database import SessionLocal

class FahrzeugService:
    def __init__(self):
        self.session = SessionLocal()

    def kosten_zugmaschine(self, fahrzeug):
        return (
            fahrzeug.monatsmiete +
            fahrzeug.steuer +
            fahrzeug.versicherung +
            fahrzeug.werkstatt_pauschale
        )

    def kosten_trailer(self, trailer):
        return (
            trailer.monatsmiete +
            trailer.steuer +
            trailer.versicherung
        )

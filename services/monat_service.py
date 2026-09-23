# services/monat_service.py
# Release v0.6.6

from database.database import SessionLocal
from database.models import Monat, Monatsdaten, MonatsKennzahlen, Fahrzeug
from ui.app_state import app_state

class MonatService:
    def __init__(self):
        self.session=SessionLocal()

    def hole_oder_erzeuge_monat(self):
        monat=self.session.query(Monat).filter_by(
            jahr=app_state.jahr,
            monat=app_state.monat
        ).first()
        if monat:
            return monat
        monat=Monat(jahr=app_state.jahr,monat=app_state.monat)
        self.session.add(monat)
        self.session.commit()
        return monat

    def hole_oder_erzeuge_kennzahlen(self,standort="Gesamt"):
        monat=self.hole_oder_erzeuge_monat()
        kz=self.session.query(MonatsKennzahlen).filter_by(
            monat_id=monat.id,
            standort=standort
        ).first()
        if kz:
            return kz
        kz=MonatsKennzahlen(monat_id=monat.id,standort=standort)
        self.session.add(kz)
        self.session.commit()
        return kz

    def speichere_kennzahlen(self,standort,zusatzfahrer,zusatztrailer,fahrerkosten,trailerkosten):
        kz=self.hole_oder_erzeuge_kennzahlen(standort)
        kz.zusatzfahrer=zusatzfahrer
        kz.zusatztrailer=zusatztrailer
        kz.durchschnitt_fahrer_kosten=fahrerkosten
        kz.durchschnitt_trailer_kosten=trailerkosten
        self.session.commit()

    def synchronisiere_fahrzeuge(self):
        monat=self.hole_oder_erzeuge_monat()
        aktive=self.session.query(Fahrzeug).filter_by(aktiv=True).all()
        vorhanden={m.fahrzeug_id for m in self.session.query(Monatsdaten).filter_by(monat_id=monat.id).all()}
        geaendert=False
        for fahrzeug in aktive:
            if fahrzeug.id not in vorhanden:
                self.session.add(Monatsdaten(fahrzeug_id=fahrzeug.id,monat_id=monat.id))
                geaendert=True
        if geaendert:
            self.session.commit()

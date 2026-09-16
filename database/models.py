from datetime import date

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Date,
    ForeignKey,
)

from sqlalchemy.orm import relationship

from .database import Base


# ------------------------------------------------------------
# Fahrzeuge
# ------------------------------------------------------------

class Fahrzeug(Base):
    __tablename__ = "fahrzeuge"

    id = Column(Integer, primary_key=True)

    kennzeichen = Column(String, unique=True, nullable=False)
    fahrzeugtyp = Column(String)
    standort = Column(String)

    fahreranzahl = Column(Integer, default=1)

    trailer_kategorie = Column(String)

    trailer_id = Column(Integer, ForeignKey("trailer.id"))

    aktiv = Column(Boolean, default=True)


# ------------------------------------------------------------
# Trailer
# ------------------------------------------------------------

class Trailer(Base):
    __tablename__ = "trailer"

    id = Column(Integer, primary_key=True)

    kennzeichen = Column(String, unique=True)
    kategorie = Column(String)

    monatsmiete = Column(Float, default=0)

    vertragsbeginn = Column(Date)
    vertragsende = Column(Date)
    rueckgabe = Column(Date)

    aktiv = Column(Boolean, default=True)

    fahrzeuge = relationship("Fahrzeug", backref="trailer")


# ------------------------------------------------------------
# Monatsdaten je Fahrzeug
# ------------------------------------------------------------

class Monatsdaten(Base):
    __tablename__ = "monatsdaten"

    id = Column(Integer, primary_key=True)

    fahrzeug_id = Column(Integer, ForeignKey("fahrzeuge.id"))

    jahr = Column(Integer)
    monat = Column(Integer)

    # Fixkosten
    finanzierung = Column(Float, default=0)
    versicherung = Column(Float, default=0)
    steuer = Column(Float, default=0)
    wartung = Column(Float, default=0)

    # Variable Kosten
    diesel = Column(Float, default=0)
    maut = Column(Float, default=0)
    werkstatt = Column(Float, default=0)
    sonstiges = Column(Float, default=0)

    # Leistungsdaten
    umsatz = Column(Float, default=0)
    kilometer = Column(Float, default=0)


# ------------------------------------------------------------
# Monatskennzahlen
# ------------------------------------------------------------

class Monatskennzahl(Base):
    __tablename__ = "monatskennzahlen"

    id = Column(Integer, primary_key=True)

    jahr = Column(Integer)
    monat = Column(Integer)

    standort = Column(String)

    zusatzfahrer = Column(Integer, default=0)
    zusatztrailer = Column(Integer, default=0)


# ------------------------------------------------------------
# Einmalkosten
# ------------------------------------------------------------

class Einmalkosten(Base):
    __tablename__ = "einmalkosten"

    id = Column(Integer, primary_key=True)

    datum = Column(Date)

    standort = Column(String)

    kategorie = Column(String)
    beschreibung = Column(String)

    betrag = Column(Float, default=0)


# ------------------------------------------------------------
# Monatsverwaltung
# ------------------------------------------------------------

class Monat(Base):
    __tablename__ = "monate"

    id = Column(Integer, primary_key=True)

    jahr = Column(Integer, nullable=False)
    monat = Column(Integer, nullable=False)

    status = Column(String, default="In Bearbeitung")

    erstellt_am = Column(Date, default=date.today)

    abgeschlossen_am = Column(Date, nullable=True)

    abgeschlossen_von = Column(String, nullable=True)
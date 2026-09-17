"""
Release: v0.6.4
Datei: database/models.py
Komplette Datei
"""

from datetime import date

from sqlalchemy import (
    Boolean,
    Column,
    Date,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


# ==========================================================
# Fahrzeuge
# ==========================================================

class Fahrzeug(Base):
    __tablename__ = "fahrzeuge"

    id = Column(Integer, primary_key=True)

    sortierung = Column(Integer, default=100)

    kennzeichen = Column(String, unique=True, nullable=False)

    fahrzeugtyp = Column(String, default="Sattelzugmaschine")

    standort = Column(String, nullable=False)

    fahreranzahl = Column(Integer, default=1)

    trailer_kategorie = Column(String, default="Standard")

    trailer_id = Column(Integer, ForeignKey("trailer.id"), nullable=True)

    aktiv = Column(Boolean, default=True)

    trailer = relationship("Trailer", back_populates="fahrzeuge")

    monatsdaten = relationship(
        "Monatsdaten",
        back_populates="fahrzeug",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Trailer
# ==========================================================

class Trailer(Base):
    __tablename__ = "trailer"

    id = Column(Integer, primary_key=True)

    bezeichnung = Column(String, nullable=False)

    standort = Column(String, nullable=False)

    kategorie = Column(String, default="Standard")

    vertragsbeginn = Column(Date)

    vertragsende = Column(Date)

    rueckgabedatum = Column(Date)

    aktiv = Column(Boolean, default=True)

    fahrzeuge = relationship("Fahrzeug", back_populates="trailer")


# ==========================================================
# Monat
# ==========================================================

class Monat(Base):
    __tablename__ = "monate"

    id = Column(Integer, primary_key=True)

    jahr = Column(Integer, nullable=False)

    monat = Column(Integer, nullable=False)

    status = Column(String, default="In Bearbeitung")

    erstellt_am = Column(Date, default=date.today)

    abgeschlossen_am = Column(Date)

    abgeschlossen_von = Column(String)

    monatsdaten = relationship(
        "Monatsdaten",
        back_populates="monat",
        cascade="all, delete-orphan",
    )

    kennzahlen = relationship(
        "MonatsKennzahlen",
        back_populates="monat",
        cascade="all, delete-orphan",
    )


# ==========================================================
# Monatsdaten (je Fahrzeug)
# ==========================================================

class Monatsdaten(Base):
    __tablename__ = "monatsdaten"

    id = Column(Integer, primary_key=True)

    fahrzeug_id = Column(Integer, ForeignKey("fahrzeuge.id"))

    monat_id = Column(Integer, ForeignKey("monate.id"))

    diesel = Column(Float, default=0)

    maut = Column(Float, default=0)

    werkstatt = Column(Float, default=0)

    sonstiges = Column(Float, default=0)

    umsatz = Column(Float, default=0)

    kilometer = Column(Float, default=0)

    fahrzeug = relationship("Fahrzeug", back_populates="monatsdaten")

    monat = relationship("Monat", back_populates="monatsdaten")


# ==========================================================
# Monatskennzahlen
# ==========================================================

class MonatsKennzahlen(Base):
    __tablename__ = "monatskennzahlen"

    id = Column(Integer, primary_key=True)

    monat_id = Column(Integer, ForeignKey("monate.id"))

    standort = Column(String, default="Gesamt")

    # Zahlen, Daten, Fakten

    zusatzfahrer = Column(Integer, default=0)

    zusatztrailer = Column(Integer, default=0)

    durchschnitt_fahrer_kosten = Column(Float, default=0)

    durchschnitt_trailer_kosten = Column(Float, default=0)

    monat = relationship("Monat", back_populates="kennzahlen")


# ==========================================================
# Einmalkosten
# ==========================================================

class Einmalkosten(Base):
    __tablename__ = "einmalkosten"

    id = Column(Integer, primary_key=True)

    monat_id = Column(Integer, ForeignKey("monate.id"))

    standort = Column(String, default="Gesamt")

    bezeichnung = Column(String)

    betrag = Column(Float, default=0)
"""
Release: v0.6.2
Datei: database/migrations.py
Komplette Datei
"""

from sqlalchemy import text

from .database import engine


def spalten(tabellenname):
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({tabellenname})"))
        return {row[1] for row in result}


def add_column(tabellenname, definition):
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {tabellenname} ADD COLUMN {definition}"))


def run_migrations():

    # -----------------------------------------------------
    # MONATSDATEN
    # -----------------------------------------------------

    cols = spalten("monatsdaten")

    if "monat_id" not in cols:
        add_column("monatsdaten", "monat_id INTEGER")

    if "kilometer" not in cols:
        add_column("monatsdaten", "kilometer REAL DEFAULT 0")

    # -----------------------------------------------------
    # FAHRZEUGE
    # -----------------------------------------------------

    cols = spalten("fahrzeuge")

    if "sortierung" not in cols:
        add_column("fahrzeuge", "sortierung INTEGER DEFAULT 100")

    if "fahrzeugtyp" not in cols:
        add_column("fahrzeuge", "fahrzeugtyp TEXT DEFAULT 'Sattelzugmaschine'")

    if "fahreranzahl" not in cols:
        add_column("fahrzeuge", "fahreranzahl INTEGER DEFAULT 1")

    if "trailer_kategorie" not in cols:
        add_column("fahrzeuge", "trailer_kategorie TEXT DEFAULT 'Standard'")
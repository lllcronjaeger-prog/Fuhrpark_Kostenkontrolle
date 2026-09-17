"""
Release: v0.6.2
Datei: database/migrations.py
Komplette Datei
"""

from sqlalchemy import inspect, text

from .database import engine


def _spalten(tabellenname):
    inspector = inspect(engine)

    if tabellenname not in inspector.get_table_names():
        return set()

    return {c["name"] for c in inspector.get_columns(tabellenname)}


def _add_column(tabellenname, definition):
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {tabellenname} ADD COLUMN {definition}"))


def run_migrations():
    inspector = inspect(engine)

    tabellen = inspector.get_table_names()

    # ---------------------------------------------------------
    # Fahrzeuge
    # ---------------------------------------------------------

    if "fahrzeuge" in tabellen:

        cols = _spalten("fahrzeuge")

        if "sortierung" not in cols:
            _add_column("fahrzeuge", "sortierung INTEGER DEFAULT 100")

        if "fahrzeugtyp" not in cols:
            _add_column("fahrzeuge", "fahrzeugtyp TEXT DEFAULT 'Sattelzugmaschine'")

        if "fahreranzahl" not in cols:
            _add_column("fahrzeuge", "fahreranzahl INTEGER DEFAULT 1")

        if "trailer_kategorie" not in cols:
            _add_column("fahrzeuge", "trailer_kategorie TEXT DEFAULT 'Standard'")

    # ---------------------------------------------------------
    # Trailer
    # ---------------------------------------------------------

    if "trailer" in tabellen:

        cols = _spalten("trailer")

        if "vertragsbeginn" not in cols:
            _add_column("trailer", "vertragsbeginn DATE")

        if "vertragsende" not in cols:
            _add_column("trailer", "vertragsende DATE")

        if "rueckgabedatum" not in cols:
            _add_column("trailer", "rueckgabedatum DATE")

        if "aktiv" not in cols:
            _add_column("trailer", "aktiv BOOLEAN DEFAULT 1")

    # ---------------------------------------------------------
    # Monate
    # ---------------------------------------------------------

    if "monate" in tabellen:

        cols = _spalten("monate")

        if "status" not in cols:
            _add_column("monate", "status TEXT DEFAULT 'In Bearbeitung'")

        if "erstellt_am" not in cols:
            _add_column("monate", "erstellt_am DATE")

        if "abgeschlossen_am" not in cols:
            _add_column("monate", "abgeschlossen_am DATE")

        if "abgeschlossen_von" not in cols:
            _add_column("monate", "abgeschlossen_von TEXT")

    # ---------------------------------------------------------
    # Monatsdaten
    # ---------------------------------------------------------

    if "monatsdaten" in tabellen:

        cols = _spalten("monatsdaten")

        if "monat_id" not in cols:
            _add_column("monatsdaten", "monat_id INTEGER")

        if "kilometer" not in cols:
            _add_column("monatsdaten", "kilometer REAL DEFAULT 0")

    # ---------------------------------------------------------
    # Monatskennzahlen
    # ---------------------------------------------------------

    if "monatskennzahlen" in tabellen:

        cols = _spalten("monatskennzahlen")

        if "monat_id" not in cols:
            _add_column("monatskennzahlen", "monat_id INTEGER")

        if "standort" not in cols:
            _add_column("monatskennzahlen", "standort TEXT DEFAULT 'Gesamt'")

        if "zusatzfahrer" not in cols:
            _add_column("monatskennzahlen", "zusatzfahrer INTEGER DEFAULT 0")

        if "zusatztrailer" not in cols:
            _add_column("monatskennzahlen", "zusatztrailer INTEGER DEFAULT 0")

        if "durchschnitt_fahrer_kosten" not in cols:
            _add_column("monatskennzahlen", "durchschnitt_fahrer_kosten REAL DEFAULT 0")

        if "durchschnitt_trailer_kosten" not in cols:
            _add_column("monatskennzahlen", "durchschnitt_trailer_kosten REAL DEFAULT 0")

    # ---------------------------------------------------------
    # Einmalkosten
    # ---------------------------------------------------------

    if "einmalkosten" in tabellen:

        cols = _spalten("einmalkosten")

        if "monat_id" not in cols:
            _add_column("einmalkosten", "monat_id INTEGER")

        if "standort" not in cols:
            _add_column("einmalkosten", "standort TEXT DEFAULT 'Gesamt'")
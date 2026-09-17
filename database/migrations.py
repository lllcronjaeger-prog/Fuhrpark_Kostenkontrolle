"""
Release: v0.6.4
Datei: database/migrations.py
Komplette Datei
"""

from sqlalchemy import text
from .database import engine


def _table_exists(name: str) -> bool:
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name=:name"),
            {"name": name},
        )
        return result.first() is not None


def _columns(table: str) -> set[str]:
    with engine.connect() as conn:
        result = conn.execute(text(f"PRAGMA table_info({table})"))
        return {row[1] for row in result}


def _add_column(table: str, definition: str):
    with engine.begin() as conn:
        conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {definition}"))


def run_migrations():
    """
    Führt alle fehlenden Migrationen aus.
    Bestehende Daten bleiben erhalten.
    """

    # =====================================================
    # Fahrzeuge
    # =====================================================

    if _table_exists("fahrzeuge"):

        cols = _columns("fahrzeuge")

        if "sortierung" not in cols:
            _add_column("fahrzeuge", "sortierung INTEGER DEFAULT 100")

        if "fahrzeugtyp" not in cols:
            _add_column(
                "fahrzeuge",
                "fahrzeugtyp TEXT DEFAULT 'Sattelzugmaschine'",
            )

        if "fahreranzahl" not in cols:
            _add_column("fahrzeuge", "fahreranzahl INTEGER DEFAULT 1")

        if "trailer_kategorie" not in cols:
            _add_column(
                "fahrzeuge",
                "trailer_kategorie TEXT DEFAULT 'Standard'",
            )

        if "aktiv" not in cols:
            _add_column("fahrzeuge", "aktiv BOOLEAN DEFAULT 1")

    # =====================================================
    # Trailer
    # =====================================================

    if _table_exists("trailer"):

        cols = _columns("trailer")

        if "vertragsbeginn" not in cols:
            _add_column("trailer", "vertragsbeginn DATE")

        if "vertragsende" not in cols:
            _add_column("trailer", "vertragsende DATE")

        if "rueckgabedatum" not in cols:
            _add_column("trailer", "rueckgabedatum DATE")

        if "aktiv" not in cols:
            _add_column("trailer", "aktiv BOOLEAN DEFAULT 1")

    # =====================================================
    # Monate
    # =====================================================

    if _table_exists("monate"):

        cols = _columns("monate")

        if "status" not in cols:
            _add_column(
                "monate",
                "status TEXT DEFAULT 'In Bearbeitung'",
            )

        if "erstellt_am" not in cols:
            _add_column("monate", "erstellt_am DATE")

        if "abgeschlossen_am" not in cols:
            _add_column("monate", "abgeschlossen_am DATE")

        if "abgeschlossen_von" not in cols:
            _add_column("monate", "abgeschlossen_von TEXT")

    # =====================================================
    # Monatsdaten
    # =====================================================

    if _table_exists("monatsdaten"):

        cols = _columns("monatsdaten")

        if "monat_id" not in cols:
            _add_column("monatsdaten", "monat_id INTEGER")

        if "kilometer" not in cols:
            _add_column("monatsdaten", "kilometer REAL DEFAULT 0")

    # =====================================================
    # Monatskennzahlen
    # =====================================================

    if not _table_exists("monatskennzahlen"):

        with engine.begin() as conn:
            conn.execute(
                text(
                    """
                    CREATE TABLE monatskennzahlen (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        monat_id INTEGER,
                        standort TEXT DEFAULT 'Gesamt',
                        zusatzfahrer INTEGER DEFAULT 0,
                        zusatztrailer INTEGER DEFAULT 0,
                        durchschnitt_fahrer_kosten REAL DEFAULT 0,
                        durchschnitt_trailer_kosten REAL DEFAULT 0
                    )
                    """
                )
            )

    else:

        cols = _columns("monatskennzahlen")

        if "monat_id" not in cols:
            _add_column("monatskennzahlen", "monat_id INTEGER")

        if "standort" not in cols:
            _add_column(
                "monatskennzahlen",
                "standort TEXT DEFAULT 'Gesamt'",
            )

        if "zusatzfahrer" not in cols:
            _add_column(
                "monatskennzahlen",
                "zusatzfahrer INTEGER DEFAULT 0",
            )

        if "zusatztrailer" not in cols:
            _add_column(
                "monatskennzahlen",
                "zusatztrailer INTEGER DEFAULT 0",
            )

        if "durchschnitt_fahrer_kosten" not in cols:
            _add_column(
                "monatskennzahlen",
                "durchschnitt_fahrer_kosten REAL DEFAULT 0",
            )

        if "durchschnitt_trailer_kosten" not in cols:
            _add_column(
                "monatskennzahlen",
                "durchschnitt_trailer_kosten REAL DEFAULT 0",
            )

    # =====================================================
    # Einmalkosten
    # =====================================================

    if _table_exists("einmalkosten"):

        cols = _columns("einmalkosten")

        if "monat_id" not in cols:
            _add_column("einmalkosten", "monat_id INTEGER")

        if "standort" not in cols:
            _add_column(
                "einmalkosten",
                "standort TEXT DEFAULT 'Gesamt'",
            )
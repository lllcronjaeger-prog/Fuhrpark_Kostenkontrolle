
import sqlite3
from pathlib import Path

# Datenbank finden
db = Path("data/fuhrpark.db")

if not db.exists():
    kandidaten = list(Path(".").rglob("*.db"))
    if not kandidaten:
        raise FileNotFoundError("Keine SQLite-Datenbank gefunden.")
    db = kandidaten[0]

print(f"Verwende Datenbank: {db}")

conn = sqlite3.connect(db)
cur = conn.cursor()


def add_column(table, column, definition):
    cur.execute(f"PRAGMA table_info({table})")
    vorhandene = {r[1] for r in cur.fetchall()}

    if column not in vorhandene:
        print(f"+ {table}.{column}")
        cur.execute(
            f"ALTER TABLE {table} ADD COLUMN {column} {definition}"
        )


# ================= Fahrzeuge =================

add_column("fahrzeuge", "inventar_id", "TEXT")
add_column("fahrzeuge", "monatsmiete", "REAL DEFAULT 0")
add_column("fahrzeuge", "steuer", "REAL DEFAULT 0")
add_column("fahrzeuge", "versicherung", "REAL DEFAULT 0")
add_column("fahrzeuge", "werkstatt_pauschale", "REAL DEFAULT 0")
add_column("fahrzeuge", "vertragsbeginn", "DATE")
add_column("fahrzeuge", "vertragsende", "DATE")
add_column("fahrzeuge", "rueckgabedatum", "DATE")
add_column("fahrzeuge", "kuendigungsfrist_monate", "INTEGER DEFAULT 0")

# ================= Trailer =================

add_column("trailer", "inventar_id", "TEXT")
add_column("trailer", "monatsmiete", "REAL DEFAULT 0")
add_column("trailer", "steuer", "REAL DEFAULT 0")
add_column("trailer", "versicherung", "REAL DEFAULT 0")
add_column("trailer", "vertragsbeginn", "DATE")
add_column("trailer", "vertragsende", "DATE")
add_column("trailer", "rueckgabedatum", "DATE")
add_column("trailer", "kuendigungsfrist_monate", "INTEGER DEFAULT 0")

conn.commit()
conn.close()

print("\nDatenbank erfolgreich aktualisiert.")
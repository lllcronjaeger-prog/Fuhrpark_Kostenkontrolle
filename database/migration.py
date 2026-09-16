from sqlalchemy import inspect, text

from .database import engine


def run_migrations():
    """
    Führt einfache Datenbankmigrationen automatisch aus.
    """

    inspector = inspect(engine)

    if "fahrzeuge" in inspector.get_table_names():

        spalten = [c["name"] for c in inspector.get_columns("fahrzeuge")]

        with engine.begin() as conn:

            neue_spalten = {
                "fahrzeugtyp": "TEXT",
                "fahreranzahl": "INTEGER DEFAULT 1",
                "trailer_kategorie": "TEXT",
                "sortierung": "INTEGER DEFAULT 100",
                "aktiv": "BOOLEAN DEFAULT 1",
            }

            for name, typ in neue_spalten.items():
                if name not in spalten:
                    conn.execute(
                        text(
                            f"ALTER TABLE fahrzeuge ADD COLUMN {name} {typ}"
                        )
                    )
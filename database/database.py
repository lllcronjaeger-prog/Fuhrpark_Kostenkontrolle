from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

from config import DATABASE_PATH

engine = create_engine(f"sqlite:///{DATABASE_PATH}", echo=False)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


def migrate_database():
    """
    Führt einfache Schema-Erweiterungen automatisch durch.
    """
    inspector = inspect(engine)

    if "fahrzeuge" in inspector.get_table_names():

        spalten = [c["name"] for c in inspector.get_columns("fahrzeuge")]

        with engine.begin() as conn:

            if "fahrzeugtyp" not in spalten:
                conn.execute(
                    text("ALTER TABLE fahrzeuge ADD COLUMN fahrzeugtyp TEXT")
                )

            if "aktiv" not in spalten:
                conn.execute(
                    text(
                        "ALTER TABLE fahrzeuge ADD COLUMN aktiv BOOLEAN DEFAULT 1"
                    )
                )

            if "fahreranzahl" not in spalten:
                conn.execute(
                    text(
                        "ALTER TABLE fahrzeuge ADD COLUMN fahreranzahl INTEGER DEFAULT 1"
                    )
                )

            if "trailer_kategorie" not in spalten:
                conn.execute(
                    text(
                        "ALTER TABLE fahrzeuge ADD COLUMN trailer_kategorie TEXT"
                    )
                )
            if "monate" not in inspector.get_table_names():
                Base.metadata.create_all(engine)   
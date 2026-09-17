"""
Release: v0.6.2
Datei: database/database.py
Komplette Datei
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DATABASE_PATH

engine = create_engine(
    f"sqlite:///{DATABASE_PATH}",
    echo=False,
)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
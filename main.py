"""
Release: v0.6.2
Datei: main.py
Komplette Datei
"""

from PySide6.QtWidgets import QApplication

from database.database import Base, engine
from database.migrations import run_migrations
from ui.main_window import MainWindow


def main():

    app = QApplication([])

    Base.metadata.create_all(bind=engine)

    run_migrations()

    window = MainWindow()
    window.show()

    app.exec()


if __name__ == "__main__":
    main()
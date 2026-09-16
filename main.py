import sys

from PySide6.QtWidgets import QApplication

from database.database import Base, engine
from database.migrations import run_migrations

# Modelle importieren
import database.models  # noqa: F401

from ui.main_window import MainWindow


def main():

    Base.metadata.create_all(engine)

    run_migrations()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
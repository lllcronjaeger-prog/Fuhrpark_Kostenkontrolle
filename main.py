import sys

from PySide6.QtWidgets import QApplication

from database.database import engine, migrate_database
from database.models import Base

from ui.main_window import MainWindow


def main():
    # Tabellen anlegen
    Base.metadata.create_all(engine)

    # Migrationen ausführen
    migrate_database()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QComboBox,
)

from config import APP_NAME, COLORS
from .app_state import app_state
from .monatserfassung import MonatsErfassung


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1450, 900)

        self.setStyleSheet(f"""
            QMainWindow {{
                background:#1f1f1f;
            }}

            QLabel {{
                color:white;
            }}

            QComboBox {{
                background:#2b2b2b;
                color:white;
                border:1px solid #444;
                border-radius:6px;
                padding:5px;
            }}
        """)

        root = QWidget()
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(10, 10, 10, 10)

        # Kopfzeile
        kopf = QHBoxLayout()

        titel = QLabel("Fuhrpark-Kostenkontrolle")
        titel.setStyleSheet(f"""
            font-size:24px;
            font-weight:bold;
            color:{COLORS["orange"]};
        """)

        kopf.addWidget(titel)
        kopf.addStretch()

        self.monat = QComboBox()
        self.monat.addItems([
            "Januar","Februar","März","April","Mai","Juni",
            "Juli","August","September","Oktober","November","Dezember"
        ])
        self.monat.setCurrentIndex(app_state.monat - 1)

        self.standort = QComboBox()
        self.standort.addItems(["Gesamt", "Leipzig", "Ettlingen"])

        kopf.addWidget(self.monat)
        kopf.addWidget(self.standort)

        layout.addLayout(kopf)

        # Neue Monatserfassung als Hauptbereich
        self.erfassung = MonatsErfassung()
        layout.addWidget(self.erfassung)

        self.statusBar().showMessage(
            f"September {app_state.jahr} | Gesamt | In Bearbeitung"
        )
from calendar import month_name

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QFrame,
    QStackedWidget,
)

from config import APP_NAME, COLORS
from .dashboard import Dashboard
from .fahrzeuge import FahrzeugeSeite
from .monate import MonateSeite
from .app_state import app_state


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1450, 900)

        self.setStyleSheet(f"""
            QMainWindow {{
                background:{COLORS["hell"]};
            }}

            QListWidget {{
                background:{COLORS["blau"]};
                color:white;
                border:none;
                font-size:15px;
            }}

            QListWidget::item {{
                padding:12px;
                margin:4px 8px;
                border-radius:8px;
            }}

            QListWidget::item:selected {{
                background:{COLORS["orange"]};
            }}

            QListWidget::item:hover {{
                background:#2b4f7a;
            }}

            QComboBox {{
                padding:6px;
                border-radius:8px;
                border:1px solid #bbbbbb;
                background:white;
                min-width:120px;
            }}

            QLabel#HeaderLabel {{
                color:white;
                font-size:14px;
                font-weight:bold;
            }}
        """)

        container = QWidget()
        self.setCentralWidget(container)

        hauptlayout = QVBoxLayout(container)
        hauptlayout.setContentsMargins(0, 0, 0, 0)
        hauptlayout.setSpacing(0)

        # Kopfzeile
        self.kopf = self.erzeuge_kopfzeile()
        hauptlayout.addWidget(self.kopf)

        # Hauptbereich
        mitte = QHBoxLayout()
        mitte.setContentsMargins(10, 10, 10, 10)

        # Navigation
        self.menu = QListWidget()

        menues = [
            "🏠 Dashboard",
            "🚛 Fahrzeuge",
            "📆 Monate",
            "🔗 Trailer",
            "📅 Monatserfassung",
            "💰 Einmalkosten",
            "📊 Management",
            "⚙ Einstellungen",
        ]

        for eintrag in menues:
            self.menu.addItem(QListWidgetItem(eintrag))

        self.menu.setMaximumWidth(230)

        # Seiten
        self.stack = QStackedWidget()

        self.stack.addWidget(Dashboard())          # Index 0
        self.stack.addWidget(FahrzeugeSeite())     # Index 1
        self.stack.addWidget(MonateSeite())        # Index 2

        # Platzhalter für kommende Seiten
        for _ in range(5):
            self.stack.addWidget(QWidget())

        self.menu.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.menu.setCurrentRow(0)

        mitte.addWidget(self.menu)
        mitte.addWidget(self.stack)

        hauptlayout.addLayout(mitte)

        self.aktualisiere_status()

    # -------------------------------------------------------------

    def erzeuge_kopfzeile(self):

        frame = QFrame()

        frame.setStyleSheet(f"""
            QFrame {{
                background:{COLORS["blau"]};
            }}
        """)

        layout = QHBoxLayout(frame)
        layout.setContentsMargins(15, 10, 15, 10)

        logo = QLabel("Fuhrpark-Kostenkontrolle")

        logo.setStyleSheet("""
            color:white;
            font-size:18px;
            font-weight:bold;
        """)

        layout.addWidget(logo)
        layout.addStretch()

        # Monat
        lbl_monat = QLabel("Monat:")
        lbl_monat.setObjectName("HeaderLabel")
        layout.addWidget(lbl_monat)

        self.monat_box = QComboBox()

        self.monat_box.addItems([
            "Januar",
            "Februar",
            "März",
            "April",
            "Mai",
            "Juni",
            "Juli",
            "August",
            "September",
            "Oktober",
            "November",
            "Dezember",
        ])

        self.monat_box.setCurrentIndex(app_state.monat - 1)
        self.monat_box.currentIndexChanged.connect(self.monat_geaendert)

        layout.addWidget(self.monat_box)

        # Jahr
        self.jahr_label = QLabel(str(app_state.jahr))
        self.jahr_label.setObjectName("HeaderLabel")

        layout.addWidget(self.jahr_label)

        layout.addSpacing(20)

        # Standort
        lbl_standort = QLabel("Standort:")
        lbl_standort.setObjectName("HeaderLabel")
        layout.addWidget(lbl_standort)

        self.standort_box = QComboBox()

        self.standort_box.addItems([
            "Gesamt",
            "Leipzig",
            "Ettlingen",
        ])

        self.standort_box.setCurrentText(app_state.standort)
        self.standort_box.currentTextChanged.connect(
            self.standort_geaendert
        )

        layout.addWidget(self.standort_box)

        # Status
        layout.addSpacing(20)

        self.status_label = QLabel(app_state.monatsstatus)
        self.status_label.setStyleSheet("""
            color:white;
            background:#F28C00;
            padding:6px 12px;
            border-radius:12px;
            font-weight:bold;
        """)

        layout.addWidget(self.status_label)

        return frame

    # -------------------------------------------------------------

    def aktualisiere_status(self):

        self.statusBar().showMessage(
            f"{month_name[app_state.monat]} "
            f"{app_state.jahr} | "
            f"{app_state.standort} | "
            f"{app_state.monatsstatus}"
        )

        self.status_label.setText(app_state.monatsstatus)

    # -------------------------------------------------------------

    def monat_geaendert(self, index):

        app_state.monat = index + 1
        self.aktualisiere_status()

    # -------------------------------------------------------------

    def standort_geaendert(self, text):

        app_state.standort = text
        self.aktualisiere_status()
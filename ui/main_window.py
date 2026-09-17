"""
Release: v0.6.0
Datei: ui/main_window.py
Komplette Datei
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QListWidget,
    QListWidgetItem,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QStackedWidget,
    QFrame,
)

from config import APP_NAME, COLORS
from ui.app_state import app_state
from ui.dashboard import Dashboard
from ui.monatserfassung import MonatsErfassung
from ui.fahrzeuge import FahrzeugeSeite


class PlatzhalterSeite(QWidget):
    """Einheitlicher Platzhalter für noch nicht umgesetzte Bereiche."""

    def __init__(self, titel):
        super().__init__()

        self.setStyleSheet(f"""
            QWidget {{
                background:{COLORS["hell"]};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(30, 30, 30, 30)

        ueberschrift = QLabel(titel)
        ueberschrift.setStyleSheet(f"""
            font-size:30px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)

        layout.addWidget(ueberschrift)

        box = QFrame()
        box.setStyleSheet("""
            background:white;
            border:1px solid #D8D8D8;
            border-radius:18px;
        """)

        box_layout = QVBoxLayout(box)

        text = QLabel("Diese Seite wird im nächsten Release umgesetzt.")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("font-size:18px;color:#777777;")

        box_layout.addWidget(text)

        layout.addWidget(box)


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(APP_NAME)
        self.resize(1500, 930)

        root = QWidget()
        self.setCentralWidget(root)

        hauptlayout = QVBoxLayout(root)
        hauptlayout.setContentsMargins(0, 0, 0, 0)
        hauptlayout.setSpacing(0)

        # =====================================================
        # Kopfleiste
        # =====================================================

        header = QWidget()

        header.setStyleSheet(f"""
            background:{COLORS["blau"]};
            color:white;
        """)

        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(18, 12, 18, 12)

        titel = QLabel("Fuhrpark-Kostenkontrolle")

        titel.setStyleSheet("""
            color:white;
            font-size:24px;
            font-weight:bold;
        """)

        header_layout.addWidget(titel)
        header_layout.addStretch()

        monat_label = QLabel("Monat:")
        monat_label.setStyleSheet("color:white;")

        self.monat = QComboBox()
        self.monat.addItems([
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

        self.monat.setCurrentIndex(app_state.monat - 1)

        standort_label = QLabel("Standort:")
        standort_label.setStyleSheet("color:white;")

        self.standort = QComboBox()
        self.standort.addItems([
            "Gesamt",
            "Leipzig",
            "Ettlingen",
        ])

        self.standort.setCurrentText(app_state.standort)

        header_layout.addWidget(monat_label)
        header_layout.addWidget(self.monat)

        header_layout.addSpacing(10)

        header_layout.addWidget(standort_label)
        header_layout.addWidget(self.standort)

        hauptlayout.addWidget(header)

        # =====================================================
        # Hauptbereich
        # =====================================================

        mitte = QHBoxLayout()
        mitte.setContentsMargins(10, 10, 10, 10)
        mitte.setSpacing(10)

        # ---------------- Navigation ----------------

        self.menu = QListWidget()
        self.menu.setMaximumWidth(220)

        self.menu.setStyleSheet(f"""
            QListWidget {{
                background:{COLORS["blau"]};
                color:white;
                border:none;
                border-radius:14px;
                font-size:15px;
            }}

            QListWidget::item {{
                padding:14px;
                margin:4px;
                border-radius:8px;
            }}

            QListWidget::item:selected {{
                background:{COLORS["orange"]};
                color:black;
                font-weight:bold;
            }}
        """)

        menupunkte = [
            "🏠 Dashboard",
            "🚛 Fahrzeuge",
            "🔗 Trailer",
            "📅 Monatserfassung",
            "💰 Einmalkosten",
            "📊 Management",
            "⚙ Einstellungen",
        ]

        for punkt in menupunkte:
            self.menu.addItem(QListWidgetItem(punkt))

        mitte.addWidget(self.menu)

        # ---------------- Seiten ----------------

        self.stack = QStackedWidget()

        self.dashboard = Dashboard()
        self.fahrzeuge = FahrzeugeSeite()
        self.trailer = PlatzhalterSeite("Trailer")
        self.monatserfassung = MonatsErfassung()
        self.einmalkosten = PlatzhalterSeite("Einmalkosten")
        self.management = PlatzhalterSeite("Management")
        self.einstellungen = PlatzhalterSeite("Einstellungen")

        # Live-KPI Dashboard
        self.monatserfassung.kpisChanged.connect(
            self.dashboard.update_kpis
        )

        self.stack.addWidget(self.dashboard)          # 0
        self.stack.addWidget(self.fahrzeuge)          # 1
        self.stack.addWidget(self.trailer)            # 2
        self.stack.addWidget(self.monatserfassung)    # 3
        self.stack.addWidget(self.einmalkosten)       # 4
        self.stack.addWidget(self.management)         # 5
        self.stack.addWidget(self.einstellungen)      # 6

        self.menu.currentRowChanged.connect(
            self.stack.setCurrentIndex
        )

        self.menu.setCurrentRow(0)

        mitte.addWidget(self.stack)

        hauptlayout.addLayout(mitte)

        self.statusBar().showMessage(
            f"September {app_state.jahr} | "
            f"{app_state.standort} | "
            "In Bearbeitung"
        )
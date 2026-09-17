"""
Release: v0.6.0
Datei: ui/fahrzeuge.py
Komplette Datei
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QTableWidget,
    QTableWidgetItem,
    QMessageBox,
    QHeaderView,
)

from config import COLORS
from database.database import SessionLocal
from database.models import Fahrzeug
from ui.dialogs.fahrzeug_dialog import FahrzeugDialog


class FahrzeugeSeite(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            QWidget {{
                background:{COLORS["hell"]};
            }}

            QTableWidget {{
                background:white;
                color:#202020;
                alternate-background-color:#F7F7F7;
                gridline-color:#D8D8D8;
                border:1px solid #D8D8D8;
                font-size:13px;
            }}

            QHeaderView::section {{
                background:#ECECEC;
                color:#17365D;
                font-weight:bold;
                padding:8px;
                border:none;
            }}

            QPushButton {{
                border:none;
                border-radius:8px;
                padding:8px 14px;
                font-weight:bold;
            }}

            QLineEdit {{
                background:white;
                color:#202020;
                border:1px solid #C8C8C8;
                border-radius:8px;
                padding:6px;
            }}
        """)

        self.session = SessionLocal()

        self._aufbauen()
        self.laden()

    # -------------------------------------------------

    def _aufbauen(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        titel = QLabel("Fahrzeuge")

        titel.setStyleSheet(f"""
            font-size:30px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)

        layout.addWidget(titel)

        # Werkzeugleiste

        toolbar = QHBoxLayout()

        self.suche = QLineEdit()
        self.suche.setPlaceholderText("Kennzeichen suchen...")

        self.suche.textChanged.connect(self.laden)

        toolbar.addWidget(self.suche)

        self.btn_neu = QPushButton("➕ Neu")
        self.btn_neu.clicked.connect(self.neu)

        self.btn_neu.setStyleSheet(f"""
            QPushButton{{
                background:{COLORS["orange"]};
                color:black;
            }}
            QPushButton:hover{{
                background:#E07D00;
            }}
        """)

        toolbar.addWidget(self.btn_neu)

        self.btn_bearbeiten = QPushButton("✏ Bearbeiten")
        self.btn_bearbeiten.clicked.connect(self.bearbeiten)

        self.btn_bearbeiten.setStyleSheet("""
            QPushButton{
                background:#4A90E2;
                color:white;
            }
            QPushButton:hover{
                background:#3979C9;
            }
        """)

        toolbar.addWidget(self.btn_bearbeiten)

        self.btn_deaktivieren = QPushButton("❌ Deaktivieren")
        self.btn_deaktivieren.clicked.connect(self.deaktivieren)

        self.btn_deaktivieren.setStyleSheet("""
            QPushButton{
                background:#C0392B;
                color:white;
            }
            QPushButton:hover{
                background:#A93226;
            }
        """)

        toolbar.addWidget(self.btn_deaktivieren)

        layout.addLayout(toolbar)

        # Tabelle

        self.table = QTableWidget(0,7)

        self.table.setHorizontalHeaderLabels([
            "Sort.",
            "Kennzeichen",
            "Typ",
            "Standort",
            "Fahrer",
            "Trailer",
            "Status",
        ])

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)

        layout.addWidget(self.table)

    # -------------------------------------------------

    def laden(self):

        self.table.setRowCount(0)

        suchtext = self.suche.text().strip().upper()

        query = self.session.query(Fahrzeug)

        if suchtext:
            query = query.filter(Fahrzeug.kennzeichen.like(f"%{suchtext}%"))

        daten = query.order_by(Fahrzeug.sortierung).all()

        for fahrzeug in daten:

            zeile = self.table.rowCount()
            self.table.insertRow(zeile)

            werte = [
                fahrzeug.sortierung,
                fahrzeug.kennzeichen,
                fahrzeug.fahrzeugtyp,
                fahrzeug.standort,
                fahrzeug.fahreranzahl,
                fahrzeug.trailer_kategorie,
                "Aktiv" if fahrzeug.aktiv else "Inaktiv",
            ]

            for spalte, wert in enumerate(werte):

                item = QTableWidgetItem(str(wert))

                item.setData(Qt.UserRole, fahrzeug.id)

                if not fahrzeug.aktiv:
                    item.setForeground(Qt.gray)

                self.table.setItem(zeile, spalte, item)

    # -------------------------------------------------

    def aktuelles_fahrzeug(self):

        zeile = self.table.currentRow()

        if zeile < 0:
            return None

        fahrzeug_id = self.table.item(zeile,0).data(Qt.UserRole)

        return self.session.get(Fahrzeug, fahrzeug_id)

    # -------------------------------------------------

    def neu(self):

        dialog = FahrzeugDialog(parent=self)

        if dialog.exec():

            daten = dialog.daten()

            fahrzeug = Fahrzeug(**daten)

            self.session.add(fahrzeug)
            self.session.commit()

            self.laden()

    # -------------------------------------------------

    def bearbeiten(self):

        fahrzeug = self.aktuelles_fahrzeug()

        if not fahrzeug:

            QMessageBox.information(
                self,
                "Hinweis",
                "Bitte zuerst ein Fahrzeug auswählen."
            )
            return

        dialog = FahrzeugDialog(fahrzeug, self)

        if dialog.exec():

            daten = dialog.daten()

            for key, value in daten.items():
                setattr(fahrzeug, key, value)

            self.session.commit()

            self.laden()

    # -------------------------------------------------

    def deaktivieren(self):

        fahrzeug = self.aktuelles_fahrzeug()

        if not fahrzeug:

            QMessageBox.information(
                self,
                "Hinweis",
                "Bitte zuerst ein Fahrzeug auswählen."
            )
            return

        antwort = QMessageBox.question(
            self,
            "Fahrzeug deaktivieren",
            f"{fahrzeug.kennzeichen} wirklich deaktivieren?"
        )

        if antwort != QMessageBox.Yes:
            return

        fahrzeug.aktiv = False

        self.session.commit()

        self.laden()
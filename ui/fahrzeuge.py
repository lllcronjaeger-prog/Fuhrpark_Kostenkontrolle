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
)

from database.database import SessionLocal
from database.models import Fahrzeug

from .dialogs.fahrzeug_dialog import FahrzeugDialog


class FahrzeugeSeite(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titel = QLabel("Fahrzeuge")

        titel.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(titel)

        oben = QHBoxLayout()

        self.suche = QLineEdit()
        self.suche.setPlaceholderText("Kennzeichen suchen...")

        self.suche.textChanged.connect(self.laden)

        neu = QPushButton("Neues Fahrzeug")

        neu.clicked.connect(self.neues_fahrzeug)

        oben.addWidget(self.suche)
        oben.addWidget(neu)

        layout.addLayout(oben)

        self.tabelle = QTableWidget()

        self.tabelle.setColumnCount(5)

        self.tabelle.setHorizontalHeaderLabels([
            "Kennzeichen",
            "Typ",
            "Standort",
            "Fahrer",
            "Trailer",
        ])

        self.tabelle.doubleClicked.connect(self.bearbeiten)

        layout.addWidget(self.tabelle)

        self.laden()

    def laden(self):

        db = SessionLocal()

        suche = self.suche.text()

        query = db.query(Fahrzeug).filter(Fahrzeug.aktiv == True)

        if suche:
            query = query.filter(
                Fahrzeug.kennzeichen.contains(suche)
            )

        daten = query.order_by(Fahrzeug.kennzeichen).all()

        self.tabelle.setRowCount(len(daten))

        for r, f in enumerate(daten):

            self.tabelle.setItem(r, 0, QTableWidgetItem(f.kennzeichen))
            self.tabelle.setItem(r, 1, QTableWidgetItem(f.fahrzeugtyp))
            self.tabelle.setItem(r, 2, QTableWidgetItem(f.standort))
            self.tabelle.setItem(r, 3, QTableWidgetItem(str(f.fahreranzahl)))
            self.tabelle.setItem(r, 4, QTableWidgetItem(f.trailer_kategorie))

        self.fahrzeuge = daten

        db.close()

    def neues_fahrzeug(self):

        dlg = FahrzeugDialog()

        if dlg.exec():
            self.laden()

    def bearbeiten(self):

        row = self.tabelle.currentRow()

        if row < 0:
            return

        dlg = FahrzeugDialog(self.fahrzeuge[row])

        if dlg.exec():
            self.laden()
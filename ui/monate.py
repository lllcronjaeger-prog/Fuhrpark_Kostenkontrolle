from calendar import month_name

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem
)

from database.database import SessionLocal
from database.models import Monat

from .dialogs.monat_dialog import MonatDialog


class MonateSeite(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        titel = QLabel("Monatsverwaltung")

        titel.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
        """)

        layout.addWidget(titel)

        neu = QPushButton("Neuen Monat anlegen")

        neu.clicked.connect(self.neuer_monat)

        layout.addWidget(neu)

        self.tabelle = QTableWidget()

        self.tabelle.setColumnCount(3)

        self.tabelle.setHorizontalHeaderLabels([
            "Monat",
            "Status",
            "Erstellt"
        ])

        layout.addWidget(self.tabelle)

        self.laden()

    def laden(self):

        db = SessionLocal()

        monate = db.query(Monat).order_by(
            Monat.jahr.desc(),
            Monat.monat.desc()
        ).all()

        self.tabelle.setRowCount(len(monate))

        for r,m in enumerate(monate):

            self.tabelle.setItem(
                r,0,
                QTableWidgetItem(f"{month_name[m.monat]} {m.jahr}")
            )

            self.tabelle.setItem(
                r,1,
                QTableWidgetItem(m.status)
            )

            self.tabelle.setItem(
                r,2,
                QTableWidgetItem(str(m.erstellt_am))
            )

        db.close()

    def neuer_monat(self):

        dlg = MonatDialog()

        if dlg.exec():

            db = SessionLocal()

            monat = Monat(
                jahr=int(dlg.jahr.currentText()),
                monat=dlg.monat.currentIndex()+1
            )

            db.add(monat)
            db.commit()
            db.close()

            self.laden()
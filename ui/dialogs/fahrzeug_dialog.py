from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QDialogButtonBox,
)

from database.database import SessionLocal
from database.models import Fahrzeug


class FahrzeugDialog(QDialog):

    def __init__(self, fahrzeug=None):
        super().__init__()

        self.fahrzeug = fahrzeug

        self.setWindowTitle("Fahrzeug")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Kennzeichen"))

        self.kennzeichen = QLineEdit()
        layout.addWidget(self.kennzeichen)

        layout.addWidget(QLabel("Fahrzeugtyp"))

        self.typ = QComboBox()
        self.typ.addItems([
            "DAF XG",
            "DAF XF",
            "MAN TGX",
            "Mercedes Actros",
            "Scania",
            "Volvo",
            "Sonstiges",
        ])
        layout.addWidget(self.typ)

        layout.addWidget(QLabel("Standort"))

        self.standort = QComboBox()
        self.standort.addItems(["Leipzig", "Ettlingen"])
        layout.addWidget(self.standort)

        layout.addWidget(QLabel("Fahrer"))

        self.fahrer = QComboBox()
        self.fahrer.addItems(["1", "2"])
        layout.addWidget(self.fahrer)

        layout.addWidget(QLabel("Trailerkategorie"))

        self.trailer = QComboBox()
        self.trailer.addItems([
            "Leipzig",
            "Ettlingen",
            "Reserve",
            "Vermietung",
            "Werkstatt",
        ])
        layout.addWidget(self.trailer)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Save | QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.speichern)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

        if fahrzeug:
            self.kennzeichen.setText(fahrzeug.kennzeichen)
            self.typ.setCurrentText(fahrzeug.fahrzeugtyp)
            self.standort.setCurrentText(fahrzeug.standort)
            self.fahrer.setCurrentText(str(fahrzeug.fahreranzahl))
            self.trailer.setCurrentText(fahrzeug.trailer_kategorie)

    def speichern(self):

        db = SessionLocal()

        if not self.fahrzeug:
            self.fahrzeug = Fahrzeug()

        self.fahrzeug.kennzeichen = self.kennzeichen.text()
        self.fahrzeug.fahrzeugtyp = self.typ.currentText()
        self.fahrzeug.standort = self.standort.currentText()
        self.fahrzeug.fahreranzahl = int(self.fahrer.currentText())
        self.fahrzeug.trailer_kategorie = self.trailer.currentText()

        db.add(self.fahrzeug)
        db.commit()

        db.close()

        self.accept()
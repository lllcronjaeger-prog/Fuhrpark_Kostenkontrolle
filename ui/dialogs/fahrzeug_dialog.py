"""
Release: v0.6.1
Datei: ui/dialogs/fahrzeug_dialog.py
Komplette Datei
"""

from sqlalchemy import func

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QSpinBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
)

from config import COLORS
from database.database import SessionLocal
from database.models import Fahrzeug


class FahrzeugDialog(QDialog):
    """
    Dialog zum Anlegen oder Bearbeiten eines Fahrzeugs.
    """

    def __init__(self, fahrzeug=None, parent=None):
        super().__init__(parent)

        self.fahrzeug = fahrzeug
        self.session = SessionLocal()

        self.setWindowTitle("Fahrzeug")
        self.resize(500, 520)

        self.setStyleSheet(f"""
            QDialog {{
                background:{COLORS["hell"]};
            }}

            QLabel {{
                color:#17365D;
                font-size:13px;
                font-weight:bold;
            }}

            QLineEdit,
            QComboBox,
            QSpinBox {{
                background:white;
                color:#202020;
                border:1px solid #C8C8C8;
                border-radius:8px;
                padding:6px;
                min-height:28px;
            }}

            /* Geöffnetes Dropdown */
            QComboBox QAbstractItemView {{
                background:white;
                color:#202020;
                selection-background-color:{COLORS["orange"]};
                selection-color:black;
                border:1px solid #C8C8C8;
            }}

            QPushButton {{
                border:none;
                border-radius:10px;
                padding:10px;
                font-weight:bold;
            }}
        """)

        self._aufbauen()

        if self.fahrzeug:
            self._laden()
        else:
            self._naechste_sortierung()

    # -----------------------------------------------------

    def _aufbauen(self):

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(16)

        titel = QLabel(
            "Fahrzeug bearbeiten"
            if self.fahrzeug
            else "Neues Fahrzeug"
        )

        titel.setStyleSheet(f"""
            font-size:24px;
            color:{COLORS["blau"]};
            font-weight:bold;
        """)

        layout.addWidget(titel)

        # Sortierung

        layout.addWidget(QLabel("Sortierreihenfolge"))

        self.sortierung = QSpinBox()
        self.sortierung.setRange(1, 9999)

        layout.addWidget(self.sortierung)

        # Kennzeichen

        layout.addWidget(QLabel("Kennzeichen"))

        self.kennzeichen = QLineEdit()
        self.kennzeichen.setPlaceholderText("z.B. KA-LL 8031")

        layout.addWidget(self.kennzeichen)

        # Fahrzeugtyp

        layout.addWidget(QLabel("Fahrzeugtyp"))

        self.fahrzeugtyp = QComboBox()
        self.fahrzeugtyp.addItems([
            "Sattelzugmaschine",
            "Wechselbrücke",
            "Transporter",
            "Sonstiges",
        ])

        layout.addWidget(self.fahrzeugtyp)

        # Standort

        layout.addWidget(QLabel("Standort"))

        self.standort = QComboBox()
        self.standort.setEditable(True)

        self.standort.addItems([
            "Leipzig",
            "Ettlingen",
        ])

        layout.addWidget(self.standort)

        # Fahreranzahl

        layout.addWidget(QLabel("Fahreranzahl"))

        self.fahrer = QComboBox()
        self.fahrer.addItems(["1", "2"])

        layout.addWidget(self.fahrer)

        # Trailerkategorie

        layout.addWidget(QLabel("Trailerkategorie"))

        self.trailer = QComboBox()
        self.trailer.setEditable(True)

        self.trailer.addItems([
            "Standard",
            "Mega",
            "Koffer",
            "Kühler",
        ])

        layout.addWidget(self.trailer)

        # Aktiv

        self.aktiv = QCheckBox("Fahrzeug aktiv")
        self.aktiv.setChecked(True)

        layout.addWidget(self.aktiv)

        layout.addStretch()

        # Buttons

        buttons = QHBoxLayout()

        self.cancel = QPushButton("Abbrechen")
        self.cancel.clicked.connect(self.reject)

        self.cancel.setStyleSheet("""
            QPushButton{
                background:#CFCFCF;
                color:black;
            }

            QPushButton:hover{
                background:#BBBBBB;
            }
        """)

        self.save = QPushButton("Speichern")
        self.save.clicked.connect(self.speichern)

        self.save.setStyleSheet(f"""
            QPushButton{{
                background:{COLORS["orange"]};
                color:black;
            }}

            QPushButton:hover{{
                background:#E07D00;
            }}
        """)

        buttons.addWidget(self.cancel)
        buttons.addWidget(self.save)

        layout.addLayout(buttons)

    # -----------------------------------------------------

    def _naechste_sortierung(self):
        """
        Vergibt automatisch die nächste freie Sortierung.
        Beispiel:
        10 -> 20 -> 30 -> 40
        """

        letzte = self.session.query(
            func.max(Fahrzeug.sortierung)
        ).scalar()

        if letzte is None:
            self.sortierung.setValue(10)
        else:
            self.sortierung.setValue(letzte + 10)

    # -----------------------------------------------------

    def _laden(self):

        self.sortierung.setValue(self.fahrzeug.sortierung)

        self.kennzeichen.setText(self.fahrzeug.kennzeichen)

        self.fahrzeugtyp.setCurrentText(self.fahrzeug.fahrzeugtyp)

        self.standort.setCurrentText(self.fahrzeug.standort)

        self.fahrer.setCurrentText(str(self.fahrzeug.fahreranzahl))

        self.trailer.setCurrentText(self.fahrzeug.trailer_kategorie)

        self.aktiv.setChecked(self.fahrzeug.aktiv)

    # -----------------------------------------------------

    def speichern(self):

        kennzeichen = self.kennzeichen.text().strip().upper()

        if not kennzeichen:
            QMessageBox.warning(
                self,
                "Fehler",
                "Bitte ein Kennzeichen eingeben."
            )
            return

        self.accept()

    # -----------------------------------------------------

    def daten(self):

        return {
            "sortierung": self.sortierung.value(),
            "kennzeichen": self.kennzeichen.text().strip().upper(),
            "fahrzeugtyp": self.fahrzeugtyp.currentText(),
            "standort": self.standort.currentText().strip(),
            "fahreranzahl": int(self.fahrer.currentText()),
            "trailer_kategorie": self.trailer.currentText().strip(),
            "aktiv": self.aktiv.isChecked(),
        }
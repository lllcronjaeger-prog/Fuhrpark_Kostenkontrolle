"""
Release: v0.6.2
Datei: ui/monatserfassung.py
Komplette Datei
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
)

from config import COLORS
from database.database import SessionLocal
from database.models import Fahrzeug, Monat, Monatsdaten
from ui.app_state import app_state


class MonatsErfassung(QWidget):

    kpisChanged = Signal(dict)

    def __init__(self):
        super().__init__()

        self.session = SessionLocal()

        self.setStyleSheet(f"""
            QWidget {{
                background:{COLORS["hell"]};
            }}

            QTableWidget {{
                background:white;
                color:#202020;
                alternate-background-color:#F8F8F8;
                gridline-color:#DADADA;
                border:1px solid #DADADA;
                selection-background-color:{COLORS["orange"]};
                selection-color:black;
                font-size:13px;
            }}

            QTableWidget::item {{
                color:#202020;
            }}

            QLineEdit {{
                color:#202020;
                background:white;
            }}

            QHeaderView::section {{
                background:#ECECEC;
                color:#17365D;
                font-weight:bold;
                border:none;
                padding:8px;
            }}
        """)

        self.monat = self.hole_oder_erzeuge_monat()

        haupt = QHBoxLayout(self)
        haupt.setContentsMargins(20,20,20,20)
        haupt.setSpacing(20)

        # ---------------- Tabelle ----------------

        links = QVBoxLayout()

        titel = QLabel("Monatserfassung")

        titel.setStyleSheet(f"""
            font-size:30px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)

        links.addWidget(titel)

        self.table = QTableWidget(0,7)

        self.table.setHorizontalHeaderLabels([
            "Fahrzeug",
            "Diesel",
            "Maut",
            "Werkstatt",
            "Sonstiges",
            "Umsatz",
            "KM"
        ])

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(34)

        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)

        self.table.itemChanged.connect(self.speichern_und_berechnen)

        links.addWidget(self.table)

        haupt.addLayout(links,4)

        # ---------------- KPI ----------------

        rechts = QVBoxLayout()

        self.labels = []

        for name in [
            "Diesel",
            "Maut",
            "Werkstatt",
            "Sonstiges",
            "Umsatz",
            "KM"
        ]:

            frame = QFrame()

            frame.setMinimumHeight(85)

            frame.setStyleSheet("""
                background:white;
                border:1px solid #DDDDDD;
                border-radius:16px;
            """)

            l = QVBoxLayout(frame)

            oben = QLabel(name)
            oben.setStyleSheet("font-size:12px;font-weight:bold;color:#666666;")

            wert = QLabel("0")
            wert.setAlignment(Qt.AlignCenter)

            wert.setStyleSheet(f"""
                font-size:24px;
                font-weight:bold;
                color:{COLORS["blau"]};
            """)

            l.addWidget(oben)
            l.addWidget(wert)

            self.labels.append(wert)

            rechts.addWidget(frame)

        rechts.addStretch()

        haupt.addLayout(rechts,1)

        self.laden()

    # -----------------------------------------------------

    def hole_oder_erzeuge_monat(self):

        monat = self.session.query(Monat).filter_by(
            jahr=app_state.jahr,
            monat=app_state.monat
        ).first()

        if monat:
            return monat

        monat = Monat(
            jahr=app_state.jahr,
            monat=app_state.monat
        )

        self.session.add(monat)
        self.session.commit()

        fahrzeuge = (
            self.session.query(Fahrzeug)
            .filter_by(aktiv=True)
            .order_by(Fahrzeug.sortierung)
            .all()
        )

        for fahrzeug in fahrzeuge:

            self.session.add(
                Monatsdaten(
                    fahrzeug_id=fahrzeug.id,
                    monat_id=monat.id
                )
            )

        self.session.commit()

        return monat

    # -----------------------------------------------------

    def laden(self):

        self.table.blockSignals(True)

        self.table.setRowCount(0)

        daten = (
            self.session.query(Monatsdaten)
            .join(Fahrzeug)
            .filter(Monatsdaten.monat_id == self.monat.id)
            .order_by(Fahrzeug.sortierung)
            .all()
        )

        for ds in daten:

            r = self.table.rowCount()
            self.table.insertRow(r)

            name = ds.fahrzeug.kennzeichen

            if ds.fahrzeug.fahreranzahl == 2:
                name += " (2 Fahrer)"

            item = QTableWidgetItem(name)
            item.setData(Qt.UserRole, ds.id)

            self.table.setItem(r,0,item)

            werte = [
                ds.diesel,
                ds.maut,
                ds.werkstatt,
                ds.sonstiges,
                ds.umsatz,
                ds.kilometer
            ]

            for s,w in enumerate(werte,start=1):

                z = QTableWidgetItem(
                    "" if w == 0 else str(int(w))
                )

                z.setData(Qt.UserRole, ds.id)

                self.table.setItem(r,s,z)

        # Zusatzzeilen

        for text in [
            "👤 Zusatzfahrer",
            "🚛 Zusatztrailer"
        ]:

            r = self.table.rowCount()

            self.table.insertRow(r)

            item = QTableWidgetItem(text)

            item.setBackground(QColor("#D9EAF7"))

            self.table.setItem(r,0,item)

        self.table.blockSignals(False)

        self.berechne_kpis()

    # -----------------------------------------------------

    def speichern_und_berechnen(self,item):

        ds_id = item.data(Qt.UserRole)

        if ds_id is None:
            return

        ds = self.session.get(Monatsdaten,ds_id)

        mapping = {
            1:"diesel",
            2:"maut",
            3:"werkstatt",
            4:"sonstiges",
            5:"umsatz",
            6:"kilometer"
        }

        if item.column() not in mapping:
            return

        try:
            wert = float(item.text().replace(",","."))
        except:
            wert = 0

        setattr(ds,mapping[item.column()],wert)

        self.session.commit()

        self.berechne_kpis()

    # -----------------------------------------------------

    def berechne_kpis(self):

        daten = (
            self.session.query(Monatsdaten)
            .filter_by(monat_id=self.monat.id)
            .all()
        )

        kpi = {
            "Diesel":0,
            "Maut":0,
            "Werkstatt":0,
            "Sonstiges":0,
            "Umsatz":0,
            "KM":0
        }

        for d in daten:

            kpi["Diesel"] += d.diesel
            kpi["Maut"] += d.maut
            kpi["Werkstatt"] += d.werkstatt
            kpi["Sonstiges"] += d.sonstiges
            kpi["Umsatz"] += d.umsatz
            kpi["KM"] += d.kilometer

        self.labels[0].setText(f"{kpi['Diesel']:,.0f} €".replace(",","."))
        self.labels[1].setText(f"{kpi['Maut']:,.0f} €".replace(",","."))
        self.labels[2].setText(f"{kpi['Werkstatt']:,.0f} €".replace(",","."))
        self.labels[3].setText(f"{kpi['Sonstiges']:,.0f} €".replace(",","."))
        self.labels[4].setText(f"{kpi['Umsatz']:,.0f} €".replace(",","."))
        self.labels[5].setText(f"{kpi['KM']:,.0f} km".replace(",", "."))

        self.kpisChanged.emit(kpi)
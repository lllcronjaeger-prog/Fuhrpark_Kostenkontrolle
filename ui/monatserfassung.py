"""
Release: v0.6.3
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
    QStyledItemDelegate,
    QLineEdit,
    QGridLayout,
    QSpinBox,
    QDoubleSpinBox,
)

from config import COLORS
from database.database import SessionLocal
from database.models import Fahrzeug, Monat, Monatsdaten, MonatsKennzahlen
from ui.app_state import app_state

class DunklerEditor(QStyledItemDelegate):
    """
    Sorgt dafür, dass Tabellenzellen beim Bearbeiten
    schwarze Schrift auf weißem Hintergrund haben.
    """

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent)
        editor.setStyleSheet("""
            QLineEdit{
                color:#202020;
                background:white;
                selection-color:black;
                selection-background-color:#FFD27A;
            }
        """)
        return editor
    
class MonatsErfassung(QWidget):

    kpisChanged = Signal(dict)

    def __init__(self):
        super().__init__()

        self.session = SessionLocal()

        self.setStyleSheet(f"""
            QWidget{{background:{COLORS["hell"]};}}

            QTableWidget{{
                background:white;
                color:#202020;
                alternate-background-color:#F8F8F8;
                gridline-color:#DADADA;
                border:1px solid #DADADA;
                selection-background-color:{COLORS["orange"]};
                selection-color:black;
            }}

            QTableWidget::item{{color:#202020;}}

            QHeaderView::section{{
                background:#ECECEC;
                color:#17365D;
                font-weight:bold;
                padding:8px;
                border:none;
            }}
        """)

        self.monat = None

        haupt = QHBoxLayout(self)
        haupt.setContentsMargins(20,20,20,20)
        haupt.setSpacing(20)

        links = QVBoxLayout()

        titel = QLabel("Monatserfassung")
        titel.setStyleSheet(f"""
            font-size:30px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)
        links.addWidget(titel)

        # ---------------- Monatskopf ----------------
        kopf = QFrame()
        kopf.setStyleSheet("""
            QFrame{
                background:white;
                border:1px solid #DDDDDD;
                border-radius:14px;
            }
            QLabel{color:#17365D;font-weight:bold;}
        """)
        grid = QGridLayout(kopf)

        self.zusatzfahrer = QSpinBox()
        self.zusatztrailer = QSpinBox()

        self.avg_fahrer_lp = QDoubleSpinBox()
        self.avg_trailer_lp = QDoubleSpinBox()
        self.avg_fahrer_et = QDoubleSpinBox()
        self.avg_trailer_et = QDoubleSpinBox()

        for box in [self.avg_fahrer_lp,self.avg_trailer_lp,self.avg_fahrer_et,self.avg_trailer_et]:
            box.setMaximum(999999)
            box.setSuffix(" €")
            box.setStyleSheet("color:#202020;background:white;")

        self.zusatzfahrer.setStyleSheet("color:#202020;background:white;")
        self.zusatztrailer.setStyleSheet("color:#202020;background:white;")

        grid.addWidget(QLabel("Zusatzfahrer"),0,0)
        grid.addWidget(self.zusatzfahrer,0,1)
        grid.addWidget(QLabel("Zusatztrailer"),0,2)
        grid.addWidget(self.zusatztrailer,0,3)

        grid.addWidget(QLabel("Ø Fahrer Leipzig"),1,0)
        grid.addWidget(self.avg_fahrer_lp,1,1)
        grid.addWidget(QLabel("Ø Trailerkosten Leipzig"),1,2)
        grid.addWidget(self.avg_trailer_lp,1,3)

        grid.addWidget(QLabel("Ø Fahrer Ettlingen"),2,0)
        grid.addWidget(self.avg_fahrer_et,2,1)
        grid.addWidget(QLabel("Ø Trailerkosten Ettlingen"),2,2)
        grid.addWidget(self.avg_trailer_et,2,3)

        self.status_label = QLabel("Status: In Bearbeitung (Speichern folgt im nächsten Schritt)")
        grid.addWidget(self.status_label,3,0,1,4)

        links.addWidget(kopf)

        self.table = QTableWidget(0,9)
        self.table.setHorizontalHeaderLabels([
            "Fahrzeug","Fahrer","Trailer","Diesel","Maut","Werkstatt","Sonstiges","Umsatz","KM"
        ])

        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setDefaultSectionSize(34)
        self.table.setAlternatingRowColors(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setItemDelegate(DunklerEditor())

        self.table.itemChanged.connect(self.speichern_und_berechnen)

        links.addWidget(self.table)

        haupt.addLayout(links,4)

        rechts = QVBoxLayout()
        self.labels=[]

        for name in [
            "Diesel","Maut","Werkstatt",
            "Sonstiges","Umsatz","KM"
        ]:

            frame=QFrame()
            frame.setMinimumHeight(85)

            frame.setStyleSheet("""
                background:white;
                border:1px solid #DDDDDD;
                border-radius:16px;
            """)

            l=QVBoxLayout(frame)

            oben=QLabel(name)
            oben.setStyleSheet("font-size:12px;font-weight:bold;color:#666666;")

            wert=QLabel("0")
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

        self.aktualisieren()

    # -----------------------------------------------------

    def aktualisieren(self):
        """Synchronisiert den aktuellen Monat mit allen aktiven Fahrzeugen."""

        self.monat = self._hole_monat()

        aktive = (
            self.session.query(Fahrzeug)
            .filter_by(aktiv=True)
            .order_by(Fahrzeug.sortierung)
            .all()
        )

        vorhanden = {
            d.fahrzeug_id
            for d in self.session.query(Monatsdaten)
            .filter_by(monat_id=self.monat.id)
            .all()
        }

        geaendert=False

        for fahrzeug in aktive:

            if fahrzeug.id not in vorhanden:

                self.session.add(
                    Monatsdaten(
                        fahrzeug_id=fahrzeug.id,
                        monat_id=self.monat.id
                    )
                )

                geaendert=True

        if geaendert:
            self.session.commit()

        self.laden()

    # -----------------------------------------------------

    def _hole_monat(self):

        monat=self.session.query(Monat).filter_by(
            jahr=app_state.jahr,
            monat=app_state.monat
        ).first()

        if monat:
            return monat

        monat=Monat(
            jahr=app_state.jahr,
            monat=app_state.monat
        )

        self.session.add(monat)
        self.session.commit()

        return monat

    # -----------------------------------------------------

    def laden(self):

        self.table.blockSignals(True)
        self.table.setRowCount(0)

        daten=(
            self.session.query(Monatsdaten)
            .join(Fahrzeug)
            .filter(Monatsdaten.monat_id==self.monat.id)
            .order_by(Fahrzeug.sortierung)
            .all()
        )

        for ds in daten:

            r=self.table.rowCount()
            self.table.insertRow(r)

            item=QTableWidgetItem(ds.fahrzeug.kennzeichen)
            item.setData(Qt.UserRole,ds.id)
            self.table.setItem(r,0,item)

            fahrer=QTableWidgetItem(str(ds.fahrzeug.fahreranzahl))
            fahrer.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(r,1,fahrer)

            trailer_name = ""

            if ds.fahrzeug.trailer is not None:
                trailer_name = ds.fahrzeug.trailer.bezeichnung

            trailer = QTableWidgetItem(trailer_name)
            trailer.setFlags(Qt.ItemIsEnabled)
            self.table.setItem(r,2,trailer)

            werte=[
                ds.diesel,
                ds.maut,
                ds.werkstatt,
                ds.sonstiges,
                ds.umsatz,
                ds.kilometer
            ]

            for s,w in enumerate(werte,start=3):

                z=QTableWidgetItem("" if w==0 else str(int(w)))
                z.setData(Qt.UserRole,ds.id)

                self.table.setItem(r,s,z)

        self.table.blockSignals(False)

        self.berechne_kpis()

    # -----------------------------------------------------

    def speichern_und_berechnen(self,item):

        ds=self.session.get(
            Monatsdaten,
            item.data(Qt.UserRole)
        )

        if ds is None:
            return

        mapping={
            3:"diesel",
            4:"maut",
            5:"werkstatt",
            6:"sonstiges",
            7:"umsatz",
            8:"kilometer"
        }

        if item.column() not in mapping:
            return

        try:
            wert=float(item.text().replace(",","."))
        except:
            wert=0

        setattr(ds,mapping[item.column()],wert)

        self.session.commit()

        self.berechne_kpis()

    # -----------------------------------------------------

    def berechne_kpis(self):

        daten=self.session.query(Monatsdaten).filter_by(
            monat_id=self.monat.id
        ).all()

        kpi={
            "Diesel":0,
            "Maut":0,
            "Werkstatt":0,
            "Sonstiges":0,
            "Umsatz":0,
            "KM":0
        }

        for d in daten:
            kpi["Diesel"]+=d.diesel
            kpi["Maut"]+=d.maut
            kpi["Werkstatt"]+=d.werkstatt
            kpi["Sonstiges"]+=d.sonstiges
            kpi["Umsatz"]+=d.umsatz
            kpi["KM"]+=d.kilometer

        self.labels[0].setText(f"{kpi['Diesel']:,.0f} €".replace(",","."))
        self.labels[1].setText(f"{kpi['Maut']:,.0f} €".replace(",","."))
        self.labels[2].setText(f"{kpi['Werkstatt']:,.0f} €".replace(",","."))
        self.labels[3].setText(f"{kpi['Sonstiges']:,.0f} €".replace(",","."))
        self.labels[4].setText(f"{kpi['Umsatz']:,.0f} €".replace(",","."))
        self.labels[5].setText(f"{kpi['KM']:,.0f} km".replace(",", "."))

        self.kpisChanged.emit(kpi)
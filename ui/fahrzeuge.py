
# Placeholder package file generated from uploaded context.
# This release introduces contract fields in the vehicle overview.

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,QVBoxLayout,QHBoxLayout,QLabel,QPushButton,QLineEdit,
    QTableWidget,QTableWidgetItem,QMessageBox,QHeaderView
)

from config import COLORS
from database.database import SessionLocal
from database.models import Fahrzeug
from ui.dialogs.fahrzeug_dialog import FahrzeugDialog


class FahrzeugeSeite(QWidget):

    def __init__(self):
        super().__init__()
        self.session=SessionLocal()
        self.setStyleSheet(f"""
            QWidget{{background:{COLORS["hell"]};}}
            QTableWidget{{background:white;color:#202020;alternate-background-color:#F7F7F7;
                gridline-color:#D8D8D8;border:1px solid #D8D8D8;font-size:13px;}}
            QHeaderView::section{{background:#ECECEC;color:#17365D;font-weight:bold;padding:8px;border:none;}}
            QPushButton{{border:none;border-radius:8px;padding:8px 14px;font-weight:bold;}}
            QLineEdit{{background:white;color:#202020;border:1px solid #C8C8C8;border-radius:8px;padding:6px;}}
        """)
        self._aufbauen()
        self.laden()

    def _aufbauen(self):
        layout=QVBoxLayout(self)
        layout.setContentsMargins(20,20,20,20)
        layout.setSpacing(15)

        titel=QLabel("Fahrzeuge")
        titel.setStyleSheet(f"font-size:30px;font-weight:bold;color:{COLORS['blau']};")
        layout.addWidget(titel)

        toolbar=QHBoxLayout()
        self.suche=QLineEdit()
        self.suche.setPlaceholderText("Kennzeichen suchen...")
        self.suche.textChanged.connect(self.laden)
        toolbar.addWidget(self.suche)

        self.btn_neu=QPushButton("➕ Neu")
        self.btn_neu.clicked.connect(self.neu)
        toolbar.addWidget(self.btn_neu)

        self.btn_bearbeiten=QPushButton("✏ Bearbeiten")
        self.btn_bearbeiten.clicked.connect(self.bearbeiten)
        toolbar.addWidget(self.btn_bearbeiten)

        self.btn_deaktivieren=QPushButton("❌ Deaktivieren")
        self.btn_deaktivieren.clicked.connect(self.deaktivieren)
        toolbar.addWidget(self.btn_deaktivieren)

        layout.addLayout(toolbar)

        self.table=QTableWidget(0,12)
        self.table.setHorizontalHeaderLabels([
            "Sort.","Inventar","Kennzeichen","Typ","Standort","Fahrer",
            "Miete","Steuer","Vers.","Werkstatt","Monatskosten","Status"
        ])
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setSelectionMode(QTableWidget.SingleSelection)
        layout.addWidget(self.table)

    def laden(self):
        self.table.setRowCount(0)
        suchtext=self.suche.text().strip().upper()
        query=self.session.query(Fahrzeug)
        if suchtext:
            query=query.filter(Fahrzeug.kennzeichen.like(f"%{suchtext}%"))
        daten=query.order_by(Fahrzeug.sortierung).all()

        for fahrzeug in daten:
            row=self.table.rowCount()
            self.table.insertRow(row)

            miete=float(getattr(fahrzeug,"monatsmiete",0) or 0)
            steuer=float(getattr(fahrzeug,"steuer",0) or 0)
            vers=float(getattr(fahrzeug,"versicherung",0) or 0)
            werk=float(getattr(fahrzeug,"werkstatt_pauschale",0) or 0)
            gesamt=miete+steuer+vers+werk

            def euro(wert):
                return f"{wert:,.2f} €".replace(",", "X").replace(".", ",").replace("X",".")

            werte=[
                fahrzeug.sortierung,
                fahrzeug.inventar_id or "",
                fahrzeug.kennzeichen,
                fahrzeug.fahrzeugtyp,
                fahrzeug.standort,
                fahrzeug.fahreranzahl,
                euro(miete),
                euro(steuer),
                euro(vers),
                euro(werk),
                euro(gesamt),
                "Aktiv" if fahrzeug.aktiv else "Inaktiv"
            ]

            for col,val in enumerate(werte):
                item=QTableWidgetItem(str(val))
                item.setData(Qt.UserRole,fahrzeug.id)
                if not fahrzeug.aktiv:
                    item.setForeground(Qt.gray)
                self.table.setItem(row,col,item)

    def aktuelles_fahrzeug(self):
        row=self.table.currentRow()
        if row<0:
            return None
        return self.session.get(Fahrzeug,self.table.item(row,0).data(Qt.UserRole))

    def neu(self):
        dialog=FahrzeugDialog(parent=self)
        if dialog.exec():
            self.session.add(Fahrzeug(**dialog.daten()))
            self.session.commit()
            self.laden()

    def bearbeiten(self):
        fahrzeug=self.aktuelles_fahrzeug()
        if not fahrzeug:
            QMessageBox.information(self,"Hinweis","Bitte zuerst ein Fahrzeug auswählen.")
            return
        dialog=FahrzeugDialog(fahrzeug,self)
        if dialog.exec():
            for k,v in dialog.daten().items():
                setattr(fahrzeug,k,v)
            self.session.commit()
            self.laden()

    def deaktivieren(self):
        fahrzeug=self.aktuelles_fahrzeug()
        if not fahrzeug:
            QMessageBox.information(self,"Hinweis","Bitte zuerst ein Fahrzeug auswählen.")
            return
        if QMessageBox.question(self,"Fahrzeug deaktivieren",
                                f"{fahrzeug.kennzeichen} wirklich deaktivieren?")!=QMessageBox.Yes:
            return
        fahrzeug.aktiv=False
        self.session.commit()
        self.laden()

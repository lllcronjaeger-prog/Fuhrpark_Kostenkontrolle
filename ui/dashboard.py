from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)

from config import COLORS


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            QWidget {{
                background:{COLORS["hell"]};
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(25, 25, 25, 25)
        layout.setSpacing(20)

        titel = QLabel("Dashboard")
        titel.setStyleSheet(f"""
            font-size:28px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)

        layout.addWidget(titel)

        kpis = QHBoxLayout()
        kpis.setSpacing(15)

        self.lbl_fahrzeuge = self.karte("Fahrzeuge", "--")
        self.lbl_trailer = self.karte("Trailer", "--")
        self.lbl_fahrer = self.karte("Fahrer", "--")
        self.lbl_umsatz = self.karte("Umsatz", "0 €")

        kpis.addWidget(self.lbl_fahrzeuge["frame"])
        kpis.addWidget(self.lbl_trailer["frame"])
        kpis.addWidget(self.lbl_fahrer["frame"])
        kpis.addWidget(self.lbl_umsatz["frame"])

        layout.addLayout(kpis)

        self.lbl_diesel = self.karte("Diesel", "0 €")
        self.lbl_maut = self.karte("Maut", "0 €")
        self.lbl_werkstatt = self.karte("Werkstatt", "0 €")
        self.lbl_sonstiges = self.karte("Sonstiges", "0 €")
        self.lbl_km = self.karte("Kilometer", "0 km")

        kosten = QHBoxLayout()
        kosten.setSpacing(15)

        kosten.addWidget(self.lbl_diesel["frame"])
        kosten.addWidget(self.lbl_maut["frame"])
        kosten.addWidget(self.lbl_werkstatt["frame"])
        kosten.addWidget(self.lbl_sonstiges["frame"])
        kosten.addWidget(self.lbl_km["frame"])

        layout.addLayout(kosten)

        diagramm = QFrame()
        diagramm.setStyleSheet("""
            background:white;
            border:1px solid #D8D8D8;
            border-radius:18px;
        """)

        d = QVBoxLayout(diagramm)

        text = QLabel("Diagramme und Auswertungen (v0.6)")
        text.setAlignment(Qt.AlignCenter)
        text.setStyleSheet("font-size:18px;color:#777777;")

        d.addWidget(text)

        layout.addWidget(diagramm)

    def karte(self, titel, wert):

        frame = QFrame()

        frame.setMinimumHeight(110)

        frame.setStyleSheet("""
            background:white;
            border:1px solid #DDDDDD;
            border-radius:18px;
        """)

        layout = QVBoxLayout(frame)

        oben = QLabel(titel)
        oben.setStyleSheet("font-size:13px;color:#666666;")

        mitte = QLabel(wert)
        mitte.setAlignment(Qt.AlignCenter)

        mitte.setStyleSheet("""
            font-size:28px;
            font-weight:bold;
            color:#17365D;
        """)

        layout.addWidget(oben)
        layout.addWidget(mitte)

        return {
            "frame": frame,
            "label": mitte
        }

    def update_kpis(self, daten):

        self.lbl_diesel["label"].setText(f"{daten['Diesel']:,.0f} €".replace(",", "."))
        self.lbl_maut["label"].setText(f"{daten['Maut']:,.0f} €".replace(",", "."))
        self.lbl_werkstatt["label"].setText(f"{daten['Werkstatt']:,.0f} €".replace(",", "."))
        self.lbl_sonstiges["label"].setText(f"{daten['Sonstiges']:,.0f} €".replace(",", "."))
        self.lbl_umsatz["label"].setText(f"{daten['Umsatz']:,.0f} €".replace(",", "."))
        self.lbl_km["label"].setText(f"{daten['KM']:,.0f} km".replace(",", "."))
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

        self.fahrzeuge = self.karte("Fahrzeuge", "--")
        self.trailer = self.karte("Trailer", "--")
        self.fahrer = self.karte("Fahrer", "--")
        self.umsatz = self.karte("Umsatz", "-- €")

        kpis.addWidget(self.fahrzeuge)
        kpis.addWidget(self.trailer)
        kpis.addWidget(self.fahrer)
        kpis.addWidget(self.umsatz)

        layout.addLayout(kpis)

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
            font-size:30px;
            font-weight:bold;
            color:#17365D;
        """)

        layout.addWidget(oben)
        layout.addWidget(mitte)

        return frame
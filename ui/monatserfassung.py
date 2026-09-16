from PySide6.QtCore import Qt
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


class MonatsErfassung(QWidget):

    def __init__(self):
        super().__init__()

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

            QHeaderView::section {{
                background:#ECECEC;
                color:#17365D;
                font-weight:bold;
                border:none;
                padding:8px;
            }}

            QTableCornerButton::section {{
                background:#ECECEC;
                border:none;
            }}
        """)

        haupt = QHBoxLayout(self)
        haupt.setContentsMargins(20,20,20,20)
        haupt.setSpacing(20)

        # ---------- Linke Seite ----------

        links = QVBoxLayout()
        links.setSpacing(15)

        titel = QLabel("Monatserfassung")

        titel.setStyleSheet(f"""
            font-size:30px;
            font-weight:bold;
            color:{COLORS["blau"]};
        """)

        links.addWidget(titel)

        self.table = QTableWidget(7,7)

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

        fahrzeuge = [
            "KA-LL 8031",
            "KA-LL 8032",
            "KA-LL 8045",
            "TS-ZM 1510",
            "👤 Zusatzfahrer",
            "🚛 Zusatztrailer",
            "Σ Summe"
        ]

        for zeile, name in enumerate(fahrzeuge):

            item = QTableWidgetItem(name)

            item.setForeground(QColor("#202020"))

            if "Zusatz" in name:
                item.setBackground(QColor("#D9EAF7"))

            if name.startswith("Σ"):
                item.setBackground(QColor(COLORS["orange"]))
                item.setForeground(QColor("black"))

            self.table.setItem(zeile,0,item)

        self.table.itemChanged.connect(self.berechne_summen)

        links.addWidget(self.table)

        haupt.addLayout(links,4)

        # ---------- Rechte Seite ----------

        rechts = QVBoxLayout()
        rechts.setSpacing(15)

        self.labels = []

        for text in [
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

            oben = QLabel(text)
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

    def berechne_summen(self):

        self.table.blockSignals(True)

        for spalte in range(1,7):

            gesamt = 0

            for zeile in range(6):

                item = self.table.item(zeile, spalte)

                if item:
                    try:
                        gesamt += float(item.text().replace(",", "."))
                    except ValueError:
                        pass

            text = f"{gesamt:,.0f}".replace(",", ".")

            if spalte == 6:
                self.labels[5].setText(text + " km")
            else:
                self.labels[spalte-1].setText(text + " €")

            summe = QTableWidgetItem(text)
            summe.setBackground(QColor(COLORS["orange"]))
            summe.setForeground(QColor("black"))

            self.table.setItem(6, spalte, summe)

        self.table.blockSignals(False)
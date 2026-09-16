from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QFrame,
    QSizePolicy,
)

from config import COLORS


class MonatsErfassung(QWidget):
    def __init__(self):
        super().__init__()

        self.setStyleSheet(f"""
            QWidget {{
                background:#1f1f1f;
                color:white;
            }}

            QTableWidget {{
                background:#252525;
                gridline-color:#333333;
                border:none;
                font-size:13px;
            }}

            QHeaderView::section {{
                background:#2d2d2d;
                color:white;
                border:none;
                padding:6px;
            }}
        """)

        haupt = QHBoxLayout(self)
        haupt.setContentsMargins(8,8,8,8)

        # -------------------------------------
        # Tabelle
        # -------------------------------------

        links = QVBoxLayout()

        titel = QLabel("Monatserfassung")

        titel.setStyleSheet(f"""
            font-size:24px;
            font-weight:bold;
            color:{COLORS["orange"]};
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

        fahrzeuge = [
            "KA-LL 8031",
            "KA-LL 8032",
            "KA-LL 8045",
            "TS-ZM 1510",
            "👤 Zusatzfahrer",
            "🚛 Zusatztrailer",
            "Σ Summe"
        ]

        for zeile,name in enumerate(fahrzeuge):

            item = QTableWidgetItem(name)

            if "Zusatz" in name:
                item.setBackground(QColor("#24415c"))

            if name.startswith("Σ"):
                item.setBackground(QColor(COLORS["orange"]))
                item.setForeground(QColor("black"))

            self.table.setItem(zeile,0,item)

        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.table.itemChanged.connect(self.berechne_summen)

        links.addWidget(self.table)

        haupt.addLayout(links,4)

        # -------------------------------------
        # Kontrollbereich
        # -------------------------------------

        rechts = QVBoxLayout()

        rechts.addWidget(self.karte("Diesel",0))
        rechts.addWidget(self.karte("Maut",1))
        rechts.addWidget(self.karte("Werkstatt",2))
        rechts.addWidget(self.karte("Sonstiges",3))
        rechts.addWidget(self.karte("Umsatz",4))
        rechts.addWidget(self.karte("KM",5))

        rechts.addStretch()

        haupt.addLayout(rechts,1)

    # -----------------------------------------

    def karte(self,name,index):

        frame = QFrame()

        frame.setFrameShape(QFrame.StyledPanel)

        frame.setStyleSheet("""
            QFrame{
                background:#2b2b2b;
                border-radius:12px;
            }
        """)

        layout = QVBoxLayout(frame)

        oben = QLabel(name)

        oben.setStyleSheet("font-weight:bold;")

        wert = QLabel("0")

        wert.setObjectName(f"kpi_{index}")

        wert.setAlignment(Qt.AlignCenter)

        wert.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(oben)
        layout.addWidget(wert)

        return frame

    # -----------------------------------------

    def berechne_summen(self):

        self.table.blockSignals(True)

        for spalte in range(1,7):

            gesamt = 0

            for zeile in range(6):

                item = self.table.item(zeile,spalte)

                if not item:
                    continue

                text = item.text().replace(",", ".")

                try:
                    gesamt += float(text)
                except:
                    pass

            sum_item = QTableWidgetItem(f"{gesamt:,.0f}".replace(",", "."))

            sum_item.setBackground(QColor(COLORS["orange"]))
            sum_item.setForeground(QColor("black"))

            self.table.setItem(6,spalte,sum_item)

            label = self.findChild(QLabel,f"kpi_{spalte-1}")

            if label:

                if spalte==6:
                    label.setText(f"{gesamt:,.0f} km".replace(",", "."))
                elif spalte==5:
                    label.setText(f"{gesamt:,.0f} €".replace(",", "."))
                else:
                    label.setText(f"{gesamt:,.0f} €".replace(",", "."))

        self.table.blockSignals(False)
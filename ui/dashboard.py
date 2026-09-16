from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QGridLayout, QFrame

from config import COLORS


class KPIBox(QFrame):

    def __init__(self, titel, wert):
        super().__init__()

        self.setStyleSheet(f"""
            QFrame{{
                background:white;
                border-radius:14px;
                border:1px solid #d8d8d8;
            }}
        """)

        layout = QVBoxLayout(self)

        t = QLabel(titel)
        t.setAlignment(Qt.AlignCenter)
        t.setStyleSheet("color:gray;font-size:12px;")

        w = QLabel(str(wert))
        w.setAlignment(Qt.AlignCenter)
        w.setStyleSheet(f"""
            color:{COLORS["blau"]};
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(t)
        layout.addWidget(w)


class Dashboard(QWidget):

    def __init__(self):
        super().__init__()

        outer = QVBoxLayout(self)
        outer.setContentsMargins(20, 20, 20, 20)
        outer.setSpacing(20)

        titel = QLabel("Dashboard")
        titel.setStyleSheet(f"""
            color:{COLORS["blau"]};
            font-size:28px;
            font-weight:bold;
        """)

        outer.addWidget(titel)

        grid = QGridLayout()

        grid.addWidget(KPIBox("Fahrzeuge", "--"), 0, 0)
        grid.addWidget(KPIBox("Trailer", "--"), 0, 1)
        grid.addWidget(KPIBox("Fahrer", "--"), 0, 2)
        grid.addWidget(KPIBox("Erlös", "-- €"), 0, 3)

        outer.addLayout(grid)

        bereich = QFrame()

        bereich.setStyleSheet("""
            QFrame{
                background:white;
                border-radius:14px;
                border:1px solid #d8d8d8;
            }
        """)

        inhalt = QVBoxLayout(bereich)

        txt = QLabel(
            "Hier erscheinen später:\n\n"
            "• Managementübersicht\n"
            "• Diagramme\n"
            "• Kostenentwicklung\n"
            "• Standortvergleich"
        )

        txt.setAlignment(Qt.AlignTop)

        txt.setStyleSheet("""
            font-size:15px;
            padding:10px;
        """)

        inhalt.addWidget(txt)

        outer.addWidget(bereich, 1)
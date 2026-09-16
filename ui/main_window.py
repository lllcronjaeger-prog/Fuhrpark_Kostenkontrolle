from PySide6.QtWidgets import QMainWindow,QWidget,QVBoxLayout,QHBoxLayout,QLabel,QComboBox,QTableWidget,QTableWidgetItem
from calendar import month_name
from config import APP_NAME,COLORS
from .app_state import app_state

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1400,850)
        root=QWidget();self.setCentralWidget(root)
        lay=QVBoxLayout(root)
        top=QHBoxLayout()
        title=QLabel("Fuhrpark-Kostenkontrolle")
        title.setStyleSheet(f"font-size:22px;font-weight:bold;color:{COLORS['blau']};")
        top.addWidget(title);top.addStretch()
        self.monat=QComboBox();self.monat.addItems(["Januar","Februar","März","April","Mai","Juni","Juli","August","September","Oktober","November","Dezember"]);self.monat.setCurrentIndex(app_state.monat-1)
        self.standort=QComboBox();self.standort.addItems(["Gesamt","Leipzig","Ettlingen"])
        top.addWidget(self.monat);top.addWidget(self.standort)
        lay.addLayout(top)
        self.table=QTableWidget(6,7)
        self.table.setHorizontalHeaderLabels(["Fahrzeug","Diesel","Maut","Werkstatt","Sonstiges","Umsatz","KM"])
        fahrzeuge=["KA-LL 8031","KA-LL 8032","KA-LL 8045","TS-ZM 1510","Zusatzfahrer","Zusatztrailer"]
        for r,f in enumerate(fahrzeuge):
            self.table.setItem(r,0,QTableWidgetItem(f))
        lay.addWidget(self.table)
        self.statusBar().showMessage(f"{month_name[app_state.monat]} {app_state.jahr} | {app_state.standort} | {app_state.monatsstatus}")

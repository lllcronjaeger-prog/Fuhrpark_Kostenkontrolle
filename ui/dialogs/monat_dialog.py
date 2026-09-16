from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QComboBox,
    QDialogButtonBox
)


class MonatDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Neuen Monat anlegen")

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Monat"))

        self.monat = QComboBox()

        self.monat.addItems([
            "Januar","Februar","März","April","Mai","Juni",
            "Juli","August","September","Oktober","November","Dezember"
        ])

        layout.addWidget(self.monat)

        layout.addWidget(QLabel("Jahr"))

        self.jahr = QComboBox()

        for j in range(2025,2036):
            self.jahr.addItem(str(j))

        layout.addWidget(self.jahr)

        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok |
            QDialogButtonBox.Cancel
        )

        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout.addWidget(buttons)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel


class LyricLabel(QLabel):

    def __init__(self, size=15, bold=False, parent=None):
        super().__init__(parent)

        self.size = size
        self.bold = bold
        self.text_value = ""

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(
            "background: transparent; color: white;"
        )
        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        font = self.font()
        font.setFamily("Lexend")
        font.setPointSize(self.size)
        font.setBold(self.bold)
        self.setFont(font)

    def fitText(self, text):
        self.text_value = text or ""
        self.setText(self.text_value)
        self.update()

from PySide6.QtCore import Qt
from PySide6.QtGui import QFontMetrics, QPainter
from PySide6.QtWidgets import QLabel


class LyricLabel(QLabel):

    def __init__(self, size=15, bold=False, parent=None):
        super().__init__(parent)

        self.size = size
        self.bold = bold
        self.text_value = ""

        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("background: transparent;")
        self.setAttribute(Qt.WA_TranslucentBackground)

    def fitText(self, text):

        self.text_value = text or ""

        font = self.font()
        font.setFamily("Lexend")
        font.setPointSize(self.size)
        font.setBold(self.bold)

        self.setFont(font)
        self.setText(self.text_value)

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )

        painter.setRenderHint(
            QPainter.TextAntialiasing
        )

        font = self.font()
        font.setFamily("Lexend")
        font.setPointSize(self.size)
        font.setBold(self.bold)

        painter.setFont(font)
        painter.setPen(Qt.white)

        metrics = QFontMetrics(font)

        text = self.text_value or ""

        width = metrics.horizontalAdvance(text)

        x = max(
            0,
            int((self.width() - width) / 2)
        )

        y = int(
            (
                self.height()
                + metrics.ascent()
                - metrics.descent()
            ) / 2
        )

        painter.drawText(
            x,
            y,
            text
        )


from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtWidgets import QWidget


class CurrentWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.text = ""
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setMinimumHeight(35)

    def setLyrics(self, text):
        self.text = text or ""
        self.update()

    def setKaraoke(self, text, words, time_ms):
        self.setLyrics(text)

    def paintEvent(self, event):
        painter = QPainter(self)

        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        if not self.text:
            return

        font = self.font()
        font.setFamily("Lexend")
        font.setPointSize(15)
        font.setBold(True)

        painter.setFont(font)
        painter.setPen(Qt.white)

        metrics = QFontMetrics(font)
        width = metrics.horizontalAdvance(self.text)

        x = max(0, int((self.width() - width) / 2))
        y = int(
            (self.height()
             + metrics.ascent()
             - metrics.descent()) / 2
        )

        painter.drawText(x, y, self.text)

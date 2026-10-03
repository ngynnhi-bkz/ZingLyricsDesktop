from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPainterPath, QPen, QFontMetrics
from PySide6.QtWidgets import QLabel


class OutlineLabel(QLabel):

    def __init__(self, text=""):
        super().__init__(text)

        self.outlineColor = QColor(0, 0, 0)
        self.textColor = QColor(255, 255, 255)
        self.outlineWidth = 3

        self.setAlignment(Qt.AlignCenter)

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        fm = QFontMetrics(self.font())

        text = self.text()

        rect = self.rect()

        x = (rect.width() - fm.horizontalAdvance(text)) / 2
        y = (rect.height() + fm.ascent() - fm.descent()) / 2

        path = QPainterPath()
        path.addText(x, y, self.font(), text)

        pen = QPen(self.outlineColor, self.outlineWidth)
        pen.setJoinStyle(Qt.RoundJoin)

        painter.setPen(pen)
        painter.drawPath(path)

        painter.fillPath(path, self.textColor)
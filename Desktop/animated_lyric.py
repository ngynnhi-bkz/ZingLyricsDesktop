from PySide6.QtWidgets import QWidget
from lyriclabel import LyricLabel


class AnimatedLyric(QWidget):

    def __init__(self, size=15, bold=False, duration=0, offset=0, opacity=0.43):
        super().__init__()

        self.label = LyricLabel(size=size, bold=bold)
        self.label.setParent(self)
        self.label.setGeometry(0, 0, self.width(), self.height())

    def setLyrics(self, text):
        self.label.fitText(text or "")
        self.update()

    def resizeEvent(self, event):
        self.label.setGeometry(0, 0, self.width(), self.height())
        super().resizeEvent(event)

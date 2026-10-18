
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget

from animated_lyric import AnimatedLyric
from current_widget import CurrentWidget


class LyricsWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowFlags(
            Qt.FramelessWindowHint
            | Qt.Tool
            | Qt.WindowTransparentForInput
        )

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.resize(580, 95)
        self.move(-50, 450)

        self.content = QWidget(self)
        self.content.setGeometry(10, 5, 560, 85)
        self.content.setAttribute(
            Qt.WA_TranslucentBackground
        )

        self.prev = AnimatedLyric(
            size=10,
            bold=False,
            duration=420,
            offset=4,
            opacity=0.43,
        )

        self.current = CurrentWidget()

        self.next = AnimatedLyric(
            size=10,
            bold=False,
            duration=420,
            offset=4,
            opacity=0.43,
        )

        self.prev.setParent(self.content)
        self.current.setParent(self.content)
        self.next.setParent(self.content)

        self.prev.setGeometry(0, 0, 560, 25)
        self.current.setGeometry(0, 25, 560, 35)
        self.next.setGeometry(0, 60, 560, 25)

        self.currentData = None
        self.dragPos = None

    def updateLyrics(self, data):
        prev = data.get("prev", "") or ""
        current = data.get("current", "") or ""
        next_line = data.get("next", "") or ""

        if not current:
            return

        self.prev.setLyrics(prev)
        self.current.setLyrics(current)
        self.next.setLyrics(next_line)

        self.currentData = {
            "prev": prev,
            "current": current,
            "next": next_line,
        }

    def showUpdating(self):
        self.prev.setLyrics("")
        self.current.setLyrics("")
        self.next.setLyrics("")

        self.currentData = None

    def showInstrumental(self):
        self.prev.setLyrics("")
        self.current.setLyrics("⋆ ⋆ ⋆")
        self.next.setLyrics("")

        self.currentData = {
            "prev": "",
            "current": "⋆ ⋆ ⋆",
            "next": "",
        }

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):
        if (
            self.dragPos is not None
            and event.buttons() & Qt.LeftButton
        ):
            self.move(
                event.globalPosition().toPoint()
                - self.dragPos
            )

    def mouseReleaseEvent(self, event):
        self.dragPos = None

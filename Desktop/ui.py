from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout

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

        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(0)

        self.prev = AnimatedLyric(
            size=10,
            bold=False
        )
        self.prev.setFixedHeight(25)

        self.current = CurrentWidget()
        self.current.setFixedHeight(35)

        self.next = AnimatedLyric(
            size=10,
            bold=False
        )
        self.next.setFixedHeight(25)

        layout.addWidget(self.prev)
        layout.addWidget(self.current)
        layout.addWidget(self.next)

        self.currentData = None
        self.dragPos = None

    def updateLyrics(self, data):

        current = data.get("current", "") or ""

        if not current:
            return

        self.prev.setLyrics(
            data.get("prev", "") or ""
        )

        self.current.setLyrics(
            current
        )

        self.next.setLyrics(
            data.get("next", "") or ""
        )

        self.currentData = {
            "prev": data.get("prev", "") or "",
            "current": current,
            "next": data.get("next", "") or ""
        }

    def showUpdating(self):

        self.prev.setLyrics("")
        self.current.setLyrics(
            "Lời bài hát đang được cập nhật"
        )
        self.next.setLyrics("")

    def showInstrumental(self):

        self.prev.setLyrics("")
        self.current.setLyrics("⋆ ⋆ ⋆")
        self.next.setLyrics("")

    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.dragPos = (
                event.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(self, event):

        if self.dragPos:
            self.move(
                event.globalPosition().toPoint()
                - self.dragPos
            )

    def mouseReleaseEvent(self, event):

        self.dragPos = None

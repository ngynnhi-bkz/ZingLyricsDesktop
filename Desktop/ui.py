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

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(580, 95)
        self.move(-50, 450)

        # Chỉ 1 lớp, không animation
        self.content = QWidget(self)
        self.content.setGeometry(10, 5, 560, 85)
        self.content.setAttribute(Qt.WA_TranslucentBackground)

        self.prev = AnimatedLyric(size=10, bold=False)
        self.current = CurrentWidget()
        self.next = AnimatedLyric(size=10, bold=False)

        self.prev.setParent(self.content)
        self.current.setParent(self.content)
        self.next.setParent(self.content)

        self.prev.setGeometry(0, 0, 560, 25)
        self.current.setGeometry(0, 25, 560, 35)
        self.next.setGeometry(0, 60, 560, 25)

        self.currentData = None
        self.dragPos = None

    def updateLyrics(self, data):
        current = data.get("current", "") or ""

        if not current:
            return

        self.prev.setLyrics(data.get("prev", "") or "")
        self.current.setLyrics(current)
        self.next.setLyrics(data.get("next", "") or "")

        self.currentData = {
            "prev": data.get("prev", "") or "",
            "current": current,
            "next": data.get("next", "") or ""
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
            "next": ""
        }

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

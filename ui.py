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

        self.resize(
            580,
            95
        )

        self.move(
            -50,
            450
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            10,
            5,
            10,
            5
        )

        layout.setSpacing(0)

        layout.setAlignment(
            Qt.AlignTop
        )

        # ==================================================
        # PREVIOUS
        # ==================================================

        self.prev = AnimatedLyric(
            size=10,
            bold=False,
            duration=260,
            offset=5,
            opacity=0.43
        )

        self.prev.setFixedHeight(25)

        # ==================================================
        # CURRENT
        # ==================================================

        self.current = CurrentWidget()

        self.current.setFixedHeight(35)

        # ==================================================
        # NEXT
        # ==================================================

        self.next = AnimatedLyric(
            size=10,
            bold=False,
            duration=260,
            offset=5,
            opacity=0.43
        )

        self.next.setFixedHeight(25)

        layout.addWidget(
            self.prev
        )

        layout.addWidget(
            self.current
        )

        layout.addWidget(
            self.next
        )

        # ==================================================
        # CACHE
        # ==================================================

        self.lastPrev = ""

        self.lastCurrent = ""

        self.lastNext = ""

        self.dragPos = None

    # ======================================================
    # UPDATE LYRICS
    # ======================================================

    def updateLyrics(
        self,
        data
    ):

        prev = (
            data.get(
                "prev",
                ""
            )
            or ""
        )

        current = (
            data.get(
                "current",
                ""
            )
            or ""
        )

        nextLyric = (
            data.get(
                "next",
                ""
            )
            or ""
        )

        if not current:
            return

        # ==================================================
        # TÍNH TEXT HIỂN THỊ
        # ==================================================

        if prev:

            displayPrev = (
                '"'
                + prev
            )

        else:

            displayPrev = ""

        if nextLyric:

            displayNext = (
                nextLyric
                + '"'
            )

        else:

            displayNext = ""

        # ==================================================
        # QUAN TRỌNG:
        #
        # Chỉ thay widget nếu text THỰC SỰ thay đổi.
        #
        # Không set ""
        # rồi set lại text.
        #
        # Đây là phần loại bỏ nháy dòng 1 / dòng 3.
        # ==================================================

        if (
            displayPrev
            != self.lastPrev
        ):

            self.prev.setLyrics(
                displayPrev
            )

            self.lastPrev = (
                displayPrev
            )

        if (
            current
            != self.lastCurrent
        ):

            self.current.setLyrics(
                current
            )

            self.lastCurrent = (
                current
            )

        if (
            displayNext
            != self.lastNext
        ):

            self.next.setLyrics(
                displayNext
            )

            self.lastNext = (
                displayNext
            )

    # ======================================================
    # DRAG
    # ======================================================

    def mousePressEvent(
        self,
        e
    ):

        if (
            e.button()
            == Qt.LeftButton
        ):

            self.dragPos = (
                e.globalPosition().toPoint()
                - self.frameGeometry().topLeft()
            )

    def mouseMoveEvent(
        self,
        e
    ):

        if self.dragPos:

            self.move(
                e.globalPosition().toPoint()
                - self.dragPos
            )

    def mouseReleaseEvent(
        self,
        e
    ):

        self.dragPos = None

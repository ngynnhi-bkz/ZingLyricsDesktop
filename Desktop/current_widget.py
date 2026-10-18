
from PySide6.QtCore import (
    Qt,
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve,
    QPoint,
)
from PySide6.QtGui import QPainter, QFontMetrics
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsOpacityEffect,
)


class CurrentWidget(QWidget):

    def __init__(self):
        super().__init__()

        self.text = ""
        self.base_pos = None
        self.animation_group = None

        self.setAttribute(
            Qt.WA_TranslucentBackground
        )
        self.setMinimumHeight(35)

        self.effect = QGraphicsOpacityEffect(self)
        self.effect.setOpacity(0.0)
        self.setGraphicsEffect(self.effect)

    def setLyrics(self, text):
        text = text or ""

        if text == self.text:
            return

        self.text = text

        if self.animation_group:
            self.animation_group.stop()
            self.animation_group = None

        if self.base_pos is not None:
            self.move(self.base_pos)

        if not text:
            self.effect.setOpacity(0.0)
            self.update()
            return

        self.base_pos = self.pos()

        start_pos = self.base_pos + QPoint(0, 5)

        self.move(start_pos)
        self.effect.setOpacity(0.0)
        self.update()

        group = QParallelAnimationGroup(self)

        fade = QPropertyAnimation(
            self.effect, b"opacity"
        )
        fade.setDuration(420)
        fade.setStartValue(0.0)
        fade.setEndValue(1.0)
        fade.setEasingCurve(
            QEasingCurve.OutCubic
        )

        slide = QPropertyAnimation(
            self, b"pos"
        )
        slide.setDuration(420)
        slide.setStartValue(start_pos)
        slide.setEndValue(self.base_pos)
        slide.setEasingCurve(
            QEasingCurve.OutCubic
        )

        group.addAnimation(fade)
        group.addAnimation(slide)

        self.animation_group = group
        group.start()

    def setKaraoke(self, text, words, time_ms):
        self.setLyrics(text)

    def paintEvent(self, event):
        if not self.text:
            return

        painter = QPainter(self)

        painter.setRenderHint(
            QPainter.Antialiasing
        )
        painter.setRenderHint(
            QPainter.TextAntialiasing
        )

        font = self.font()
        font.setFamily("Lexend")
        font.setPointSize(15)
        font.setBold(True)

        painter.setFont(font)
        painter.setPen(Qt.white)

        metrics = QFontMetrics(font)
        width = metrics.horizontalAdvance(self.text)

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

        painter.drawText(x, y, self.text)


from PySide6.QtCore import (
    QPropertyAnimation,
    QParallelAnimationGroup,
    QEasingCurve,
    QPoint,
)
from PySide6.QtWidgets import (
    QWidget,
    QGraphicsOpacityEffect,
)

from lyriclabel import LyricLabel


class AnimatedLyric(QWidget):

    def __init__(
        self,
        size=15,
        bold=False,
        duration=380,
        offset=5,
        opacity=0.43,
    ):
        super().__init__()

        self.duration = duration
        self.offset = offset
        self.target_opacity = opacity

        self.text_value = ""
        self.base_pos = None
        self.animation_group = None

        self.label = LyricLabel(
            size=size,
            bold=bold,
            parent=self,
        )

        self.label.setGeometry(
            0, 0, self.width(), self.height()
        )

        self.effect = QGraphicsOpacityEffect(self)
        self.effect.setOpacity(0.0)
        self.setGraphicsEffect(self.effect)

    def setLyrics(self, text):
        text = text or ""

        # Không chạy lại animation trong mỗi lần polling.
        if text == self.text_value:
            return

        self.text_value = text

        if self.animation_group:
            self.animation_group.stop()
            self.animation_group = None

        if self.base_pos is not None:
            self.move(self.base_pos)

        if not text:
            self.label.fitText("")
            self.effect.setOpacity(0.0)
            return

        self.label.fitText(text)

        # Lưu vị trí gốc của dòng.
        self.base_pos = self.pos()

        start_pos = self.base_pos + QPoint(
            0, self.offset
        )

        self.move(start_pos)
        self.effect.setOpacity(0.0)

        group = QParallelAnimationGroup(self)

        fade = QPropertyAnimation(
            self.effect, b"opacity"
        )
        fade.setDuration(self.duration)
        fade.setStartValue(0.0)
        fade.setEndValue(self.target_opacity)
        fade.setEasingCurve(
            QEasingCurve.OutCubic
        )

        slide = QPropertyAnimation(
            self, b"pos"
        )
        slide.setDuration(self.duration)
        slide.setStartValue(start_pos)
        slide.setEndValue(self.base_pos)
        slide.setEasingCurve(
            QEasingCurve.OutCubic
        )

        group.addAnimation(fade)
        group.addAnimation(slide)

        self.animation_group = group
        group.start()

    def resizeEvent(self, event):
        self.label.setGeometry(
            0, 0, self.width(), self.height()
        )
        super().resizeEvent(event)

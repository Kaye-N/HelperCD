import sys

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette

class ClockWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Clock')
        self.setGeometry(100, 100, 400, 200)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.time_label = QLabel()
        self.time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.time_label.setFont(QFont('Arial', 48))
        self.layout.addWidget(self.time_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)  # update every second

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime()
        self.time_label.setText(current_time.toString('hh:mm:ss'))
class BouncingLetter(QLabel):
    def __init__(self, letter, parent=None):
        super().__init__(letter, parent)
        self.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.setStyleSheet("color: hotpink;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(600)
        self.anim.setEasingCurve(QEasingCurve.Type.OutBounce)

    def bounce(self, delay, y_offset=30):
        rect = self.geometry()
        start_rect = QRect(rect.x(), rect.y(), rect.width(), rect.height())
        end_rect = QRect(rect.x(), rect.y() - y_offset, rect.width(), rect.height())
        self.anim.setStartValue(start_rect)
        self.anim.setEndValue(end_rect)
        self.anim.setLoopCount(2)
        QTimer.singleShot(delay, self.anim.start)

class PinkClock(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Hallo! Good Day!')
        self.setGeometry(100, 100, 600, 300)
        self.setMinimumSize(400, 200)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffe6f0"))  # light pink
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Scrolling banner setup
        self.banner_text = "   Good Morning  Good Afternoon  Good Night   "
        self.scroll_index = 0

        self.banner_label = QLabel()
        self.banner_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.banner_label.setStyleSheet("color: hotpink;")
        self.banner_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.banner_label)

        # Clock label with bounce animation
        self.clock_label = QLabel()
        self.clock_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.clock_label.setFont(QFont('Arial', 48, QFont.Weight.Bold))
        self.clock_label.setStyleSheet("color: deeppink;")
        layout.addWidget(self.clock_label)

        self.setLayout(layout)

        # Timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)

        self.scroll_timer = QTimer(self)
        self.scroll_timer.timeout.connect(self.scroll_banner)
        self.scroll_timer.start(30)  # Faster for smoother scroll

        self.bounce_anim = QPropertyAnimation(self.clock_label, b"geometry")
        self.bounce_anim.setDuration(400)
        self.bounce_anim.setEasingCurve(QEasingCurve.Type.OutBounce)

        self.bounce_timer = QTimer(self)
        self.bounce_timer.timeout.connect(self.animate_bounce)
        self.bounce_timer.start(2000)

        self.update_time()
        self.scroll_banner()

    def resizeEvent(self, event):
        self.banner_label.setMinimumWidth(self.width())
        super().resizeEvent(event)

    def update_time(self):
        current_time = QTime.currentTime()
        self.clock_label.setText(current_time.toString('hh:mm:ss'))

    def scroll_banner(self):
        # Calculate padding so text starts off-screen left
        chars_visible = max(1, self.banner_label.width() // 16)  # ~16px per char
        padded_text = " " * chars_visible + self.banner_text + " " * chars_visible
        self.scroll_index = (self.scroll_index + 1) % len(padded_text)
        display_text = padded_text[self.scroll_index:self.scroll_index + chars_visible]
        self.banner_label.setText(display_text)

    def animate_bounce(self):
        rect = self.clock_label.geometry()
        start_rect = QRect(rect.x(), rect.y(), rect.width(), rect.height())
        end_rect = QRect(rect.x(), rect.y() - 30, rect.width(), rect.height())
        self.bounce_anim.stop()
        self.bounce_anim.setStartValue(start_rect)
        self.bounce_anim.setEndValue(end_rect)
        self.bounce_anim.start()
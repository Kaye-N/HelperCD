from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer, QTime, QPropertyAnimation, QRect, QEasingCurve
from PyQt6.QtGui import QFont, QColor, QPalette

class BouncingLetter(QLabel):
    def __init__(self, letter, parent=None):
        super().__init__(letter, parent)
        self.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        self.setStyleSheet("color: hotpink;")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(600)
        self.anim.setEasingCurve(QEasingCurve.Type.OutBounce)

    def bounce(self, delay, y_offset=20):
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
        self.setWindowTitle('Pink Aesthetic Clock')
        self.setGeometry(100, 100, 600, 300)

        self.setAutoFillBackground(True)
        palette = QPalette()
        palette.setColor(QPalette.ColorRole.Window, QColor("#ffe6f0"))  # light pink
        self.setPalette(palette)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Banner text
        banner_text = "Good Morning Good Afternoon Good Night"
        self.banner_layout = QHBoxLayout()
        self.letters = []

        for i, char in enumerate(banner_text):
            letter = BouncingLetter(char)
            self.banner_layout.addWidget(letter)
            self.letters.append(letter)

        layout.addLayout(self.banner_layout)

        # Clock label
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

        self.bounce_timer = QTimer(self)
        self.bounce_timer.timeout.connect(self.animate_banner)
        self.bounce_timer.start(2000)

        self.update_time()

    def update_time(self):
        current_time = QTime.currentTime()
        self.clock_label.setText(current_time.toString('hh:mm:ss'))

    def animate_banner(self):
        for i, letter in enumerate(self.letters):
            letter.bounce(i * 100)


import sys
import subprocess

from PyQt6.QtCore import Qt, QSize, QPoint
from PyQt6.QtGui import QFont, QIcon, QPainter, QPixmap
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFrame
)

class ArrowButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: #e9a6b3;
            }
            QPushButton:hover {
                background-color: #f2b6c6;
            }
        """)
        self.setIcon(self.create_arrow_icon())
        self.setIconSize(QSize(24, 24))

    def create_arrow_icon(self):
        pixmap = QPixmap(24, 24)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.GlobalColor.white)
        painter.setBrush(Qt.GlobalColor.white)
        points = [
            QPoint(6, 4), QPoint(18, 12), QPoint(6, 20)
        ]
        painter.drawPolygon(*points)
        painter.end()
        return QIcon(pixmap)

class ScrapePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Begin Scraping")
        self.setStyleSheet("background-color: #f2b6c6;")
        self.url = ""

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center everything

        title = QLabel("Begin Scraping")
        title_font = QFont("Comic Sans MS", 32, QFont.Weight.Bold)
        title.setFont(title_font)
        title.setStyleSheet("color: #d16e8d; margin-top: 40px; margin-bottom: 30px;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title)

        # Create a frame to act as the input box container
        input_frame = QFrame()
        input_frame.setStyleSheet("""
            QFrame {
                background: #fff0f5;
                border: 2px solid #e9a6b3;
                border-radius: 16px;
                padding: 24px;
            }
        """)
        input_frame.setFixedWidth(400)

        input_layout = QHBoxLayout()
        input_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("Enter URL...")
        self.input_box.setFixedWidth(250)
        self.input_box.setStyleSheet("""
            QLineEdit {
                border: 1px solid #e9a6b3;
                border-radius: 10px;
                padding: 8px;
                font-size: 18px;
                background: #fff;
                color: #d16e8d;
            }
        """)

        arrow_btn = ArrowButton()
        arrow_btn.clicked.connect(self.run_script)

        input_layout.addWidget(self.input_box)
        input_layout.addWidget(arrow_btn)

        input_frame.setLayout(input_layout)
        main_layout.addWidget(input_frame, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setLayout(main_layout)
        self.setFixedSize(500, 300)

    def run_script(self):
        self.url = self.input_box.text()
        subprocess.Popen([sys.executable, "script.py", self.url])
        try:
            result = subprocess.run(["python", "script.py"], capture_output=True, text=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}")
            print(f"Error output: {e.stderr}")


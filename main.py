#scripts 
import clock

import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel, QGraphicsDropShadowEffect
)
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QLinearGradient, QBrush
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helper")
        self.setGeometry(100, 100, 800, 600)
        self.setAutoFillBackground(True)

        #font 
        font = QFont('Archivo', 13)
        bold_font = QFont('Archivo', 13, QFont.Weight.Bold)

        #background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#342A47"))  
        gradient.setColorAt(1.0, QColor("#5D4E8C"))  
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # Central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        main_layout.addStretch()

        # Image label
        label = QLabel()
        image = QPixmap('Circleicon.png')
        label.setPixmap(image)
        label.setScaledContents(True)
        label.setFixedSize(150, 150)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        #buttons and designs
        button_names = ["To do", "Clock", "Webscrape", "Exit"]
        buttons = [QPushButton(name) for name in button_names]


        #clock window instance
        self.clock_window = None

        for button in buttons:
            button.setFont(bold_font)
            button.setMinimumHeight(50)
            button.setStyleSheet(
                """QPushButton {
                    background-color: #6C63FF;
                    color: white;
                    border-radius: 15px;
                    padding: 10px 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #857DFF;
                }
            """)

            #button shadow
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15)
            shadow.setOffset(3, 3)
            shadow.setColor(QColor(0, 0, 0, 160))  # Semi-transparent black
            button.setGraphicsEffect(shadow)

                #button actions
        if button.text() == "To do":
            button.clicked.connect(lambda: print("To do clicked")) #placeholder
        elif button.text() == "Clock":
            button.clicked.connect(self.open_clock)
        elif button.text() == "Exit":
            button.clicked.connect(self.close)

        def open_clock(self):
            if self.clock_window is None:
                self.clock_window = clock.PinkClock()
                self.clock_window.show()
                self.clock_window.raise_()
                self.clock_window.activateWindow()

        #layout image+buttons
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        content_layout.setSpacing(20)
        content_layout.addWidget(label, alignment=Qt.AlignmentFlag.AlignCenter)

        for button in buttons:
            content_layout.addWidget(button, alignment=Qt.AlignmentFlag.AlignCenter)

        center_container = QWidget()
        center_container.setLayout(content_layout)
        main_layout.addWidget(center_container, alignment=Qt.AlignmentFlag.AlignHCenter)

        main_layout.addStretch()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()

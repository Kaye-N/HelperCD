#scripts 
import clock
import webscrape as scrape

import sys
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton,
    QVBoxLayout, QLabel, QGraphicsDropShadowEffect, QSizePolicy,
    QHBoxLayout, QFrame
)
from PyQt6.QtGui import QPalette, QColor, QFont, QPixmap, QLinearGradient, QBrush
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helper")
        # reverted window size per request
        self.setGeometry(100, 100, 900, 600)
        self.setAutoFillBackground(True)

        # background: dark vertical gradient (keeps same purple palette)
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0.0, QColor("#2f2540"))   # darker top
        gradient.setColorAt(1.0, QColor("#5D4E8C"))   # existing bottom color
        palette = QPalette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(gradient))
        self.setPalette(palette)

        # fonts
        title_font = QFont('Archivo', 26, QFont.Weight.Bold)
        subtitle_font = QFont('Archivo', 12)
        btn_font = QFont('Archivo', 13, QFont.Weight.DemiBold)

        # central widget & layout
        central = QWidget()
        self.setCentralWidget(central)
        outer_layout = QVBoxLayout(central)
        outer_layout.setContentsMargins(28, 28, 28, 28)
        outer_layout.setSpacing(28)
        outer_layout.addStretch()

        # card frame (rounded panel)
        card = QFrame()
        card.setObjectName("card")
        # keep card width reasonable for 900x600 window
        card.setMinimumWidth(620)
        card.setMaximumWidth(860)
        card_layout = QVBoxLayout(card)
        # more generous internal padding and spacing
        card_layout.setContentsMargins(40, 32, 40, 32)
        card_layout.setSpacing(20)

        # header: icon + title
        header = QWidget()
        header_l = QHBoxLayout(header)
        header_l.setContentsMargins(0, 0, 0, 0)
        header_l.setSpacing(12)

        icon = QLabel()
        pix = QPixmap('Circleicon.png')
        if not pix.isNull():
            pix = pix.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            icon.setPixmap(pix)
        icon.setFixedSize(64, 64)

        title = QLabel("Helper")
        title.setFont(title_font)
        title.setStyleSheet("color: #EFE9FF;")  # light text

        subtitle = QLabel("Productivity tools — clock, scraping and more")
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #D8CFEF;")

        text_block = QWidget()
        text_l = QVBoxLayout(text_block)
        text_l.setContentsMargins(0, 0, 0, 0)
        text_l.addWidget(title)
        text_l.addWidget(subtitle)

        header_l.addWidget(icon, alignment=Qt.AlignmentFlag.AlignLeft)
        header_l.addWidget(text_block, alignment=Qt.AlignmentFlag.AlignVCenter)
        header_l.addStretch()

        card_layout.addWidget(header)

        # divider
        divider = QFrame()
        divider.setFixedHeight(1)
        divider.setStyleSheet("background: rgba(255,255,255,0.06); border: none;")
        card_layout.addWidget(divider)

        # NAV CARD: larger rounded box that holds all buttons/navigation
        nav_card = QFrame()
        nav_card.setObjectName("navcard")
        nav_card.setMinimumHeight(140)
        nav_card.setMaximumHeight(220)
        nav_layout = QHBoxLayout(nav_card)
        # larger padding and spacing for a roomy look
        nav_layout.setContentsMargins(20, 18, 20, 18)
        nav_layout.setSpacing(20)

        # create buttons (inside nav_card)
        button_names = ["To do", "Clock", "Webscrape", "Exit"]
        self.buttons = []
        for name in button_names:
            b = HoverButton(name)
            b.setFont(btn_font)
            # a bit wider/taller buttons inside the nav box
            b.setFixedHeight(60)
            b.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

            # improved button style: softer gradient, subtle inner gloss, clearer border
            b.setStyleSheet("""
                QPushButton {
                    color: #FFFFFF;
                    border-radius: 14px;
                    padding: 10px 22px;
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(117,107,255,230), stop:0.5 rgba(102,93,245,230), stop:1 rgba(84,76,224,220));
                    border: 1px solid rgba(255,255,255,20);
                }
                QPushButton:hover {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(148,140,255,255), stop:0.5 rgba(132,125,255,255), stop:1 rgba(106,99,239,255));
                    border: 1px solid rgba(255,255,255,28);
                }
                QPushButton:pressed {
                    background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                        stop:0 rgba(84,76,224,255), stop:1 rgba(72,64,200,255));
                    padding-top: 12px;
                }
                QPushButton:focus {
                    outline: none;
                    border: 1px solid rgba(255,255,255,40);
                }
            """)

            # removed button shadows (no QGraphicsDropShadowEffect applied)
            # b.setGraphicsEffect(...) intentionally omitted

            self.buttons.append(b)
            nav_layout.addWidget(b)

        # add nav_card into main card layout
        card_layout.addWidget(nav_card)

        # footer / helper text
        footer = QLabel("Stressed to the Max")
        footer.setStyleSheet("color: #CFC8F2;")
        footer.setFont(subtitle_font)
        card_layout.addWidget(footer, alignment=Qt.AlignmentFlag.AlignLeft)

        # card drop shadow
        card_shadow = QGraphicsDropShadowEffect()
        card_shadow.setBlurRadius(40)
        card_shadow.setOffset(0, 12)
        card_shadow.setColor(QColor(0, 0, 0, 180))
        card.setGraphicsEffect(card_shadow)

        # small drop shadow for nav card
        # reduced nav card shadow: smaller blur, smaller offset, lower opacity
        nav_shadow = QGraphicsDropShadowEffect()
        nav_shadow.setBlurRadius(10)
        nav_shadow.setOffset(0, 4)
        nav_shadow.setColor(QColor(0, 0, 0, 60))
        nav_card.setGraphicsEffect(nav_shadow)

        outer_layout.addWidget(card, alignment=Qt.AlignmentFlag.AlignHCenter)
        outer_layout.addStretch()

        # window-level stylesheet for card and navcard
        self.setStyleSheet("""
            QFrame#card {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(63,52,86,230), stop:1 rgba(57,46,78,210));
                border-radius: 18px;
            }
            QFrame#navcard {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba(86,74,122,230), stop:1 rgba(76,64,110,210));
                border-radius: 14px;
                border: 1px solid rgba(255,255,255,10);
            }
        """)

        # store window refs
        self.clock_window = None
        self.scrape_window = None

        # connect buttons
        for b in self.buttons:
            if b.text() == "To do":
                b.clicked.connect(lambda _, x=b.text(): print(f"{x} clicked"))
            elif b.text() == "Clock":
                b.clicked.connect(self.open_clock)
            elif b.text() == "Webscrape":
                b.clicked.connect(self.open_webscrape)
            elif b.text() == "Exit":
                b.clicked.connect(self.close)

    def open_clock(self):
        if self.clock_window is None:
            self.clock_window = clock.PinkClock()
        self.clock_window.show()
        self.clock_window.raise_()
        self.clock_window.activateWindow()

    def open_webscrape(self):
        if self.scrape_window is None:
            self.scrape_window = scrape.ScrapePage()
        self.scrape_window.show()
        self.scrape_window.raise_()
        self.scrape_window.activateWindow()

# Add this HoverButton class (place after imports, before MainWindow)
class HoverButton(QPushButton):
    def __init__(self, *args, lift_px: int = 8, anim_ms: int = 160, **kwargs):
        super().__init__(*args, **kwargs)
        self._lift_px = lift_px
        self._anim = QPropertyAnimation(self, b"geometry")
        self._anim.setDuration(anim_ms)
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        # track current effect so we don't reference a deleted C++ object
        self._current_effect = None

    def enterEvent(self, event):
        # animate up
        start = self.geometry()
        end = start.translated(0, -self._lift_px)
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

        # ensure previous effect cleared (if any)
        if self._current_effect is not None:
            try:
                self.setGraphicsEffect(None)
            except Exception:
                pass
            self._current_effect = None

        # create a fresh, parented effect for this widget (safe from C++ deletion)
        eff = QGraphicsDropShadowEffect(self)
        eff.setBlurRadius(18)
        eff.setOffset(0, 6)
        eff.setColor(QColor(6, 4, 20, 120))
        self.setGraphicsEffect(eff)
        self._current_effect = eff

        super().enterEvent(event)

    def leaveEvent(self, event):
        # animate back down
        start = self.geometry()
        end = start.translated(0, self._lift_px)
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)

        # safely disconnect previous finished handlers
        try:
            self._anim.finished.disconnect()
        except Exception:
            pass

        def _clear_shadow():
            try:
                self.setGraphicsEffect(None)
            except Exception:
                pass
            self._current_effect = None
            try:
                self._anim.finished.disconnect(_clear_shadow)
            except Exception:
                pass

        self._anim.finished.connect(_clear_shadow)
        self._anim.start()
        super().leaveEvent(event)

if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
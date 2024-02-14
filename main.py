import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        splitter = QSplitter(self)

        # Code pane setup
        code_execute_button = QPushButton("Execute")
        code_execute_button.released.connect(self.code_execute)

        code_pane_buttons = QWidget()
        code_pane_buttons_layout = QHBoxLayout(code_pane_buttons)
        code_pane_buttons_layout.addWidget(code_execute_button)
        code_pane_buttons_layout.addWidget(QPushButton("Step"))

        self.code_edit = QPlainTextEdit()
        code_font = QFont("Monospace", 12)
        self.code_edit.setFont(code_font)
        self.code_edit.setTabStopDistance(40)

        code_pane = QWidget()
        code_pane_layout = QVBoxLayout(code_pane)
        code_pane_layout.addWidget(self.code_edit)
        code_pane_layout.addWidget(code_pane_buttons)

        # Add three panes to main splitter
        splitter.addWidget(code_pane)       # Left
        splitter.addWidget(Color('green'))  # Middle
        splitter.addWidget(Color('blue'))   # Right

        # Strech factors for three panes
        splitter.setStretchFactor(0, 1)     # Left
        splitter.setStretchFactor(1, 1)     # Middle
        splitter.setStretchFactor(2, 1)     # Right

        splitter.setSizes([200, 200, 100])

        self.setCentralWidget(splitter)

        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("CodeViz")

    def code_execute(self):
        usercode = self.code_edit.toPlainText()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()


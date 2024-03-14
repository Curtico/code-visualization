import sys
import trace

from PyQt6 import QtGui
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Color(QWidget):
    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor(color))
        self.setPalette(palette)


class MyGraphicsView(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setMouseTracking(True)
        self.last_mouse_pos = None
        self.setInteractive(True)
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.scene.setSceneRect(-10000, -10000, 20000, 20000)

    def draw_square(self, x, y, width, height):
        self.scene.addRect(x, y, width, height)

    def draw_array(self, y, width, height, items, distance):
        for i in range(items):
            x = i * (width + distance)
            self.scene.addRect(x, y, width, height)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QtGui.QIcon('CV.png'))

        code_execute_button = QPushButton("Execute")

        code_pane_buttons = QWidget()
        code_pane_buttons_layout = QHBoxLayout(code_pane_buttons)
        code_pane_buttons_layout.addWidget(code_execute_button)
        code_execute_button.released.connect(self.code_execute)
        code_pane_buttons_layout.addWidget(QPushButton("Step"))

        self.code_edit = QPlainTextEdit()
        code_font = QFont("Monospace", 12)
        self.code_edit.setFont(code_font)
        self.code_edit.setTabStopDistance(40)

        code_pane = QWidget()
        code_pane_layout = QVBoxLayout(code_pane)
        code_pane_layout.addWidget(self.code_edit)
        code_pane_layout.addWidget(code_pane_buttons)

        self.view = MyGraphicsView()

        left_splitter = QSplitter(self)
        right_splitter = QSplitter(self)

        left_splitter.setOrientation(Qt.Orientation.Horizontal)
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        left_splitter.addWidget(code_pane)
        right_splitter.addWidget(self.view)
        right_splitter.addWidget(Color('blue'))
        right_splitter.setSizes([200, 200])

        main_splitter = QSplitter(self)
        main_splitter.addWidget(left_splitter)
        main_splitter.addWidget(right_splitter)
        main_splitter.setStretchFactor(0, 1)
        main_splitter.setStretchFactor(1, 1)
        main_splitter.setSizes([100, 200])

        self.setCentralWidget(main_splitter)

        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle("CodeViz")

    def draw_thing(self):
        self.view.draw_array(0, 100, 100, 5, 50)

    def code_execute(self):
        usercode = self.code_edit.toPlainText()
        tracee = trace.Tracer(usercode)
        #print(tracee)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()
    window.draw_thing()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

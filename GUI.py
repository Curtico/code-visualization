import sys
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

    def paintEvent(self, event):
        super().paintEvent(event)

        # Draw a rectangle
        # self.scene.addRect(10, 10, 100, 100)
        # for i in range(5):
        #     square_width = 100
        #     distance_between_squares = 20
        #     x = i * (square_width + distance_between_squares)
        #     self.scene.addRect(x, 0, square_width, square_width)

        # Draw another rectangle using QPainter

    def paint_array(self, event):
        super().paint_array(event)

        square_width = 50
        square_height = 50
        distance_between_squares = 20

        # Create and add squares to the scene
        self.scene.addRect(20, 20, 100, 100)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        code_pane_buttons = QWidget()
        code_pane_buttons_layout = QHBoxLayout(code_pane_buttons)
        code_pane_buttons_layout.addWidget(QPushButton("Execute"))
        code_pane_buttons_layout.addWidget(QPushButton("Step"))

        code_pane = QWidget()
        code_pane_layout = QVBoxLayout(code_pane)
        code_pane_layout.addWidget(QPlainTextEdit())
        code_pane_layout.addWidget(code_pane_buttons)

        view = MyGraphicsView()

        left_splitter = QSplitter(self)
        right_splitter = QSplitter(self)

        left_splitter.setOrientation(Qt.Orientation.Horizontal)
        right_splitter.setOrientation(Qt.Orientation.Vertical)

        left_splitter.addWidget(code_pane)
        right_splitter.addWidget(view)
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


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()

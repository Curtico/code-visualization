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
        self.arrow = QPixmap("arrow.png")

        self.scene.setSceneRect(-10000, -10000, 20000, 20000)

    def draw_square(self, x, y, width, height):
        self.scene.addRect(x, y, width, height)

    def draw_array(self, y, width, height, items, distance,text):
        self.scene.clear()
        for i in range(items):
            x = i * (width + distance)
            self.scene.addRect(x, y, width, height)
            text_item = QGraphicsTextItem(str(text[i]))
            text_item.setPos(x+width/2 - text_item.boundingRect().width()/2,y+height/2 - text_item.boundingRect().height()/2)
            self.scene.addItem(text_item)
            self.draw_arrow(x+width,y+50,x+distance+width,y+50)

    def draw_arrow(self,start_x,start_y,end_x,end_y):
        self.scene.addLine(start_x,start_y,end_x,end_y)
        self.scene.addLine(end_x-10,end_y-5,end_x,end_y)
        self.scene.addLine(end_x-10,end_y+5,end_x,end_y)




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowIcon(QtGui.QIcon('CV.png'))

        code_execute_button = QPushButton("Execute")
        step_forward_button = QPushButton("Step Forwards")
        step_backwards_button = QPushButton("Step Backwards")
        code_pane_buttons = QWidget()
        code_pane_buttons_layout = QHBoxLayout(code_pane_buttons)
        code_pane_buttons_layout.addWidget(code_execute_button)
        code_execute_button.released.connect(self.code_execute)
        code_pane_buttons_layout.addWidget(step_forward_button)
        step_forward_button.released.connect(self.step)
        code_pane_buttons_layout.addWidget(step_backwards_button)
        step_backwards_button.released.connect(self.step_backwards)
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


        self.primitive_output = QTextEdit(self)
        self.primitive_output.setReadOnly(True)
        self.primitive_output.setPlaceholderText("All Variables in the state will be shown here")
        self.stdout_widget = QTextEdit(self)
        self.stdout_widget.setReadOnly(True)
        self.stdout_widget.setPlaceholderText("All Stdout will be shown here")
        sub_right_splitter = QSplitter(self)
        sub_right_splitter.addWidget(self.primitive_output)
        sub_right_splitter.addWidget(self.stdout_widget)



        left_splitter.addWidget(code_pane)
        right_splitter.addWidget(self.view)
        right_splitter.addWidget(sub_right_splitter)
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
        self.state_index = 0
        self.trace_report = None

    def draw_thing(self):
        #debug
        self.view.draw_array(0, 100, 100, 5, 50)

    def code_execute(self):
        usercode = self.code_edit.toPlainText()
        tracee = trace.Tracer(usercode)
        self.state_index = 0
        self.trace_report = tracee
        

    def show_state(self):
        #print(type(trace.states[29].objects[0].name))
        #print(trace.states[29].stdout)
        #print(trace.states[29].objects[1].name)
        self.primitive_output.clear()
        self.view.scene.clear()
        for each in self.trace_report.states[self.state_index].objects:
            print(each.name)
            if each.instance == "primitive":
                self.primitive_output.append(f"{each.name} = {each.value}")
            elif each.instance == "LIST":
                print(f"LIST = {each.name}, {each.value}")
                print(each.value)
                print(len(each.value))
                self.view.draw_array(0,100,100,len(each.value),50,each.value)
        self.stdout_widget.clear()
        self.stdout_widget.append(self.trace_report.states[self.state_index].stdout)
        print("End of Debug")
    def step(self):
        if self.state_index + 1 < len(self.trace_report.states):
            self.state_index += 1
            print(f"State index -> {self.state_index}")
            self.show_state()
    def step_backwards(self):
        if self.state_index == 0:
           return
        self.state_index -= 1
        print(f"State index -> {self.state_index}")
        self.show_state()

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()

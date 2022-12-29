import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()

        font = self.font()
        font.setPointSize(18)
        self.setFont(font)

        self.setWindowTitle("Rehab Exoskeleton App")
        self.resize(500, 500)

        button1 = QPushButton("Position Control Mode")
        button2 = QPushButton("Gravity Compensation")
        button3 = QPushButton("Position Control with Gravity Compensation")

        left_panel_layout = QVBoxLayout()
        left_panel_layout.addWidget(button1)
        left_panel_layout.addWidget(button2)
        left_panel_layout.addWidget(button3)

        left_panel = QWidget()
        left_panel.setLayout(left_panel_layout)

        line1 = QLineEdit()
        line2 = QLineEdit()
        
        for line in line1, line2:
            line.setMaxLength(3)
        
        button4 = QPushButton("Load Patient Data")

        middle_panel_layout = QVBoxLayout()
        middle_panel_layout.addWidget(line1)
        middle_panel_layout.addWidget(line2)
        middle_panel_layout.addWidget(button4)

        middle_panel = QWidget()
        middle_panel.setLayout(middle_panel_layout)
        
        label1 = QLabel("Instructions for Usage")
        font = label1.font()
        font.setBold(True)
        font.setPointSize(20)
        label1.setFont(font)
        list = QListWidget()
        list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])

        right_panel_layout = QVBoxLayout()
        right_panel_layout.addWidget(label1)
        right_panel_layout.addWidget(list)


        right_panel = QWidget()
        right_panel.setLayout(right_panel_layout)


        initial_screen_layout = QHBoxLayout()
        initial_screen_layout.addWidget(left_panel)
        initial_screen_layout.addWidget(middle_panel)
        initial_screen_layout.addWidget(right_panel)


        self.setLayout(initial_screen_layout)
        

class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()        
        initial_screen = InitialScreen()

        self.setCentralWidget(initial_screen)

        self.show()

app = QApplication(sys.argv)

window = MainWindow()

app.exec()
import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from testing import function1

class Heading(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)      
        font = self.font()
        font.setBold(True)
        font.setPointSize(23)
        self.setFont(font)


class InitialScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = Heading("Modes Available")

        self.button1 = QRadioButton("Position Control")        
        self.button2 = QRadioButton("Gravity Compensation")
        self.button3 = QRadioButton("Position Control \nwith Gravity Compensation")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addStretch(1)
        
        self.setLayout(layout)


class InitialScreenMiddlePanel(QWidget):
        
    def __init__(self):
        super().__init__()

        self.heading = Heading("Patient Details")

        self.label1 = QLabel("Patient Weight (in kilograms)")
        self.line1 = QLineEdit()        
        self.label2 = QLabel("Patient Leg Length (in metre)")
        self.line2 = QLineEdit()
        
        for line in self.line1, self.line2:
            line.setMaxLength(3)
        
        self.button = QPushButton("Save Patient Data")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.label1)
        layout.addWidget(self.line1)
        layout.addWidget(self.label2)
        layout.addWidget(self.line2)
        layout.addStretch(1)
        layout.addWidget(self.button)

        self.setLayout(layout)


class InitialScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = Heading("Instructions for Usage")
        self.list = QListWidget()
        self.list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])
        self.button = QPushButton("Continue")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.list)
        layout.addStretch(1)
        layout.addWidget(self.button)
        self.setLayout(layout)        

class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()
        

        self.left_panel = InitialScreenLeftPanel()
#        left_panel.setStyleSheet("background-color: white;")
        self.middle_panel = InitialScreenMiddlePanel()
        self.right_panel = InitialScreenRightPanel()

        initial_screen_layout = QHBoxLayout()
        initial_screen_layout.addWidget(self.left_panel)
        
        initial_screen_layout.addWidget(self.middle_panel)
        initial_screen_layout.addWidget(self.right_panel)

        self.setLayout(initial_screen_layout)

class GravityCompensationScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.label = QLabel("")

        self.button1 = QPushButton("Start")
        self.button2 = QPushButton("Stop")

        self.button1.clicked.connect(function1)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addStretch(1)
        self.setLayout(layout)        

class GravityCompensationScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = Heading("Instructions for Usage")
        self.list = QListWidget()
        self.list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])
        self.button = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.list)
        layout.addStretch(1)
        layout.addWidget(self.button)
        self.setLayout(layout)        

class GravityCompensationScreen(QWidget):
    def __init__(self):
        super().__init__()
        
        self.left_panel = GravityCompensationScreenLeftPanel()
        self.right_panel = GravityCompensationScreenRightPanel()
        
        layout = QHBoxLayout()
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)

        self.setLayout(layout)

class PositionControlScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__()
    

class PositionControlScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()
    
        self.heading = Heading("Instructions for Usage")
        self.list = QListWidget()
        self.list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])
        self.button = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.list)
        layout.addStretch(1)
        layout.addWidget(self.button)
        self.setLayout(layout)        


class PositionContolScreen(QWidget):

    def __init__(self):
        super().__init__()
        
        self.right_panel = PositionControlScreenRightPanel()
        self.left_panel = PositionControlScreenLeftPanel()
        layout = QHBoxLayout()
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)

        self.setLayout(layout)

class PositionContolWithGravityScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__()    

class PositionContolWithGravityScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()
    
        self.heading = Heading("Instructions for Usage")
        self.list = QListWidget()
        self.list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])
        self.button = QPushButton("Back")

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.list)
        layout.addStretch(1)
        layout.addWidget(self.button)
        self.setLayout(layout)        


class PositionContolWithGravityScreen(QWidget):

    def __init__(self):
        super().__init__()

        self.left_panel = PositionContolWithGravityScreenLeftPanel()        
        self.right_panel = PositionContolWithGravityScreenRightPanel()

        layout = QHBoxLayout()
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)

        self.setLayout(layout)

class PatientDetailsMessage(QMessageBox):
    def __init__(self):

        super().__init__()      
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Patient Details Error")
        self.setText("Please Fill Patient Details!")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        
class ModeMessage(QMessageBox):
    def __init__(self):

        super().__init__()      
        self.setIcon(QMessageBox.Warning)
        self.setWindowTitle("Mode Error")
        self.setText("Please Enter Required Mode!")
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)


class MainWindow(QMainWindow):
    def __init__(self):

        super().__init__()      

        self.patient_leg_length = 0
        self.patient_weight = 0
        
        font = self.font()
        font.setPointSize(18)
        self.setFont(font)
        self.setWindowTitle("Rehab Exoskeleton App: Home")
        self.resize(500, 500)

        self.screens = QStackedWidget()  
        
        self.initial_screen = InitialScreen()
        self.initial_screen.middle_panel.button.clicked.connect(self.button_press_patient_data)
        self.initial_screen.right_panel.button.clicked.connect(self.button_press_fwd)

        self.position_control_screen = PositionContolScreen()
        self.position_control_screen.right_panel.button.clicked.connect(self.button_press_bwd)

        self.gravity_compensation_screen = GravityCompensationScreen()
        self.gravity_compensation_screen.right_panel.button.clicked.connect(self.button_press_bwd)

        self.position_control_with_gravity_screen = PositionContolWithGravityScreen()
        self.position_control_with_gravity_screen.right_panel.button.clicked.connect(self.button_press_bwd)

        self.screens.addWidget(self.initial_screen)
        self.screens.addWidget(self.position_control_screen)
        self.screens.addWidget(self.gravity_compensation_screen)
        self.screens.addWidget(self.position_control_with_gravity_screen)
        self.screens.setCurrentIndex(0)

        self.setCentralWidget(self.screens)

        self.show()

    def button_press_fwd(self):

        if self.patient_leg_length == 0 or self.patient_weight == 0:
            message = PatientDetailsMessage()
            message.exec_()         
        else:
            if self.initial_screen.left_panel.button1.isChecked():
                self.screens.setCurrentIndex(1)
                self.setWindowTitle("Rehab Exoskeleton App: Position Control Mode")
            elif self.initial_screen.left_panel.button2.isChecked():
                self.screens.setCurrentIndex(2)
                self.setWindowTitle("Rehab Exoskeleton App: Gravity Compensation Mode")
            elif self.initial_screen.left_panel.button3.isChecked():
                self.screens.setCurrentIndex(3)
                self.setWindowTitle("Rehab Exoskeleton App: Position Control With Gravity Compensation Mode")
            else:
                message = ModeMessage()
                message.exec_()         

    def button_press_bwd(self):
        self.screens.setCurrentIndex(0)
        self.setWindowTitle("Rehab Exoskeleton App: Home")

    def button_press_patient_data(self):
        self.patient_weight = self.initial_screen.middle_panel.line1.text()
        self.patient_leg_length = self.initial_screen.middle_panel.line2.text()
        self.gravity_compensation_screen.left_panel.label.setText(f"Patient Weight: {self.patient_weight} kg\nPatient Height: {self.patient_leg_length} m")

app = QApplication(sys.argv)

window = MainWindow()

sys.exit(app.exec_())

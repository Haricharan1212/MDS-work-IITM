import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt

class Heading(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)      
        font = self.font()
        font.setBold(True)
        font.setPointSize(23)
        self.setFont(font)

class PlotScreen(QDialog):
    
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)  
        # self.toolbar = NavigationToolbar(self.canvas, self)  

        layout = QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)  
          
        self.setLayout(layout)

    def plot(self):          

        self.figure.clear()

        self.data1 = [0 for i in range(10)] 
        ax1 = self.figure.add_subplot(221)  
        ax1.plot(self.data1, '*-')  
        ax1.set_title("Left Hip")

        self.data2 = [0 for i in range(10)] 
        ax2 = self.figure.add_subplot(222)  
        ax2.plot(self.data2, '*-')  
        ax2.set_title("Right Hip")

        self.data3 = [0 for i in range(10)] 
        ax3 = self.figure.add_subplot(223)  
        ax3.plot(self.data3, '*-')  
        ax3.set_title("Left Knee")

        self.data4 = [0 for i in range(10)] 
        ax4 = self.figure.add_subplot(224)  
        ax4.plot(self.data4, '*-')  
        ax4.set_title("Right Knee")

        self.figure.tight_layout(pad = 3)
        self.canvas.draw()

class MotorInteract(QObject):
    
    def __init__(self):
        super().__init__()
        self.mode = None
        self.on = False
        self.index = 0

        self.mode = None
        self.minimum_position = None
        self.maximum_position = None
        self.minimum_velocity = None
        self.maximum_velocity = None
        
    def run_motor(self):        
        while True:
            print(self.index)
            time.sleep(1)
            self.index += 1
            if not self.on:
                return
  
  
class InputPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.label1 = QLabel("Minimum position")
        self.input1 = QLineEdit()        
        self.label2 = QLabel("Maximum position")
        self.input2 = QLineEdit()        
        self.label3 = QLabel("Minimum Velocity")
        self.input3 = QLineEdit()        
        self.label4 = QLabel("Maximum Velocity")
        self.input4 = QLineEdit()        
        
        self.button = QPushButton("Save Data")
        
        for line in self.input1, self.input2, self.input3, self.input4:
            line.setMaxLength(3)
        
        layout = QGridLayout()
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(0, 1)

        layout.addWidget(self.label1, 0, 0)
        layout.addWidget(self.input1, 0, 1)
        layout.addWidget(self.label2, 1, 0)
        layout.addWidget(self.input2, 1, 1)
        layout.addWidget(self.label3, 2, 0)
        layout.addWidget(self.input3, 2, 1)
        layout.addWidget(self.label4, 3, 0)
        layout.addWidget(self.input4, 3, 1)
        layout.addWidget(self.button, 4, 1)

        self.setLayout(layout)

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
        self.list.setFixedHeight(300)
        self.list.addItems(["1. Enter Patient Details- Patient Leg Length and Patient Weight", "2. Select Required Mode", "3. Handle Device Carefully"])
        self.list.setWordWrap(True)
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

        self.state = False

        self.input_panel = InputPanel()

        self.label = QLabel("")

        self.button0 = QPushButton("Start Motor")
        self.button1 = QPushButton("Start Therapy")
        self.button2 = QPushButton("Stop Therapy")
        self.button3 = QPushButton("Go to Origin")

        self.button1.setDisabled(self.state)
        self.button2.setDisabled(not self.state)

        layout = QVBoxLayout()
        layout.addWidget(self.input_panel)
        layout.addWidget(self.label)
        layout.addWidget(self.button0)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addStretch(1)
        self.setLayout(layout)        

        self.workerThread = QThread()
        self.worker = MotorInteract()
        self.worker.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.worker.run_motor)
        # self.workerThread.finished.connect()
        self.worker.on = self.state
    

class GravityCompensationScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.heading = Heading("Plotting Data")
        # self.list = QListWidget()
        # self.list.addItems(["1. Gravity Compensation Mode: Weight of patient will be provided by motor", "2. Physiotherapist Supervision is required"])
        # self.list.setWordWrap(True)
        
        self.graph = PlotScreen()
        self.button = QPushButton("Back")                
        
        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        # layout.addWidget(self.list)
        layout.addWidget(self.graph)
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
        self.list.setWordWrap(True)

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
        self.list.setWordWrap(True)
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
        font.setFamily("Courier New")
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
        self.gravity_compensation_screen.left_panel.button1.clicked.connect(self.gravity_compensation_start_therapy)
        self.gravity_compensation_screen.left_panel.button2.clicked.connect(self.gravity_compensation_stop)
        self.gravity_compensation_screen.left_panel.input_panel.button.clicked.connect(self.input_panel_button_pressed)

        self.position_control_with_gravity_screen = PositionContolWithGravityScreen()
        self.position_control_with_gravity_screen.right_panel.button.clicked.connect(self.button_press_bwd)

        self.motor_interact = MotorInteract()        

        self.screens.addWidget(self.initial_screen)
        self.screens.addWidget(self.position_control_screen)
        self.screens.addWidget(self.gravity_compensation_screen)
        self.screens.addWidget(self.position_control_with_gravity_screen)
        self.screens.setCurrentIndex(0)

        self.setCentralWidget(self.screens)

        self.show()

    def input_panel_button_pressed(self):
        self.motor_interact.minimum_position = self.gravity_compensation_screen.left_panel.input_panel.input1.text()
        self.motor_interact.maximum_position = self.gravity_compensation_screen.left_panel.input_panel.input2.text()
        self.motor_interact.minimum_velocity = self.gravity_compensation_screen.left_panel.input_panel.input3.text()
        self.motor_interact.maximum_velocity = self.gravity_compensation_screen.left_panel.input_panel.input4.text()

    def gravity_compensation_start_therapy(self):

        self.gravity_compensation_screen.left_panel.workerThread.start()
        self.gravity_compensation_screen.left_panel.state = True
        self.gravity_compensation_screen.left_panel.button1.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button2.setDisabled(False)
        self.gravity_compensation_screen.left_panel.worker.on = True
        self.gravity_compensation_screen.right_panel.button.setDisabled(True)
        self.gravity_compensation_screen.right_panel.graph.plot()

    def gravity_compensation_stop(self):

        self.gravity_compensation_screen.left_panel.state = False
        self.gravity_compensation_screen.left_panel.button1.setDisabled(False)
        self.gravity_compensation_screen.left_panel.button2.setDisabled(True)
        self.gravity_compensation_screen.left_panel.worker.on = False
        self.gravity_compensation_screen.right_panel.button.setDisabled(False)
        self.gravity_compensation_screen.left_panel.workerThread.exit(0)

    def button_press_fwd(self):

        if self.patient_leg_length == 0 or self.patient_weight == 0:
            message = PatientDetailsMessage()
            message.exec_()         
        else:
            if self.initial_screen.left_panel.button1.isChecked():
                self.motor_interact.mode = 1
                self.setWindowTitle("Rehab Exoskeleton App: Position Control Mode")
            elif self.initial_screen.left_panel.button2.isChecked():
                self.motor_interact.mode = 2
                self.setWindowTitle("Rehab Exoskeleton App: Gravity Compensation Mode")
            elif self.initial_screen.left_panel.button3.isChecked():
                self.motor_interact.mode = 3
                self.setWindowTitle("Rehab Exoskeleton App: Position Control With Gravity Compensation Mode")
            else:
                message = ModeMessage()
                message.exec_()         

            self.screens.setCurrentIndex(self.motor_interact.mode)

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

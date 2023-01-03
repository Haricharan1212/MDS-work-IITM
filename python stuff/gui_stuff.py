import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import time
import numpy as np
from scipy import interpolate

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib import pyplot as plt

import tmotorCAN

MINPOSKNEE = -30
MAXPOSKNEE = 30
MINPOSHIP = -30
MAXPOSHIP = 30
# MAXVEL = -15
# MAXPOS = 15

KP = 10
KD = 1

TIMES = [1, 2, 3, 4, 5]

HIP_VALUES = [30, 15, 0, -15, 5]
KNEE_VALUES = [30, 10, 0, -15, 5]
    
class Heading(QLabel):
    def __init__(self, text):
        super().__init__()
        self.setText(text)      
        font = self.font()
        font.setBold(True)
        font.setPointSize(23)
        self.setFont(font)

class Plot(QDialog):
    
    def __init__(self):
        super().__init__()
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)  
        self.toolbar = NavigationToolbar(self.canvas, self)  
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)  
        self.setLayout(layout)

        self.data1 = None
        self.data2 = None

    def plot(self):          

        x = TIMES

        self.figure.clear()
        ax1 = self.figure.add_subplot(211)  
        y = self.data1

        x_new = np.linspace(min(x), max(x), 50)
        bspline = interpolate.make_interp_spline(x, y)
        y_new = bspline(x_new)

        ax1.axhline(y=0, color='k')
        ax1.axvline(x=0, color='k')

        ax1.plot(x_new, y_new, '-')
        ax1.plot(x, y, 's')  
        ax1.set_title("Hip")

        ax2 = self.figure.add_subplot(212)  
        y = self.data2

        x_new = np.linspace(min(x), max(x), 50)
        bspline = interpolate.make_interp_spline(x, y)
        y_new = bspline(x_new)

        ax2.axhline(y=0, color='k')
        ax2.axvline(x=0, color='k')

        ax2.plot(x_new, y_new, '-')
        ax2.plot(x, y, 's')  
        ax2.set_title("Knee")

        self.canvas.draw()

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
        self.index = 0 # For debugging TODO delete
        self.to_origin = False

        self.minimum_position_hip = MINPOSHIP
        self.maximum_position_hip = MAXPOSHIP
        self.minimum_position_knee = MINPOSKNEE
        self.maximum_position_knee = MAXPOSKNEE
                        
        self.left_hip = True
        self.left_knee = True
        self.right_hip = True
        self.right_knee = True
                
        self.left_hip_motor = tmotorCAN.tmotor(2, "ak80-64")       
        self.right_hip_motor = tmotorCAN.tmotor(3, "ak80-64")       
        self.left_knee_motor = tmotorCAN.tmotor(4, "ak80-64")       
        self.right_knee_motor = tmotorCAN.tmotor(5, "ak80-64")       
                
    def run_motor(self):        
        while True:
            time.sleep(0.01)
            if (self.to_origin):
                 # Do something
                 self.to_origin = False                       
            else:
                if (self.on):
                    if (self.mode == 1):

                        print(self.index)
                        time.sleep(1)
                        self.index += 1
                    elif (self.mode == 2):
                        print(self.index)
                        time.sleep(0.1)
                        self.index += 1  

    def start_motors(self):
        if (self.left_hip):
            self.left_hip_motor.start_motor()
        if (self.right_hip):
            self.right_hip_motor.start_motor()
        if (self.left_knee):
            self.left_knee_motor.start_motor()
        if (self.right_knee):
            self.right_knee_motor.start_motor()
    
class InputPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.label1 = QLabel("Minimum position (hip)")
        self.input1 = QLineEdit()        
        self.input1.setText(str(MINPOSHIP))
        self.label2 = QLabel("Maximum position (hip)")
        self.input2 = QLineEdit()        
        self.input2.setText(str(MAXPOSHIP))
        self.label3 = QLabel("Minimum Velocity (knee)")
        self.input3 = QLineEdit()        
        self.input3.setText(str(MINPOSKNEE))
        self.label4 = QLabel("Maximum Velocity (knee)")
        self.input4 = QLineEdit()        
        self.input4.setText(str(MAXPOSKNEE))
        
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

        self.heading1 = Heading("Modes Available")

        self.button1 = QRadioButton("Automatic")        
        self.button2 = QRadioButton("Physiotherapist Guided")

        self.heading2 = Heading("Motors activated")
        self.checkbox1 = QCheckBox("Left Hip Motor")
        self.checkbox2 = QCheckBox("Left Knee Motor")
        self.checkbox3 = QCheckBox("Right Hip Motor")
        self.checkbox4 = QCheckBox("Right Knee Motor")
        
        self.checkbox1.setChecked(True)
        self.checkbox2.setChecked(True)
        self.checkbox3.setChecked(True)
        self.checkbox4.setChecked(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.heading1)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.heading2)
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)
        layout.addWidget(self.checkbox4)
        layout.addStretch(1)
        
        self.setLayout(layout)


class InitialScreenMiddlePanel(QWidget):
        
    def __init__(self):
        super().__init__()

        self.heading = Heading("Patient Details")

        self.label1 = QLabel("Patient Weight (in kilograms)")
        self.line1 = QLineEdit()        
        self.label2 = QLabel("Patient Height (in metre)")
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

        self.heading = Heading("Maximum and Minimum Values")
        self.input_panel = InputPanel()

        self.label = QLabel("")

        self.button0 = QPushButton("Start Motor")
        self.button1 = QPushButton("Start Therapy")
        self.button2 = QPushButton("Stop Therapy")
        self.button3 = QPushButton("Go to Origin")

        self.button0.setDisabled(False)
        self.button1.setDisabled(True)
        self.button2.setDisabled(True)
        self.button3.setDisabled(True)

        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.input_panel)
        layout.addWidget(self.label)
        layout.addWidget(self.button0)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addStretch(1)
        self.setLayout(layout)            

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

class TrajectoryInput(QWidget):
    def __init__(self):
        super().__init__()

        layout = QGridLayout()
        layout.setColumnStretch(0, 1)
        layout.setColumnStretch(1, 0)
        layout.setColumnStretch(2, 1)
        layout.setColumnStretch(3, 0)

        self.texts1 = []
        self.texts2 = []
        self.texts3 = []
        self.inputs1 = []
        self.inputs2 = []
        
        for i in range(1, 6):

            self.texts1.append(QLabel(f"t {TIMES[i - 1]}"))
            self.texts2.append(QLabel(f"hip angle {i}"))
            self.inputs1.append(QLineEdit())        
            self.texts3.append(QLabel(f"knee angle {i}"))
            self.inputs2.append(QLineEdit())        

            layout.addWidget(self.texts1[-1], i -  1, 0)
            layout.addWidget(self.texts2[-1], i -  1, 1)
            layout.addWidget(self.inputs1[-1], i -  1, 2)
            layout.addWidget(self.texts3[-1], i -  1, 3)
            layout.addWidget(self.inputs2[-1], i -  1, 4)
    
        
        for i in range(0, 5):
            self.inputs1[i].setText(str(HIP_VALUES[i]))
            self.inputs2[i].setText(str(KNEE_VALUES[i]))
    
        self.setLayout(layout)

class PositionControlScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__()

        heading = Heading("Points in trajectory")
        
        self.trajectory_input = TrajectoryInput()
        self.button = QPushButton("Update")

        self.label = QLabel("Note: Default Values \n have been Provided")
                
        layout = QVBoxLayout()

        layout.addWidget(heading)
        layout.addWidget(self.trajectory_input)
        layout.addWidget(self.button)
        layout.addStretch(1)
        layout.addWidget(self.label)

        self.setLayout(layout)
        

class PositionControlScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()
    
        self.heading = Heading("Plotting Data")
        self.graph = Plot()        
        self.button1 = QPushButton("Continue")
        self.button2 = QPushButton("Back")                
        
        self.button1.setDisabled(True)
        
        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.graph)
        layout.addStretch(1)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
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

class PositionControlFinalScreenLeftPanel(QWidget):
    def __init__(self):
        super().__init__() 

        self.heading = Heading("Maximum and Minimum Values")

        self.input_panel = InputPanel()           
        self.label = QLabel("")

        self.button0 = QPushButton("Start Motor")
        self.button1 = QPushButton("Start Therapy")
        self.button2 = QPushButton("Stop Therapy")
        self.button3 = QPushButton("Go to Origin")

        layout = QVBoxLayout()

        self.button0.setDisabled(False)
        self.button1.setDisabled(True)
        self.button2.setDisabled(True)
        self.button3.setDisabled(True)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(10)
        
        label1 = QLabel("Low")
        label2 = QLabel("High")
        layout1 = QHBoxLayout()
        layout1.addWidget(label1)
        layout1.addStretch(1)
        layout1.addWidget(label2)
        unit = QWidget()
        unit.setLayout(layout1)
        self.label = QLabel("Speed")
 
        layout.addWidget(self.heading)
        layout.addWidget(self.input_panel)
        layout.addWidget(self.label)
        layout.addWidget(self.slider)
        layout.addWidget(unit)
        layout.addWidget(self.button0)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addStretch(1)

        self.setLayout(layout)

class PositionControlFinalScreenRightPanel(QWidget):
    def __init__(self):
        super().__init__()
        
        self.heading = Heading("Plotting Data")
        
        self.graph = PlotScreen()
        self.button = QPushButton("Back")                
        
        layout = QVBoxLayout()
        layout.addWidget(self.heading)
        layout.addWidget(self.graph)
        layout.addStretch(1)
        layout.addWidget(self.button)
        self.setLayout(layout)        

    
class PositionControlFinalScreen(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.right_panel = PositionControlFinalScreenRightPanel()
        self.left_panel = PositionControlFinalScreenLeftPanel()
        layout = QHBoxLayout()
        layout.addWidget(self.left_panel)
        layout.addWidget(self.right_panel)
        self.setLayout(layout)
    

# class PositionContolWithGravityScreenLeftPanel(QWidget):
#     def __init__(self):
#         super().__init__()    

# class PositionContolWithGravityScreenRightPanel(QWidget):
#     def __init__(self):
#         super().__init__()
    
#         self.heading = Heading("Instructions for Usage")
#         self.list = QListWidget()
#         self.list.addItems(["1. Instruction1", "2. Instruction2", "3. Instruction3"])
#         self.list.setWordWrap(True)
#         self.button = QPushButton("Back")

#         layout = QVBoxLayout()
#         layout.addWidget(self.heading)
#         layout.addWidget(self.list)
#         layout.addStretch(1)
#         layout.addWidget(self.button)
#         self.setLayout(layout)        


# class PositionContolWithGravityScreen(QWidget):

#     def __init__(self):
#         super().__init__()

#         self.left_panel = PositionContolWithGravityScreenLeftPanel()        
#         self.right_panel = PositionContolWithGravityScreenRightPanel()

#         layout = QHBoxLayout()
#         layout.addWidget(self.left_panel)
#         layout.addWidget(self.right_panel)

#         self.setLayout(layout)

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

        self.patient_height = 0
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
        self.position_control_screen.right_panel.button1.clicked.connect(self.button_press_continue)
        self.position_control_screen.right_panel.button2.clicked.connect(self.button_press_bwd)
        self.position_control_screen.left_panel.button.clicked.connect(self.button_press_update)


        self.gravity_compensation_screen = GravityCompensationScreen()
        self.gravity_compensation_screen.right_panel.button.clicked.connect(self.button_press_bwd)
        self.gravity_compensation_screen.left_panel.button0.clicked.connect(self.gravity_compensation_start_motor)
        self.gravity_compensation_screen.left_panel.button1.clicked.connect(self.gravity_compensation_start_therapy)
        self.gravity_compensation_screen.left_panel.button2.clicked.connect(self.gravity_compensation_stop)
        self.gravity_compensation_screen.left_panel.button3.clicked.connect(self.gravity_compensation_go_to_origin)
        self.gravity_compensation_screen.left_panel.input_panel.button.clicked.connect(self.input_panel_button_pressed)

        self.position_control_final_screen = PositionControlFinalScreen()
        self.position_control_final_screen.right_panel.button.clicked.connect(self.button_press_bwd)
        self.position_control_final_screen.left_panel.button0.clicked.connect(self.position_control_start_motor)
        self.position_control_final_screen.left_panel.button1.clicked.connect(self.position_control_start_therapy)
        self.position_control_final_screen.left_panel.button2.clicked.connect(self.position_control_stop)
        self.position_control_final_screen.left_panel.button3.clicked.connect(self.position_control_go_to_origin)
        self.position_control_final_screen.left_panel.input_panel.button.clicked.connect(self.input_panel_button_pressed)

        # self.position_control_with_gravity_screen = PositionContolWithGravityScreen()
        # self.position_control_with_gravity_screen.right_panel.button.clicked.connect(self.button_press_bwd)

        self.motor_interact = MotorInteract()        
        self.workerThread = QThread()
        self.motor_interact.moveToThread(self.workerThread)
        self.workerThread.started.connect(self.motor_interact.run_motor)
        # self.workerThread.finished.connect()

        self.screens.addWidget(self.initial_screen)
        self.screens.addWidget(self.position_control_screen)
        self.screens.addWidget(self.gravity_compensation_screen)
        self.screens.addWidget(self.position_control_final_screen)
        # self.screens.addWidget(self.position_control_with_gravity_screen)
        
        self.screen_mode = 0
        self.screens.setCurrentIndex(self.screen_mode)
        self.setCentralWidget(self.screens)
        self.show()

    def button_press_continue(self):
        self.screen_mode = 3
        self.screens.setCurrentIndex(self.screen_mode)

    def button_press_update(self):

        data1 = []
        data2 = []

        for i in range(0, 5):
            data1.append(int(self.position_control_screen.left_panel.trajectory_input.inputs1[i].text()))
            data2.append(int(self.position_control_screen.left_panel.trajectory_input.inputs2[i].text()))
        
        data1 = np.array(data1)
        data2 = np.array(data2)

        self.position_control_screen.right_panel.graph.data1 = data1
        self.position_control_screen.right_panel.graph.data2 = data2
        self.position_control_screen.right_panel.graph.plot()

        self.position_control_screen.right_panel.button1.setDisabled(False)

    def input_panel_button_pressed(self):
        self.motor_interact.minimum_position_hip = self.gravity_compensation_screen.left_panel.input_panel.input1.text()
        self.motor_interact.maximum_position_hip = self.gravity_compensation_screen.left_panel.input_panel.input2.text()
        self.motor_interact.minimum_position_knee = self.gravity_compensation_screen.left_panel.input_panel.input3.text()
        self.motor_interact.maximum_position_knee = self.gravity_compensation_screen.left_panel.input_panel.input4.text()

    def position_control_start_motor(self):

        self.motor_interact.on = False
        self.workerThread.start()

        self.position_control_final_screen.left_panel.button0.setDisabled(True)
        self.position_control_final_screen.left_panel.button1.setDisabled(False)
        self.position_control_final_screen.left_panel.button2.setDisabled(True)
        self.position_control_final_screen.left_panel.button3.setDisabled(False)

    def position_control_start_therapy(self):

        self.motor_interact.on = True
        self.position_control_final_screen.right_panel.graph.plot()
        
        self.position_control_final_screen.left_panel.button0.setDisabled(True)
        self.position_control_final_screen.left_panel.button1.setDisabled(True)
        self.position_control_final_screen.left_panel.button2.setDisabled(False)
        self.position_control_final_screen.left_panel.button3.setDisabled(True)
        self.position_control_final_screen.right_panel.button.setDisabled(True)
        self.position_control_final_screen.left_panel.slider.setDisabled(True)

        self.position_control_final_screen.left_panel.input_panel.button.setDisabled(True)

    def position_control_stop(self):

        self.position_control_final_screen.left_panel.button0.setDisabled(True)
        self.position_control_final_screen.left_panel.button1.setDisabled(False)
        self.position_control_final_screen.left_panel.button2.setDisabled(True)
        self.position_control_final_screen.left_panel.button3.setDisabled(False)
        self.position_control_final_screen.right_panel.button.setDisabled(False)
        self.position_control_final_screen.left_panel.input_panel.button.setDisabled(False)
        self.position_control_final_screen.left_panel.slider.setDisabled(False)

        self.motor_interact.on = False
        self.workerThread.exit(0)

    def position_control_go_to_origin(self):

        self.motor_interact.to_origin = True
        return

    def gravity_compensation_start_motor(self):

        self.motor_interact.on = False
        self.workerThread.start()

        self.gravity_compensation_screen.left_panel.button0.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button1.setDisabled(False)
        self.gravity_compensation_screen.left_panel.button2.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button3.setDisabled(False)

    def gravity_compensation_start_therapy(self):

        self.motor_interact.on = True
        self.gravity_compensation_screen.right_panel.graph.plot()
        
        self.gravity_compensation_screen.left_panel.button0.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button1.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button2.setDisabled(False)
        self.gravity_compensation_screen.left_panel.button3.setDisabled(True)
        self.gravity_compensation_screen.right_panel.button.setDisabled(True)

        self.gravity_compensation_screen.left_panel.input_panel.button.setDisabled(True)

    def gravity_compensation_stop(self):

        self.gravity_compensation_screen.left_panel.button0.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button1.setDisabled(False)
        self.gravity_compensation_screen.left_panel.button2.setDisabled(True)
        self.gravity_compensation_screen.left_panel.button3.setDisabled(False)
        self.gravity_compensation_screen.right_panel.button.setDisabled(False)
        self.gravity_compensation_screen.left_panel.input_panel.button.setDisabled(False)

        self.motor_interact.on = False
        self.workerThread.exit(0)

    def gravity_compensation_go_to_origin(self):

        self.motor_interact.to_origin = True
        return

    def button_press_fwd(self):

        self.motor_interact.left_hip = self.initial_screen.left_panel.checkbox1.isChecked()
        self.motor_interact.left_knee = self.initial_screen.left_panel.checkbox2.isChecked()
        self.motor_interact.right_hip = self.initial_screen.left_panel.checkbox3.isChecked()
        self.motor_interact.right_knee = self.initial_screen.left_panel.checkbox4.isChecked()

        if self.patient_height == 0 or self.patient_weight == 0:
            message = PatientDetailsMessage()
            message.exec_()         
        else:
            if self.initial_screen.left_panel.button1.isChecked():
                self.motor_interact.mode = 1
                self.screen_mode = 1
                self.setWindowTitle("Rehab Exoskeleton App: Automatic Mode")
            elif self.initial_screen.left_panel.button2.isChecked():
                self.motor_interact.mode = 2
                self.screen_mode = 2
                self.setWindowTitle("Rehab Exoskeleton App: Physiotherapist-guided Mode")
            else:
                message = ModeMessage()
                message.exec_()         

            self.screens.setCurrentIndex(self.screen_mode)

    def button_press_bwd(self):
        if (self.screen_mode <= 2):
            self.screen_mode = 0
        elif (self.screen_mode == 3):
            self.screen_mode = 1
        self.screens.setCurrentIndex(self.screen_mode)
        self.setWindowTitle("Rehab Exoskeleton App: Home")

    def button_press_patient_data(self):
        self.patient_weight = self.initial_screen.middle_panel.line1.text()
        self.patient_height = self.initial_screen.middle_panel.line2.text()
        self.gravity_compensation_screen.left_panel.label.setText(f"Patient Weight: {self.patient_weight} kg\nPatient Height: {self.patient_height} m")


app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())

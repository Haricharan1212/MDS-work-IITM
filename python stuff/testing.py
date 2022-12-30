import time
import tmotorCAN
import numpy as np
import trajectory
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# motor1 = tmotorCAN.tmotor(1, 'ak80-64')
# motor2 = tmotorCAN.tmotor(2, 'ak80-64')
# motor3 = tmotorCAN.tmotor(3, 'ak80-64')
# motor4 = tmotorCAN.tmotor(5, 'ak10-9')
# motor5 = tmotorCAN.tmotor(6, 'ak10-9')

class Worker(QObject):

    def __init__(self):
        super().__init__()
        self.on = False
        self.index = 0

    def function1(self):        
        while True:
            print(self.index)
            time.sleep(1)
            self.index += 1
            if not self.on:
                return
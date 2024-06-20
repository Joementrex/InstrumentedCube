import sys
import serial
import serial.tools.list_ports
from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QTextEdit, QDialog, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox
# get sliders 
from PyQt5 import QtGui, QtCore
import time

import numpy as np
import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
from pyqtgraph.opengl import GLViewWidget, GLBoxItem, GLScatterPlotItem

# global array to store the recieved data
global_data = []

# import pylab 
import pylab as plt
# import numpy as np

# Data container
class DataContainer(QObject):
    data_received = pyqtSignal(np.ndarray)
# Main window
class ComPortApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("COM Port Selector")

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.port_list_widget = QListWidget(self)
        self.layout.addWidget(self.port_list_widget)

        self.refresh_button = QPushButton("Refresh Ports", self)
        self.layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_ports)

        self.open_button = QPushButton("Open Port", self)
        self.layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_selected_port)

        self.ports = []
        self.refresh_ports()

    def refresh_ports(self):
        self.ports = serial.tools.list_ports.comports()
        self.port_list_widget.clear()
        for port in self.ports:
            port_info = f"{port.device} - {port.description}"
            self.port_list_widget.addItem(port_info)

    def open_selected_port(self):
        selected_item = self.port_list_widget.currentItem()
        if selected_item:
            selected_port_info = selected_item.text().split(" - ")[0]
            try:
                self.serial_port = serial.Serial(selected_port_info, baudrate=115200)  # Adjust baudrate if needed
                print(f"Opened port: {selected_port_info}")
                self.show_options_window()
            except Exception as e:
                print(f"Failed to open port {selected_port_info}: {str(e)}")

    def show_options_window(self):
        self.options_window = OptionsWindow(self.serial_port, self)
        self.options_window.show()

    def show_terminal_window(self):
        self.DataContainer = DataContainer()
        self.terminal_window = TerminalWindow(self.serial_port, self.DataContainer)
        self.terminal_window.show()

class OptionsWindow(QDialog):
    def __init__(self, serial_port, parent):
        super().__init__()

        self.setWindowTitle("Select Option")
        self.parent = parent

        self.layout = QVBoxLayout(self)

        self.square_button = QPushButton("Square", self)
        self.layout.addWidget(self.square_button)
        self.square_button.clicked.connect(lambda: self.send_option(1))

        self.cone_button = QPushButton("Cone", self)
        self.layout.addWidget(self.cone_button)
        self.cone_button.clicked.connect(lambda: self.send_option(2))

        self.triangle_button = QPushButton("Triangle", self)
        self.layout.addWidget(self.triangle_button)
        self.triangle_button.clicked.connect(lambda: self.send_option(3))

        self.serial_port = serial_port
        self.serial_port.timeout = 0.1

    def send_option(self, option):
        self.serial_port.write(str(option).encode())
        self.parent.show_terminal_window()
        self.close()

class TerminalWindow(QDialog):
    def __init__(self, serial_port, DataContainer):
        super().__init__()

        self.DataContainer = DataContainer

        self.setWindowTitle("Serial Terminal")

        self.layout = QVBoxLayout(self)

        self.export_checkbox = QCheckBox("Export Data", self)
        self.layout.addWidget(self.export_checkbox)

        self.table_widget = QTableWidget(self)
        self.layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["Sensor ID", "Value", "Timestamp"])

        self.serial_port = serial_port
        self.serial_port.timeout = 0.1

        self.read_timer = self.startTimer(100)

        # add option to open 3D visualizer
        self.visualizer_button = QPushButton("Open 3D Visualizer", self)
        self.layout.addWidget(self.visualizer_button)
        self.visualizer_button.clicked.connect(self.open_visualizer)

    def open_visualizer(self):
        self.visualizer = CubeVisualizer(self.serial_port, self.DataContainer)




    def update_table(self, sensor_id, value, timestamp):
        for row in range(self.table_widget.rowCount()):
            if int(self.table_widget.item(row, 0).text()) == sensor_id:
                self.table_widget.item(row, 1).setText(str(value))
                self.table_widget.item(row, 2).setText(str(timestamp))
                return

        row_position = self.table_widget.rowCount()
        self.table_widget.insertRow(row_position)
        self.table_widget.setItem(row_position, 0, QTableWidgetItem(str(sensor_id)))
        self.table_widget.setItem(row_position, 1, QTableWidgetItem(str(value)))
        self.table_widget.setItem(row_position, 2, QTableWidgetItem(str(timestamp)))

    def timerEvent(self, event):
        if event.timerId() == self.read_timer:
            try:
                if self.serial_port.is_open:
                    data = self.serial_port.read_all().decode()
                    if data:
                        data_array = []
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        for entry in data.strip().split('\n'):
                            try:
                                sensor_id, value = entry.split(":")
                                sensor_id = int(sensor_id.strip().split(" ")[-1])  # Extract sensor ID
                                # sensor_id = int(sensor_id)
                                value = int(value)
                                self.update_table(sensor_id, value, timestamp)

                                #update data array
                                data_array.append([sensor_id, value])
                                
                                if self.export_checkbox.isChecked():
                                    with open("serial_data.csv", "a") as f:
                                        f.write(f"{timestamp},{sensor_id},{value}\n")
                                        
                            except ValueError:
                                pass
                        
                        if data_array:
                            self.DataContainer.data_received.emit(np.array(data_array))
                            # update global data
                            global global_data 
                            global_data = data_array

            except Exception as e:
                print(f"Error reading data from serial port: {str(e)}")




class CubeVisualizer:
    def __init__(self, serial_port, data_container):
        # open new window
        super().__init__()
        self.view = GLViewWidget()
        self.serial_port = serial_port
        self.data_container = data_container
        self.data_container.data_received.connect(self.data_container_reciever)
        # add a delay to make sure the view is initialized before attempting to add content
        self.view.show()

        # Three custom points to make a triangle inside the top face of a cube
        self.point1 = np.array([0.25, 0.75, 1])
        self.point2 = np.array([0.75, 0.75, 1])
        self.point3 = np.array([0.5, 0.25, 1])
        self.points = np.array([self.point1, self.point2, self.point3])

        # Create GLScatterPlotItem using the points array and specifying initial color
        self.point_item = GLScatterPlotItem(pos=self.points, color=(1, 1, 1, 1), size=10)
        self.view.addItem(self.point_item)

        self.cube = GLBoxItem()
        self.view.addItem(self.cube)

        self.view.show()

        ### Redundant code ###
        # Change point colors every 1000 ms
        # self.timer = pg.QtCore.QTimer()
        # self.timer.timeout.connect(self.update_points)
        # self.timer.start(100)

        # # create a view for the GUI
        # self.glWidget = GLViewWidget()
        # # make widget background blue
        # self.glWidget.setBackgroundColor('b')
        # # add a delay to make sure the view is initialized before attempting to add content
        # self.glWidget.show()

        # # add a slider to the GUI
        # sliderX = QtGui.QSlider(QtCore.Qt.Horizontal)
        # sliderX.setRange(1, 1000)
        # sliderX.setValue(500)
        # # add the slider to the GUI
        # self.glWidget.addWidget(sliderX)
        # self.glWidget.show()

        self.init_gui()

        # sys.exit(app.exec_())

    # define function for GUI 
    def init_gui(self):
        central_widget = QtGui.QWidget()
        gui_layout = QtGui.QVBoxLayout()
        central_widget.setLayout(gui_layout)
        self.setCentralWidget(central_widget)
        gui_layout.addWidget(self.glWidget)
        sliderX = QtGui.QSlider(QtCore.Qt.Horizontal)
        sliderX.setRange(1, 1000)
        sliderX.setValue(500)
        gui_layout.addWidget(sliderX)
        


    def get_data(self):
        # array to store sensor data
        data_array = []
        # get data from serial port
        
        # # Get data from the terminal window
        # data = self.serial_port.read_all().decode()
        # if data:
        #     timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        #     for entry in data.strip().split('\n'):
        #         try:
        #             sensor_id, value = entry.split(":")
        #             sensor_id = int(sensor_id.strip().split(" ")[-1])  # Extract sensor ID
        #             # sensor_id = int(sensor_id)
        #             value = int(value)
        #             data_array.append([sensor_id, value])
        #             # print("data recieved in visualiser")
        #             # print(sensor_id, value, timestamp)
        #         except ValueError:
        #             pass
        # print(data_array)
        # return data_array
    
        # return global data array 
        global global_data
        return global_data
        # print(np.random.rand(3, 4))
        # return np.random.rand(3, 4)
    

    
    def process_data(self, data):
        # To do, implement if needed
        # the incoming data is a list of lists with sensor ID and value. 
        # Each sensor has 3 values, x, y and z.
        recieved = data
        # print(recieved)
        processed = []
        # get the abs sum of the x, y and z values
        # in range of 3

        # extract the 2nd element of each list in data
        data2 = [x[1] for x in recieved]
        # take the abs of each value
        data2 = [abs(x) for x in data2]
        # print(data2)
        # for each data in data2, abs and sum the values in groups of three
        # data3 = [sum(data2[i:i+3]) for i in range(0, len(data2), 3)]
        # print(data3)

        data3 = data2[1::3]
        Sensitivity = 600
        data3 = [x/Sensitivity for x in data3]
        processed = [[x, 0.1, 0.1, 1] for x in data3]
        # if any values in processed are greater than 1 set them to 1
        for i in range(len(processed)):
            for j in range(len(processed[i])):
                if processed[i][j] > 1:
                    processed[i][j] = 1
        processed = np.array(processed)
        # take the absolute value of the sum
        # for each value in data3, convert to rgb value
        # data4 = [[x, x, x, 1] for x in data3]

        # print(processed)

        return processed
    
    def update_points(self):
    # Change point colors dynamically during runtime
        self.data = self.get_data()
        self.data = self.process_data(self.data)
        # if the data is not empty
        if self.data != []:
            self.point_item.setData(color=self.data, size=10)
        else:
            print("no data recieved")

        # update the points
        # self.point_item.setData(color=self.data, size=10)
        # print(self.data_container.data_received)
        # self.data = self.data_container.data_received
        # print(self.data)

        # print contents of data_container

    def data_container_reciever(self, data):
        # print("data recieved")
        # print("Is this function running?")
        # print(data)

        # process the data 
        self.data = self.process_data(data)
        # print(self.data)
        # update the points
        self.point_item.setData(color=self.data, size=10)
        

        return 1



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComPortApp()
    window.setGeometry(100, 100, 400, 400)
    window.show()

    sys.exit(app.exec_())

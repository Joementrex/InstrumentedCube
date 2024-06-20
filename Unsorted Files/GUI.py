import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QListWidget, QPushButton, QTextEdit, QDialog, QHBoxLayout
from PyQt5.QtCore import Qt, QEvent

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
                self.serial_port = serial.Serial(selected_port_info, baudrate=9600)  # Adjust baudrate if needed
                print(f"Opened port: {selected_port_info}")
                self.show_terminal_window()
            except Exception as e:
                print(f"Failed to open port {selected_port_info}: {str(e)}")

    def show_terminal_window(self):
        self.terminal_window = TerminalWindow(self.serial_port)
        self.terminal_window.show()

    def create_buttons_layout(self):
        layout = QHBoxLayout()

        self.refresh_button = QPushButton("Refresh Ports", self)
        layout.addWidget(self.refresh_button)
        self.refresh_button.clicked.connect(self.refresh_ports)

        self.open_button = QPushButton("Open Port", self)
        layout.addWidget(self.open_button)
        self.open_button.clicked.connect(self.open_selected_port)

        return layout
    
class TerminalWindow(QDialog):
    def __init__(self, serial_port):
        super().__init__()

        self.setWindowTitle("Serial Terminal")

        self.layout = QVBoxLayout(self)

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # Make the receiving text area read-only
        self.layout.addWidget(self.text_edit)

        self.input_edit = QTextEdit(self)
        self.layout.addWidget(self.input_edit)

        self.send_button = QPushButton("Send", self)
        self.layout.addWidget(self.send_button)
        self.send_button.clicked.connect(self.send_data)

        self.close_button = QPushButton("Close Port", self)
        self.layout.addWidget(self.close_button)
        self.close_button.clicked.connect(self.close_serial_port)

        self.serial_port = serial_port
        self.serial_port.timeout = 0.1  # Set a timeout for reading

        self.read_timer = self.startTimer(100)  # Timer for reading data from serial port

        # Set focus to input_edit and connect Enter key press event
        self.input_edit.setFocusPolicy(Qt.StrongFocus)
        self.input_edit.setFocus()
        self.input_edit.installEventFilter(self)

    def send_data(self):
        data = self.input_edit.toPlainText()
        data = data.encode()
        self.serial_port.write(data)

    def close_serial_port(self):
        if self.serial_port.is_open:
            self.serial_port.close()
            print("Serial port closed")

    def timerEvent(self, event):
        if event.timerId() == self.read_timer:
            try:
                if self.serial_port.is_open:
                    data = self.serial_port.read_all().decode()
                    if data:
                        self.text_edit.insertPlainText(data)
            except Exception as e:
                print(f"Error reading data from serial port: {str(e)}")

    def eventFilter(self, obj, event):
        if obj == self.input_edit and event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Enter or event.key() == Qt.Key_Return:
                self.send_data()
                return True
        return super().eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ComPortApp()
    window.setGeometry(100, 100, 300, 300)
    window.show()
    sys.exit(app.exec_())


# to do 
# setup a page for sensor configuration: 
# The process should activate all sensors and display the output of 
# each individual sensor should be named and activated one by one, this 
# will allow the devices to be connected in a set configuration once the new outer 
# shell is connected 
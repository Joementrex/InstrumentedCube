# This program will read the ESP32 data from the serial port and print it to the console.

import serial
import time

# com port of the ESP32
com_reciever = 'COM8'
# Com of the master device
com_master = 'COM6'
# baud rate of the ESP32
baud_rate = 115200

device = None

# open the serial port
try:
    ser = serial.Serial(com_reciever, baud_rate)
    device = 'reciever'
except:
    print("Error opening Serial Port for reciever, trying master")
    try:
        ser = serial.Serial(com_master, baud_rate)
        device = 'master'
    except:
        print("Error opening Serial Port for master, quitting")
        exit()

print(f"Device: {device}")
time.sleep(2)
# ser2 = serial.Serial(com2, baud_rate)

# Read the esp data from value 0 to value 17 
def read_esp_data():
    # if ser is None:
    #     ser = serial.Serial(com_port, baud_rate)
    if ser.in_waiting > 0:
        # read the data from the serial port
        data = ser.readline().decode('utf-8').strip()

        # if the data does not start with 'Value 0', ignore it and redo the process
        if not data.startswith('Value 0'):
            return read_esp_data()

        # print(data)

# The incoming data from the ESP32 will be in the following format:
# Value 0: value
# Value 1: value
# ...
# Value 17: value

# Grab one set of data from the ESP32
def get_esp_data():
    ser.reset_input_buffer()

    if device == 'reciever':
        data = []
        while data == []:
            while ser.in_waiting <= 0:
                time.sleep(0.01)
                continue

            for i in range(45):
                data.append(ser.readline().decode('utf-8').strip())
                if not data[i].startswith(f'Value {i}'):
                    # print("Error reading data, retrying")
                    data = []
                    break
        # if the data does not start with 'Value 0', ignore it and redo the process
        # if not data[0].startswith('Value 0'):
        #     return get_esp_data()
        
        # organise the data 
        # each sensor will have three values (X, Y, Z)

        # remove the 'Value i: ' from each value
        data = [x.split(': ')[1] for x in data]
        # convert the values to integers
        data = [int(x) for x in data]

    elif device == 'master':
        data = []
        while data == []:
            while ser.in_waiting <= 0:
                time.sleep(0.01)
                continue

            data = ser.readline().decode('utf-8').strip()
                # The data enters as Packet: data,data,data
                # If the data does not start with 'Packet:', ignore it and redo the process
            if not data.startswith('Packet:'):
                data = []
                continue
            # Extract the data from the packet
            data = data.split(': ')[1].split(',')
            # Convert the data to integers
            # data = [int(x) for x in data]
            # remove last element from the list
            # Remove any elements that are ''
            data = [x for x in data if x != '']
            data = [int(x) for x in data]

    return data


# Python serial monitor for ESP32
# This program will read the serial port and display the data in a window 
# It will list the com ports and allow the user to select the port

#import the time library
import time
# import the serial library
import serial

# print out the com ports
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()

# print out the com ports
for port in ports:
    print(port)

# select the com port
comPort = input("Select com port: ")

# open the serial port
ser = serial.Serial(comPort, 115200, timeout=1)

print("\033[H\033[J")

data = ""

# array of data with length 25
dataArray = [0] * 25

RecieveData = False

# main loop
while True:
    # clear the data variable
    data = ""
    # if there is data waiting in the serial buffer 
    if(ser.in_waiting >0):
        # read the data
        data = ser.readline()
        # convert from bytes to string
        data = data.decode("utf-8")
        # print the data
        if (RecieveData == False):
            print(data)

    # check if the data line was a request for data, contains the symbol $
    if data.find("$") != -1:
        # get the shape data from the user
        shape = input("Enter shape: ")
        # send the shape data to the ESP32
        ser.write(shape.encode())

    # if the data starts with a number and contains a semi colon then it is a data line
    # get the data and add it to the array 
    # check if number and semi colon are in the data
    if data.find(":") != -1 and data[0].isdigit():
        RecieveData = True
        # get the number before the semi colon and convert to an integer 
        number = int(data.split(":")[0])
        # get the number after the semi colon and convert to an integer
        value = int(data.split(":")[1])
        # add the data to the array
        dataArray[number] = value

    # if the dataarray is not empty then print it out 
    # style the output so that it is easy to read
    if (RecieveData == True):
        # clear the screen
        print("\033[H\033[J")
        print("Data: ", end="")
        for i in range(0, len(dataArray)):
            print(str(dataArray[i]) + " ", end="")
        print()
        # delay for 1 second
        time.sleep(0.1)
                
    
     

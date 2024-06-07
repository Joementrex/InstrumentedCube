 # This module controls the printer connected through octoprint webserver

import requests
import time

step = 68/5

# Replace with your OctoPrint server URL and API key
octoprint_url = "http://192.168.2.10"
api_key = "BF587631209C498EB55CD8615F12C02E"

# Headers for authentication
headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}

# # Function to send a G-code command
# def send_gcode_command(command):
#     response = requests.post(f"{octoprint_url}/api/printer/command", json={"command": command}, headers=headers)
#     return response.status_code == 204  # HTTP 204 No Content indicates success



# Function to send a G-code command with retry logic
def send_gcode_command(command):
    while True:
        try:
            response = requests.post(f"{octoprint_url}/api/printer/command", json={"command": command}, headers=headers, timeout=60)
            if response.status_code == 204:
                return True  # HTTP 204 No Content indicates success
            else:
                print(f"Failed to send command {command}: {response.status_code}")
        except requests.exceptions.ConnectTimeout as e:
            print(f"Connection timed out while sending command {command}: {e}")
            print("retrying...")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while sending command {command}: {e}")
            print("retrying...")
            break
    return False

# Function to check if the printer is currently busy
def is_printer_busy():
    response = requests.get(f"{octoprint_url}/api/printer", headers=headers)
    if response.status_code == 200:
        printer_data = response.json()
        flags = printer_data['state']['flags']
        return flags['printing'] or flags['paused']
    return True

# Function to test the printer connection 
def test_printer_connection():
    response = requests.get(f"{octoprint_url}/api/version", headers=headers)
    return response.status_code == 200

# Function to disable the motors
def disable_motors():
    send_gcode_command("M18")
    print("Motors disabled")

# Function to home the printer
def home_printer():
    send_gcode_command("G28")
    print("Printer homed")

# Function to move the print head axis by a specified distance
def move_axis_relative(axis, distance, speed):
    # change to relative positioning
    send_gcode_command("G91")
    feed_rate = speed
    # Calculate time to move 
    timeTaken = abs((distance / feed_rate) * 60)
    if axis not in ['x', 'y', 'z']:
        print("Invalid axis specified")
        return
    if is_printer_busy():
        print("Printer is busy. Cannot move axis.")
        return
    if axis == 'x':
        send_gcode_command(send_gcode_command(f"G1 X{distance} F{feed_rate}"))
    elif axis == 'y':
        send_gcode_command(send_gcode_command(f"G1 Y{distance} F{feed_rate}"))
    elif axis == 'z':
        send_gcode_command(send_gcode_command(f"G1 Z{distance} F{feed_rate}"))
    print("Moving print head...")
    time.sleep(timeTaken)
    print(f"Moved {axis} axis by {distance} mm")

    
def move_axis_absolute(axis, position, speed, current_position=None):
    # change to relative positioning
    send_gcode_command("G90")
    feed_rate = speed
    timeSkip = None
    # get current position of the print head
    if current_position != None:
        timeSkip = abs((position - current_position) / feed_rate) * 60

    if axis not in ['x', 'y', 'z']:
        print("Invalid axis specified")
        return
    if is_printer_busy():
        print("Printer is busy. Cannot move axis.")
        return
    if axis == 'x':
        send_gcode_command(send_gcode_command(f"G1 X{position} F{feed_rate}"))
    elif axis == 'y':
        send_gcode_command(send_gcode_command(f"G1 Y{position} F{feed_rate}"))
    elif axis == 'z':
        send_gcode_command(send_gcode_command(f"G1 Z{position} F{feed_rate}"))

    # Calcualte the time it will take to move the print head 
    print("Moving print head...")
    if timeSkip != None:
        time.sleep(timeSkip)
    print(f"Moved {axis} axis to {position} mm")

# Get the current position of the print head using M114
def get_current_position():
    send_gcode_command("M114")
    time.sleep(1)  # Wait a moment for the command to execute
    response = requests.get(f"{octoprint_url}/api/printer/command", headers=headers)
    if response.status_code == 200:
        command_data = response.json()
        for line in command_data['logs']:
            if 'X:' in line and 'Y:' in line and 'Z:' in line:
                print(line)
                return line
    return None

# get current status of the printer all flags
# def get_printer_status():
#     response = requests.get(f"{octoprint_url}/api/printer", headers=headers)
#     if response.status_code == 200:
#         printer_data = response.json()
#         status = printer_data
#         print(status)
#         return status
#     return None

# This status function does not show if the printer is busy while running custom commands
# Find a new function 
def get_printer_status():
    response = requests.get(f"{octoprint_url}/api/job", headers=headers)
    if response.status_code == 200:
        printer_data = response.json()
        status = printer_data
        print(status)
        return status
    return None

# Job does not show if the printer is busy while running custom commands
# Find a new function


# check if the printer is currently moving 

# Get current position using M114 command
if __name__ == "__main__":
    print("Testing printer connection...")
    if test_printer_connection():
        print("Printer connection successful")
    else:
        print("Printer connection failed")

    print("Getting current position...")
    # get_current_position()
    # send m114 command 
    response = requests.post(f"{octoprint_url}/api/printer/command", json={"command": "M114"}, headers=headers)
    print(response.status_code)
    # Get terminal logs
    response = requests.get(f"{octoprint_url}/api/printer/command", headers=headers)
    print(response.json())


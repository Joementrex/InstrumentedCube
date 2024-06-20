import requests
import time

# Replace with your OctoPrint server URL and API key
octoprint_url = "http://192.168.2.10"
api_key = "BF587631209C498EB55CD8615F12C02E"

# Headers for authentication
headers = {
    "X-Api-Key": api_key,
    "Content-Type": "application/json"
}

# Function to send a G-code command
def send_gcode_command(command):
    response = requests.post(f"{octoprint_url}/api/printer/command", json={"command": command}, headers=headers)
    return response.status_code == 204  # HTTP 204 No Content indicates success

# Function to check if the printer is currently busy
def is_printer_busy():
    response = requests.get(f"{octoprint_url}/api/printer", headers=headers)
    if response.status_code == 200:
        printer_data = response.json()
        flags = printer_data['state']['flags']
        return flags['printing'] or flags['paused']
    return True

# Disable motors
send_gcode_command("M18")
print("Motors disabled. Press Enter to continue...")
input()

# Enable relative positioning
send_gcode_command("G91")

# Define the feed rate (e.g., 8000 mm/min)
feed_rate = 8000

try:
    y_travel = 0
    while y_travel < 68:
        # Move 68mm to the right
        send_gcode_command(f"G1 X68 F{feed_rate}")
        while is_printer_busy():
            time.sleep(0.1)
        
        # Move 68mm to the left
        send_gcode_command(f"G1 X-68 F{feed_rate}")
        while is_printer_busy():
            time.sleep(0.1)
        
        # Move 1mm in the Y direction
        send_gcode_command(f"G1 Y1 F{feed_rate}")
        while is_printer_busy():
            time.sleep(0.1)
        
        y_travel += 1
        print(f"Completed movement at Y = {y_travel}mm")

    # Move back to the starting position
    send_gcode_command(f"G1 Y-68 F{feed_rate}")
    while is_printer_busy():
        time.sleep(0.1)

    print("Completed full movement cycle. Press Enter to exit.")

except KeyboardInterrupt:
    print("Script interrupted by user")

# Clean up and reset any settings if needed
send_gcode_command("G90")  # Ensure absolute positioning is enabled
print("Exiting script.")

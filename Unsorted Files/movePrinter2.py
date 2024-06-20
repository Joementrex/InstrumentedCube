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

# Define the feed rate (e.g., 3000 mm/min)
feed_rate = 3000

# Move in a 68mm square in the XY plane with the specified feed rate
send_gcode_command(f"G1 X68 F{feed_rate}")  # Move 68mm in the X direction
send_gcode_command(f"G1 Y68 F{feed_rate}")  # Move 68mm in the Y direction
send_gcode_command(f"G1 X-68 F{feed_rate}")  # Move -68mm in the X direction
send_gcode_command(f"G1 Y-68 F{feed_rate}")  # Move -68mm in the Y direction

# Set back to absolute positioning (optional, based on your use case)
send_gcode_command("G90")

# Wait for the printer to complete the movement
while is_printer_busy():
    time.sleep(1)  # Wait for 1 second before checking again

print("Completed 68mm square movement.")

time.sleep(3)



feed_rate = 10000

# lets make this a loop until enter is pressed
while True:
    time.sleep(3)
    # Enable relative positioning
    send_gcode_command("G91")
    
    # Define the feed rate (e.g., 3000 mm/min)
    feed_rate += 1000
    print(f"Feed rate: {feed_rate} mm/min")
    

    # # Move in a 68mm square in the XY plane incrementing the Y axis from 68 to -68
    # for i in range(68, -69, -1):
    #     send_gcode_command(f"G1 Y{i} F{feed_rate}")
    #     # move in the X axis from 68 to -68
    #     for j in range(68, -69, -1):
    #         send_gcode_command(f"G1 X{j} F{feed_rate}")
    # time.sleep(1)
    # DO NOT USE THIS LOL

    # Move in a 68mm square in the XY plane with the specified feed rate
    send_gcode_command(f"G1 X68 F{feed_rate}")  # Move 68mm in the X direction
    send_gcode_command(f"G1 Y68 F{feed_rate}")  # Move 68mm in the Y direction
    send_gcode_command(f"G1 X-68 F{feed_rate}")  # Move -68mm in the X direction
    send_gcode_command(f"G1 Y-68 F{feed_rate}")  # Move -68mm in the Y direction
    
    # Set back to absolute positioning (optional, based on your use case)
    send_gcode_command("G90")
    
    # Wait for the printer to complete the movement
    while is_printer_busy():
        time.sleep(1)  # Wait for 1 second before checking again
    
    print("Completed 68mm square movement.")
    # print("Press Enter to continue or type 'exit' to exit")
    # if input() == "exit":
    #     break
    # else:
    #     continue

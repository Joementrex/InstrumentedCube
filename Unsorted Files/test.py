import serial
import re
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Initialize serial port (adjust the port and baudrate as needed)
ser = serial.Serial('COM8', baudrate=115200, timeout=0.1)


# Number of values to display on the bar graph
num_values = 17
data_values = [0] * num_values

# Create a bar graph
fig, ax = plt.subplots()
bars = ax.bar(range(1, num_values + 1), data_values)
ax.set_title('Real-time Bar Graph')
ax.set_xlabel('Data Points')
ax.set_ylabel('Values')

# Function to update the bar graph
def update_graph(frame):
    global data_values

    # Read incoming data from serial port
    data = ser.readline().decode('utf-8')

    # Extract values using regular expression
    values = re.findall(r'Value (\d+): (-?\d+)', data)

    # Update data_values with the latest values
    for value in values:
        index = int(value[0])
        data_values[index - 1] = int(value[1])

    # Update bar heights
    for bar, height in zip(bars, data_values):
        bar.set_height(height)

# Set up animation
animation = FuncAnimation(fig, update_graph, blit=False, interval=100)  # Update every 100 milliseconds

# Show the plot
plt.show()

# Close the serial port when the plot is closed
plt.close()
ser.close()
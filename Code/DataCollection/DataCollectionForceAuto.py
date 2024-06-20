# Crappy manual data collection script
import sys
import os
import time
import fileManager
import PrinterController


# Define the csv file and path 
filename = 'faceForceAuto.csv'
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

# Columns to write to the CSV file
columns = ['Face', 'Pos', 'Force', 'X1', 'Y1', 'Z1', \
           'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3', \
           'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', \
           'X6', 'Y6', 'Z6', 'X7', 'Y7', 'Z7', \
           'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9', \
           'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', \
           'X12', 'Y12', 'Z12', 'X13', 'Y13', 'Z13', \
           'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']
# Turn columns into a string to write to the csv file in the first row
columnsString = ','.join(columns)


# FLAGS
# Save data 
saveData = True

startX= 100
startY = 94 

startHeight = 95
# heights = [89, 88, 87]
# heights = [90, 85, 80]
heights = [91, 90, 89, 88, 87]

x = 0
y = 0
z = 0

# Start pos skip 
Skip = 0
# Number of repeats 
Repeats = 1

def generate_grid_center_points(width, height, steps_x, steps_y):
    """
    Generate grid center points for a rectangle of given width and height.

    Args:
        width (float): The width of the rectangle.
        height (float): The height of the rectangle.
        steps_x (int): The number of steps (divisions) along the width.
        steps_y (int): The number of steps (divisions) along the height.

    Returns:
        list: A list of tuples representing the center points of each grid cell.
    """
    step_size_x = width / steps_x
    step_size_y = height / steps_y
    grid_centers = []

    for i in range(steps_x):
        for j in range(steps_y):
            x = (i + 0.5) * step_size_x
            y = (j + 0.5) * step_size_y
            grid_centers.append((x, y))
    
    return grid_centers


if __name__ == "__main__":
    # Add the path to the module
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    # import PrinterController
    import ESPReader

    fileManager.create_csv_file(dir, columnsString)

    force = 0

   # # Test the printer connection
    if PrinterController.test_printer_connection():
        print("Printer connection successful")
    else:
        print("Printer connection failed")
        # exit the program
        exit()


 # Home the printer
    # PrinterController.home_printer()
    # # disable motors
    # PrinterController.disable_motors()
    x = startX
    y = startY
    z = startHeight
    # move the print head z axis by 70mm 
    PrinterController.move_axis_absolute('z', z, 1200)
    # # move the print head to the centre of the bed
    PrinterController.move_axis_absolute('x', x, 1200)
    # PrinterController.move_axis_absolute('y', y, 1200)
    
    # # Move the print head negative 68mm
    # PrinterController.move_axis_absolute('x', x, 5000)
    # PrinterController.move_axis_absolute('y', y, 5000)

    # Move the y axis 100m forward
    y += 100
    PrinterController.move_axis_absolute('y', y, 1200)
    # time.sleep(1)
    # prompt the user to place the device on the bed and press enter
    input("Place Device and Press Enter to continue...")
    # # # move the print head to the start position
    y = startY
    PrinterController.move_axis_absolute('y', y, 1200)

    while True:
            print(f"Current x: {x}, y: {y}")
            print("Press 'w' to move the print head up by 1mm")
            print("Press 's' to move the print head down by 1mm")
            print("Press 'a' to move the print head left by 1mm")
            print("Press 'd' to move the print head right by 1mm")
            print("Press 'Enter' to continue")
            userInput = input()
            if userInput == 'w':
                y += 1
            elif userInput == 's':
                y -= 1
            elif userInput == 'a':
                x -= 1
            elif userInput == 'd':
                x += 1
            elif userInput == '':
                break
            else:
                print("Invalid input")
            PrinterController.move_axis_absolute('x', x, 1200)
            PrinterController.move_axis_absolute('y', y, 1200)
            time.sleep(1)

    StartX = x
    StartY = y

    # Just for testing purposes
    # Move the print head down by 1mm 10 times while enter is pressed and print the z head
    # while True:
    #     print("Press 'Enter' to move the print head down by 1mm")
    #     userInput = input()
    #     if userInput == '':
    #         z -= 1
    #         PrinterController.move_axis_absolute('z', z, 1200)
    #         time.sleep(1)
    #         print(f"Current z: {z}")
    #     else:
    #         exit()

    # Generate grid points for the printer to follow
    width = 68
    height = 68
    steps = 2
    grid_centers = generate_grid_center_points(width,height, steps, steps)

    # Add the startX and startY to the grid points
    grid_centers = [(x + startX, y + startY) for (x, y) in grid_centers]

    pos = 0
    force = 0
    side = 1

    # # Train a bunch of zero data
    if saveData:
        for i in range(500):
            data = ESPReader.get_esp_data()
            data.insert(0, side)
            data.insert(1, pos)
            data.insert(2, force)
            fileManager.write_data_to_csv(filename, data)
            continue

    while True:
        # Loop over the generated grid coordinates and move the print head to each point
        for (xNew,yNew) in grid_centers:
            if pos < Skip:
                print(f"Skipping {pos}")
                pos += 1
                continue
            # Set skip to 0
            Skip = 0
            

            # xNew = xNew + startX
            # yNew = yNew + startY
            # # Get difference between the new and old x and y
            # xDiff = xNew - x
            # yDiff = yNew - y
            oldX = x
            oldY = y
            x = xNew
            y = yNew
            # Move the print head to the new x and y relative
            # PrinterController.move_axis_relative('x', xDiff, 500)
            # PrinterController.move_axis_relative('y', yDiff, 500)
            PrinterController.move_axis_absolute('x', x, 800, oldX)
            PrinterController.move_axis_absolute('y', y, 800, oldY)
            # time.sleep(1)
            pos += 1
            print(f"Position: {pos}")
            # For number of repeats 
            for i in range(Repeats):
                for height in heights:
                    # Move the print head to the new z height
                    oldZ = z
                    z = height
                    PrinterController.move_axis_absolute('z', z, 200, oldZ)
                    # Force is index of the height + 1
                    force = heights.index(height) + 1
                    # time.sleep(1)
                    # Also grab many repeats of the data read
                    for i in range(100):
                        if saveData:
                            # Get the data from the ESP32
                            data = ESPReader.get_esp_data()
                            data.insert(0, side)
                            data.insert(1, pos)
                            data.insert(2, force)
                            fileManager.write_data_to_csv(filename, data)

                # Bring the print head back up to Start Height
                oldZ = z
                z = startHeight
                PrinterController.move_axis_absolute('z', z, 200, oldZ)
                # time.sleep(1)
                 
        pos = 0
        # Also write a bunch of zero data
        if saveData:
            for i in range(1000):
                data = ESPReader.get_esp_data()
                data.insert(0, side)
                data.insert(1, pos)
                data.insert(2, force)
                fileManager.write_data_to_csv(filename, data)
                continue






    # # Print out the data
    # while True:

    #     print("Enter 0 for no face, enter value to skip to that face:")
    #     userInput = input()
    #     face = int(userInput)
    #     if face == 0:
    #         count = 0
    #         while count < 4000:
    #             # data = ESPReader.read_master()
    #             data = ESPReader.get_esp_data()
    #             if data != []:
    #                 data.insert(0, face)
    #                 data.insert(1, 0)
    #                 data.insert(2, 0)
    #                 fileManager.write_data_to_csv(dir, data)
    #                 count += 1
    #                 continue
    #         continue
    #     # Loop through face 1 to 5
    #     for i in range(1, 6):
    #         if i < face:
    #             continue
    #         face = i
    #         # Loop through positions 1 to 4 
    #         for i in range(1, 5):
    #             # Loop through force 1 to 3
    #             for j in range(1, 2): 
    #                 force = j        
    #                 pos = i
    #                 print("Press enter when ready to collect data for position "+ str(i) + " on face " + str(face) + " with force " + str(j))
    #                 input()
    #                 # pos = int(userInput)
    #                 count = 0
    #                 while count < 300:
    #                     # data = ESPReader.read_master()
    #                     data = ESPReader.get_esp_data()
    #                     if data != []:
    #                         data.insert(0, face)
    #                         data.insert(1, pos)
    #                         data.insert(2, force)
    #                         fileManager.write_data_to_csv(dir, data)
    #                         print('Saving data to file')
    #                         count += 1
    #                         continue




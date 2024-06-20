# Crappy manual data collection script
import sys
import os
import time
import fileManager

# Define the csv file and path 
filename = 'ManualFinal3.csv'
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

# Columns to write to the CSV file
columns = ['Face', 'Pos1', 'Pos2', 'Pos3', 'Force1', 'Force2', 'Force3', 'X1', 'Y1', 'Z1', \
           'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3', \
           'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', \
           'X6', 'Y6', 'Z6', 'X7', 'Y7', 'Z7', \
           'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9', \
           'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', \
           'X12', 'Y12', 'Z12', 'X13', 'Y13', 'Z13', \
           'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']

# Skip faces
Skip = 4

def check_for_zero():
    data = ESPReader.get_esp_data()
    if data!=[]:
        print(data)
    return


def data_collect(face, pos, force, samples=500):
    count = 0
    pos1 = pos[0]
    pos2 = pos[1]
    pos3 = pos[2]
    force1 = force[0]
    force2 = force[1]
    force3 = force[2]

    print("Saving face " + str(face) + " positions: " + str(pos1) + ", " + str(pos2) + ", " + str(pos3) + " with force " + str(force1) + ", " + str(force2) + ", " + str(force3))
    while count < samples:
        # data = ESPReader.read_master()
        data = ESPReader.get_esp_data()
        if data != []:
            data.insert(0, face)
            data.insert(1, pos1)
            data.insert(2, pos2)
            data.insert(3, pos3)
            data.insert(4, force1)
            data.insert(5, force2)
            data.insert(6, force3)
            fileManager.write_data_to_csv(dir, data)
            count += 1
            continue


if __name__ == "__main__":
    # Add the path to the module
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    # import PrinterController
    import ESPReader
    
    stringColumns = ','.join(columns)
    # Remove " from the string
    stringColumns = stringColumns.replace('"', '')
    fileManager.create_csv_file(dir, stringColumns)


    # Check for zero values
    # while True:
        # check_for_zero()

    # Print out the data
    while True:
        list_of_positions = []
        list_of_forces = []

        # Define the max values for each element in the array
        max_values = [4, 4, 4]

        # Use nested loops to iterate through all combinations within the defined ranges
        # The first element starts at 1
        for x in range(1, max_values[0] + 1):
            for y in range(0, max_values[1] + 1):
                for z in range(0, max_values[2] + 1):
                    # Skip combinations where y is zero but x or z are not at their minimum
                    if y == 0 and (z > 0):
                        # print("Skipping position 1 " + str([x, y, z]))
                        continue
                    # skip any positions containing the same number except for zero 
                    if x == y or x == z or y == z:
                        if x != 0 and (y != 0 or z != 0):
                            # print("Skipping position 2 " + str([x, y, z]))
                            continue
                    # print([x, y, z])
                    # If y is greater than z and z is not 0 then skip
                    if y > z and z != 0:
                        continue
                    # if x is greater than y and y and z are not 0 then skip 
                    if x > y and (y != 0 or z != 0):
                        # print("Skipping position 3 " + str([x, y, z]))
                        continue
                    list_of_positions.append([x, y, z])

        max_forces = [1, 1, 1]

        for x in range(1, max_forces[0] + 1):
            for y in range(0, max_forces[1] + 1):
                for z in range(0, max_forces[2] + 1):
                    if y == 0 and x > 0 and z > 0:
                        # print("Skipping force " + str([x, y, z]))
                        continue
                    list_of_forces.append([x, y, z])
        # print(list_of_forces)
        # exit()

        # for pos in list_of_positions:
        #     print(pos)
        # exit()
        # print([x, y, z])
        # print(list_of_positions)
        # exit()      
        # Get user input to start
        print("Get ready to collect data. Press enter to start collecting zero face data.")
        input()
        data_collect(0, [0,0,0], [0,0,0], 500)
        # Start collecting data
        # Loop through the faces, positions, and forces
        for face in range(1, 6):
            if face < Skip:
                continue
            for pos in list_of_positions:
                for force in list_of_forces:
                    # print("Press enter when ready to collect data for position "+ str(pos) + " on face " + str(face) + " with force " + str(force))
                    # If index for force is 0 in pos, then skip
                    skip = False
                    for i in range(len(pos)):
                        if pos[i] == 0:
                            if force[i] != 0:
                                # print("Skipping force " + str(force) + " for position " + str(pos))
                                skip = True
                    # Check if pos is not 0 and force is 0 
                    for i in range(len(pos)):
                        if pos[i] != 0:
                            if force[i] == 0:
                                # print("Skipping force " + str(force) + " for position " + str(pos))
                                skip = True
                    # # For now skip any position where the second and third values are 0
                    # if pos[1] != 0:
                    #     skip = True
                    if skip:
                        continue
                    print("Press enter when ready to collect data for position "+ str(pos) + " on face " + str(face) + " with force " + str(force))
                    input()
                    data_collect(face, pos, force, 1500)

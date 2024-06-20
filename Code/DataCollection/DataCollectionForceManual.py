# Crappy manual data collection script
import sys
import os
import time
import fileManager

# Define the csv file and path 
# filename = 'faceForceManualSuperSensitive1.csv'
filename = 'facePosForceManual2.csv'
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


if __name__ == "__main__":
    # Add the path to the module
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    # import PrinterController
    import ESPReader

    fileManager.create_csv_file(dir, columnsString)

    force = 0
    
    # # Check data
    # while True:
    #     data = ESPReader.get_esp_data()
    #     if data != []:
    #         # clear the terminal
    #         print("\033[H\033[J")
    #         print(data)
    #         continue


    # Print out the data
    while True:

        print("Enter 0 for no face, enter value to skip to that face:")
        userInput = input()
        face = int(userInput)
        if face == 0:
            count = 0
            while count < 4000:
                # data = ESPReader.read_master()
                data = ESPReader.get_esp_data()
                if data != []:
                    data.insert(0, face)
                    data.insert(1, 0)
                    data.insert(2, 0)
                    fileManager.write_data_to_csv(dir, data)
                    count += 1
                    continue
            continue
        # Loop through face 1 to 5
        for i in range(1, 6):
            if i < face:
                continue
            face = i
            # Loop through positions 1 to 4 
            for i in range(1, 5):
                # Loop through force 1 to 3
                for j in range(1, 4): 
                    force = j        
                    pos = i
                    print("Press enter when ready to collect data for position "+ str(i) + " on face " + str(face) + " with force " + str(j))
                    input()
                    # pos = int(userInput)
                    count = 0
                    while count < 500:
                        # data = ESPReader.read_master()
                        data = ESPReader.get_esp_data()
                        if data != []:
                            data.insert(0, face)
                            data.insert(1, pos)
                            data.insert(2, force)
                            fileManager.write_data_to_csv(dir, data)
                            print('Saving data to file')
                            count += 1
                            continue





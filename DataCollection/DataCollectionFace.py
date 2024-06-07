# Crappy manual data collection script
import sys
import os
import time
import fileManager

# Define the csv file and path 
filename = 'faceData.csv'
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

if __name__ == "__main__":
    # Add the path to the module
    sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
    # import PrinterController
    import ESPReader

    fileManager.create_csv_file(dir)


    # Print out the data
    while True:

        print("Face")
        userInput = input()
        face = int(userInput)
        count = 0
        while count < 500:
            data = ESPReader.read_master()
            if data != []:
                data.insert(0, face)
                fileManager.write_data_to_csv(dir, data)
                count += 1
                continue





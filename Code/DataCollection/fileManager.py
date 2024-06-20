import csv
import os

# Function to create the CSV file if it does not exist
def create_csv_file(filename, columns):
    if not os.path.isfile(filename):
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Optionally, write the header row if needed
            # writer.writerow(["Side", "Pos", "Force", "X1", "Y1", "Z1", \
            #                  "X2", "Y2", "Z2", "X3", "Y3", "Z3"])  # Modify columns as needed

            # Write row with side pos force and 15 x,y,z values
            writer.writerow([columns])
        print(f"Created file: {filename}")
    else:
        print(f"File {filename} already exists.")

# Function to write a row of data to the CSV file
def write_data_to_csv(filename, data):
    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(data)
    # print(f"Wrote data to {filename}: {data}")
    print(f"Wiring data to {filename}")

# Main execution
if __name__ == "__main__":
    filename = 'Test.csv'
    create_csv_file(filename)

# # Check if file was created and print its content
# if os.path.isfile(filename):
#     print(f"\nContents of {filename}:")
#     with open(filename, mode='r') as file:
#         print(file.read())
# else:
#     print(f"Failed to create {filename}.")

# Print contents of the file 
def print_file_contents(filename):
    if os.path.isfile(filename):
        with open(filename, mode='r') as file:
            print(file.read())


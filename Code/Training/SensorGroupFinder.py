import ESPReader
import numpy as np
import os

def collect_idle_sensor():
    # Wait until some data is available
    while True:
        data = ESPReader.get_esp_data()
        if data != []:
            break
    return np.array(data)

def test_face(face_number, idle_sensor_data):
    input("Press Enter when ready to start testing face {}...".format(face_number))
    print("Testing face {}...".format(face_number))
    most_varied_sensor_set = 0   
    data = ESPReader.get_esp_data()
    if data!= []:
        print(data)
        # Get 9 sensor readings, subtract the idle sensor data and get the sum of the difference
        for i in range(0, 45, 9):
            sensor_set_diff = data[i:i+9] - idle_sensor_data[i:i+9]
            sensor_set_diff_sum = np.sum(sensor_set_diff)
            if sensor_set_diff_sum > most_varied_sensor_set:
                most_varied_sensor_set = i
        most_varied_sensor_set = most_varied_sensor_set // 9
        print(f"Most Varied Sensor Set: {most_varied_sensor_set }")
        # Print sensor numbers 
        print(f"Sensor Numbers: {most_varied_sensor_set * 3 + 1} to {most_varied_sensor_set * 3 + 3}")
        return most_varied_sensor_set

if __name__ == "__main__":
    idle_sensor_data = collect_idle_sensor()
    saved = []
    for face_number in range(1, 6):
        # saved.append = [face_number,test_face(face_number, idle_sensor_data)]
        # Save face number and most varied sensor set to saved
        saved.append([face_number,test_face(face_number, idle_sensor_data)])
        

    
    print(saved)
    # Save sensor order to a file in data folder
    dir = os.path.join(os.path.dirname(__file__), 'Data')

    np.savetxt(os.path.join(dir, 'sensor_order.txt'), saved, fmt='%d')
                
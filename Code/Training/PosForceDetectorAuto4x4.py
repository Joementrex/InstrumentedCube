import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestRegressor
import joblib
import os
import ESPReader
import time
# Ignore warnings
import warnings 
warnings.filterwarnings("ignore")

import threading

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

import threading
import VisPosAuto as Vis

Visualier = True
SkipTrainingIfDone = False


if Visualier == True:
    # Global instance
    vis_instance = Vis.VisualPositionAuto(4, 4, Vis.screen_size)


# Define the csv file and path 
filename = 'Balanced4x4.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)
# Model dir 
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'.pkl')
scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'_scaler.pkl')
data_version_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', str(filename)+'_data_version.csv')


trainingFace = 1
sensorGroup = None
# load sensor order text file
sensorOrder_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'sensor_order.txt')
sensorOrder = pd.read_csv(sensorOrder_dir, header=None)
sensorOrder = sensorOrder.values.tolist()
print(sensorOrder)
# Grab sensor order for the face
sensorOrder = sensorOrder[trainingFace - 1]
# split sensor order into face and pos as they are a string with a space
sensorOrder = sensorOrder[0].split(' ')
print(f"using sensor order: {sensorOrder}")
# print(sensorOrder)
sensorGroup = int(sensorOrder[1])
print(f"using sensor group: {sensorGroup}")
# Grab 
# most_varied_sensor_set = sensorOrder[0]
# print(f"Sensor Numbers: {most_varied_sensor_set * 3 + 1} to {most_varied_sensor_set * 3 + 3}")



class PosDetector:
    def __init__(self, csv_file=dir, model_file=model_dir, scaler_file=scaler_dir, data_version_file=data_version_dir):
        self.csv_file = csv_file
        self.model_file = model_file
        self.model = None
        self.scalerfile = scaler_file
        self.data_version_file = data_version_file

    def train_model(self):
        # Load the data
        data = pd.read_csv(self.csv_file)
        # Get number of rows in the data and store it in data version 
        data_version_current = data.shape[0]


        # If data version exists
        if os.path.exists(self.data_version_file):
            # Load the data version 
            data_version = pd.read_csv(self.data_version_file)
            # Get the count of data rows from the data_version file in the first element 
            data_version_file = data_version.iloc[0,0]
            # If the data version is the same as the data version file, then skip training
            if data_version_file == data_version_current and SkipTrainingIfDone == True:
                print('Data Version is the same, skipping training')
                return

        # Drop rows with NaN values
        data.dropna(inplace=True)

        # Drop rows without 47 values
        data = data[data.apply(lambda x: len(x) == 48, axis=1)]

        # Drop all face 0 rows
        # data = data[data['Face'] != 0]

        # If face is 10 make 0 
        # data.loc[data['Face'] == 10, 'Face'] = 0

        # Equalise the number of face values
        face0 = data[data['Face'] == 0]
        face1 = data[data['Face'] == 1]
        face2 = data[data['Face'] == 2]
        face3 = data[data['Face'] == 3]
        face4 = data[data['Face'] == 4]
        face5 = data[data['Face'] == 5]

        # Get the number of rows in each face
        face0_rows = face0.shape[0]
        face1_rows = face1.shape[0]
        face2_rows = face2.shape[0]
        face3_rows = face3.shape[0]
        face4_rows = face4.shape[0]
        face5_rows = face5.shape[0]

        # Get the minimum number of rows
        print(f'Number of rows in each face: {face0_rows}, {face1_rows}, {face2_rows}, {face3_rows}, {face4_rows}, {face5_rows}')
        min_rows = min(face0_rows, face1_rows, face2_rows, face3_rows, face4_rows, face5_rows)
        print(f'Minimum number of rows: {min_rows}')
        # Get the first min_rows of each face
        face0 = face0.head(min_rows)
        face1 = face1.head(min_rows)
        face2 = face2.head(min_rows)
        face3 = face3.head(min_rows)
        face4 = face4.head(min_rows)
        face5 = face5.head(min_rows)
        # input()


        sample_size = 10
        # Filter out the rows with [0, 0, 0]
        data_no_contact = data[(data['Face'] == 0) & (data['Pos'] == 0) & (data['Force'] == 0)]
        # limit the number of no contact data
        data_no_contact = data_no_contact.sample(sample_size)

        # Filter out the rows for face1 and face2
        data_face1 = data[(data['Face'] == 1)]
        data_face2 = data[(data['Face'] == 2)]

        # Initialize an empty list to store the sampled data
        sampled_data = []

        # Sample 'sample_size' values for each combination of face, position, and force
        for face_data in [data_face1, data_face2]:
            for face in range(1, sample_size):  # Assuming face1 and face2
                for pos in range(1, 17):  # Assuming positions 1 to 16
                    for force in range(1, 6):  # Assuming forces 1 to 5
                        sampled_data.append(face_data[(face_data['Pos'] == pos) & (face_data['Force'] == force)].sample(sample_size))

        # Concatenate the sampled dataframes into a single dataframe
        sampled_data = pd.concat(sampled_data)

        # Combine the no-contact data with the sampled data
        final_data = pd.concat([data_no_contact, sampled_data])
        print(final_data)
        # save 
        final_data.to_csv('TestData.csv', index=False)
        # exit()
        data = final_data


        # # Reduce the sample size keeping an even number of samples for each face force and pos
        # face0 = face0.sample(n=1000, random_state=42)
        # #get 10 samples of each force of each pos of each face
        # face1 = face1.groupby(['Pos', 'Force']).head(10)

        # Concatenate the faces
        # data = pd.concat([face0, face1, face2, face3, face4, face5], ignore_index=True)


        # Extract features and target
        features = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3',
                         'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6',
                         'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9',
                         'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12',
                         'X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
        target = data[['Face', 'Pos', 'Force']]

        # Group every 3 sensor readings 
        if sensorGroup:
            print(f"Only training on sensor group {sensorGroup} for face {trainingFace}")
            sensorGroup1 = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3']] # Face 3
            sensorGroup2 = data[['X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6']]
            sensorGroup3 = data[['X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9']]
            sensorGroup4 = data[['X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12']]
            sensorGroup5 = data[['X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
            # Make tuple of the sensor groups
            sensorGroups = (sensorGroup1, sensorGroup2, sensorGroup3, sensorGroup4, sensorGroup5)
            features = sensorGroups[sensorGroup]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Initialize and train the model
        print('Training model...')
        timeStart = time.time()
        self.model = RandomForestClassifier(random_state=100)
        # Make regressor
        # self.model = RandomForestRegressor(random_state=42) # Regressor has poor pos accuracy
        self.model.fit(X_train_scaled, y_train)
        print('Model trained')
        timeEnd = time.time()
        timeTaken = timeEnd - timeStart
        print(f'Training time: {timeEnd - timeStart}')

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        # accuracy = accuracy_score(y_test, y_pred)
        # accuracy = self.model.score(X_test, y_test)
        # print(f'Accuracy: {accuracy}')

        # # Save the model and scaler
        joblib.dump(self.model, self.model_file)
        joblib.dump(scaler, self.scalerfile)

        # clear the data version file 
        if os.path.exists(self.data_version_file):
            os.remove(self.data_version_file)
        # Write the data version to the data_version_dir in the first element
        pd.DataFrame([data_version_current]).to_csv(self.data_version_file, index=False)
        # Save time taken in data version file
        pd.DataFrame([timeTaken]).to_csv(self.data_version_file, mode='a', header=False, index=False)

        

    def run_inference(self):
        # Load the model and scaler
        self.model = joblib.load(self.model_file)
        scaler = joblib.load(self.scalerfile)

        # Load the machine model 
        # model = keras.models.load_model('face_model.h5')

    
        # Read data from ESP32 (you need to implement ESPReader.read_master)
        while True:
            # data = ESPReader.read_master()
            data = ESPReader.get_esp_data()
            # If data is not 45 values long, continue
            if len(data) != 45:
                print('Data not long enough')
                continue
            if data!= []:

                 # Group every every 9 sensor readings
                if sensorGroup:
                    sensorGroup1 = data[0:9]
                    sensorGroup2 = data[9:18]
                    sensorGroup3 = data[18:27]
                    sensorGroup4 = data[27:36]
                    sensorGroup5 = data[36:45]
                    # Make tuple of the sensor groups
                    sensorGroups = (sensorGroup1, sensorGroup2, sensorGroup3, sensorGroup4, sensorGroup5)
                    data = sensorGroups[sensorGroup]

                # Clear the terminal 
                print("\033[H\033[J")
                # Ensure that data includes the correct number of features
                data_scaled = scaler.transform([data])
                pred = self.model.predict(data_scaled)
                # pred_face = pred[0]

                # print the prediction
                # print(f'Predicted Face and Pos: {pred}')

                pred_face = pred[0][0]
                pred_pos = pred[0][1]
                pred_force = pred[0][2]
                # convert face and pos to integers
                pred_face = int(round(pred_face))
                pred_pos = int(round(pred_pos))
                print(f'Predicted Face: {pred_face}')
                print(f'Predicted Pos: {pred_pos}')
                print(f'Predicted Force: {pred_force}')
                print(' ')

                # Set pos to zero if the face is zero 
                if pred_face == 0:
                    pred_pos = 0
                if pred_pos == 0:
                    pred_face = 0

                

                if Visualier == True:
                    pred_pos = pred_pos - 1
                    vis_instance.change_all_square_colors(Vis.GREY)
                    if pred_face >= 0:
                        # Multiply the first element of Vis.RED by the force prediction
                        Colour = 255 * (pred_force / 5)
                        Colour = (Colour, 0, 0)
                        vis_instance.change_square_color(pred_pos, Colour ) 

def run_pygame():
    vis_instance.run()

if __name__ == '__main__':
    classifier = PosDetector()
    classifier.train_model()
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()
    vis_instance.change_all_square_colors(Vis.GREY)
    print('Running inference...')
    classifier.run_inference()

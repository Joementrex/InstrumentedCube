import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os
# import ESPReader
import time
# Ignore warnings
import warnings 
warnings.filterwarnings("ignore")

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

import threading
import VisForce as Vis

Visualier = True
forceTrain = True

if Visualier == False:
# Run vis main in a thread
    vis_thread = threading.Thread(target=Vis.main)
    vis_thread.start()


# Define the csv file and path 
# filename = 'faceForceManualSuperSensitive1.csv'
filename = 'facePosForceManual2.csv'
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


class ForceDetector:
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
            if data_version_file == data_version_current and forceTrain == False:
                print('Data Version is the same, skipping training')
                return

        # Drop rows with NaN values
        data.dropna(inplace=True)

        # Drop rows without 47 values
        data = data[data.apply(lambda x: len(x) == 48, axis=1)]

        # # Extract features and target
        features = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3',
                         'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6',
                         'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9',
                         'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12',
                         'X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
        
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


        target = data[['Face','Pos', 'Force']]

        print(features)
        exit()

        # Only keep target and features data
        # data = data[[target, features]]

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Initialize and train the model
        # self.model = RandomForestClassifier(random_state=500)
        # self.model.fit(X_train_scaled, y_train)

        # initalize MultiOutputRegressor
        self.model = MultiOutputRegressor(RandomForestRegressor(random_state=100))
        self.model =  RandomForestRegressor(random_state=42)
        print('Training Model')
        self.model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        # accuracy = accuracy_score(y_test, y_pred)
        # print(f'Accuracy: {accuracy}')

        print('Model Trained')
        # # Save the model and scaler
        # Save the model and scaler in the model_dir and scaler_dir
        # joblib.dump

        joblib.dump(self.model, self.model_file)
        joblib.dump(scaler, self.scalerfile)

        # clear the data version file 
        if os.path.exists(self.data_version_file):
            os.remove(self.data_version_file)
        # Write the data version to the data_version_dir in the first element
        pd.DataFrame([data_version_current]).to_csv(self.data_version_file, index=False)



    def run_inference(self):
        import ESPReader
        # Load the model and scaler
        self.model = joblib.load(self.model_file)
        scaler = joblib.load(self.scalerfile)

        # Load the machine model 
        # model = keras.models.load_model('face_model.h5')

    
        # Read data from ESP32 (you need to implement ESPReader.read_master)
        while True:
            # data = ESPReader.read_master()
            data = ESPReader.get_esp_data()
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
                # pred_force = pred[0][2]

                # Turn pred_face and pred_pos into integers
                print(f'Predicted Face: {pred_face}')
                print(f'Predicted Pos: {pred_pos}')
                pred_face = int(round(pred_face))
                pred_pos = int(round(pred_pos))
                print(f'Predicted Face: {pred_face}')
                print(f'Predicted Pos: {pred_pos}')
                print(f'Predicted Force: {pred_force}')
                print(' ')

                # Set pos to zero if the face is zero 
                if pred_face == 0:
                    pred_pos = 0


                # print(f'Predicted Face: {pred_face}')

                # round the prediction to the nearest integer
                # pred_face = int(round(pred_face[0]))
                # turn the prediction into a single value not an array 
                # pred_face = 'None'
                # Change the face in the vis
                if Visualier == True:
                    Vis.drawTextPos(pred_pos)
                    if pred_face == 0 or pred_pos == 0:
                        Vis.colour_face('None')
                        Vis.change_square_color('None', 0)
                    elif pred_face == 1:
                        Vis.colour_face('Top')
                        Vis.change_square_color('Top', pred_pos, pred_force)
                    elif pred_face == 2:
                        Vis.colour_face('Front')
                        Vis.change_square_color('Front', pred_pos, pred_force)
                    elif pred_face == 3:
                        Vis.colour_face('Left')
                        Vis.change_square_color('Left', pred_pos, pred_force)
                    elif pred_face == 4:
                        Vis.colour_face('Right')
                        Vis.change_square_color('Right', pred_pos, pred_force)
                    elif pred_face == 5:
                        Vis.colour_face('Back')
                        Vis.change_square_color('Back', pred_pos, pred_force)
                    # Vis.change_square_color(pred_face, pred_pos)


if __name__ == '__main__':
    classifier = ForceDetector()
    classifier.train_model()
    # print('Training Skipped')
    # classifier.run_inference()

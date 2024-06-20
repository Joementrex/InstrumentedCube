import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
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


if Visualier == True:
    # Global instance
    vis_instance = Vis.VisualPositionAuto(5, 5, Vis.screen_size)


# Define the csv file and path 
filename = 'facePosForceAuto.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)
# Model dir 
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'.pkl')
scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'_scaler.pkl')
data_version_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', str(filename)+'_data_version.csv')

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
            if data_version_file == data_version_current:
                print('Data Version is the same, skipping training')
                return

        # Drop rows with NaN values
        data.dropna(inplace=True)
        
        # Drop force column
        data = data.drop(columns=['Force'])

        # Drop rows without 47 values
        data = data[data.apply(lambda x: len(x) == 47, axis=1)]

        # Extract features and target
        features = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3',
                         'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6',
                         'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9',
                         'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12',
                         'X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
        target = data[['Face', 'Pos']]

        #

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Initialize and train the model
        print('Training model...')
        self.model = RandomForestClassifier(random_state=500)
        self.model.fit(X_train_scaled, y_train)
        print('Model trained')

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        # accuracy = accuracy_score(y_test, y_pred)
        # print(f'Accuracy: {accuracy}')

        # # Save the model and scaler
        joblib.dump(self.model, self.model_file)
        joblib.dump(scaler, self.scalerfile)

        # clear the data version file 
        if os.path.exists(self.data_version_file):
            os.remove(self.data_version_file)
        # Write the data version to the data_version_dir in the first element
        pd.DataFrame([data_version_current]).to_csv(self.data_version_file, index=False)


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
                print(f'Predicted Face: {pred_face}')
                print(f'Predicted Pos: {pred_pos}')
                print(' ')

                # Set pos to zero if the face is zero 
                if pred_face == 0:
                    pred_pos = 0
                if pred_pos == 0:
                    pred_face = 0

                

                if Visualier == True:
                    pred_pos = pred_pos  - 1
                    vis_instance.change_all_square_colors(Vis.GREY)
                    if pred_face >= 0:
                        vis_instance.change_square_color(pred_pos, Vis.RED)

def run_pygame():
    vis_instance.run()

if __name__ == '__main__':
    classifier = PosDetector()
    # classifier.train_model()
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()
    print('Running inference...')
    classifier.run_inference()

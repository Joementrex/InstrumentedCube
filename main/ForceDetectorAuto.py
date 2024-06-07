import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
from sklearn.multioutput import MultiOutputRegressor
import joblib
import os
import ESPReader
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





# Define the csv file and path 
filename = 'faceForceAuto.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)
# Model dir 
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'.pkl')
scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'_scaler.pkl')

# Check if file exists
try:
    with open(dir) as f:
        pass
except FileNotFoundError:
    print(f'File {dir} not found. Please check the file path and try again.')
    exit()

# Print the contents of the file and pause



class ForceDetector:
    def __init__(self, csv_file=dir, model_file=model_dir, scaler_file=scaler_dir):
        self.csv_file = csv_file
        self.model_file = model_file
        self.model = None
        self.scalerfile = scaler_file
        self.data = None

        if Visualier == True:
        # Run vis main in a thread
            vis_thread = threading.Thread(target=Vis.main)
            vis_thread.start()

    def update_data(self, data):
        self.data = data


    def run_inference(self):
        # Load the model and scaler
        self.model = joblib.load(self.model_file)
        scaler = joblib.load(self.scalerfile)
    
        while True:
            # data = ESPReader.read_master()
            data = ESPReader.get_esp_data()
            if data!= [] and data != None:
                # print('Data: ', data)
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
                # Set self.data to None
                self.data = None


if __name__ == '__main__':
    classifier = ForceDetector()
    # print('Training Skipped')
    classifier.run_inference()

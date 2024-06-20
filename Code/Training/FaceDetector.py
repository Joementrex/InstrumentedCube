import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib
import os
import ESPReader
# Ignore warnings
import warnings 
warnings.filterwarnings("ignore")

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

import threading
import VisFace as Vis



# Run vis main in a thread
vis_thread = threading.Thread(target=Vis.main)
vis_thread.start()

# Define the csv file and path 
filename = 'faceData.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

# Check if file exists
try:
    with open(dir) as f:
        pass
except FileNotFoundError:
    print(f'File {dir} not found. Please check the file path and try again.')
    exit()

# Print the contents of the file and pause



class FaceClassifier:
    def __init__(self, csv_file=dir, model_file='face_model.pkl'):
        self.csv_file = csv_file
        self.model_file = model_file
        self.model = None

    def train_model(self):
        # Load the data
        data = pd.read_csv(self.csv_file)

        # Drop rows with NaN values
        data.dropna(inplace=True)

        # Extract features and target
        features = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3',
                         'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6',
                         'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9',
                         'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12',
                         'X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
        target = data['Face']

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Initialize and train the model
        self.model = RandomForestClassifier(random_state=500)
        self.model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        accuracy = accuracy_score(y_test, y_pred)
        print(f'Accuracy: {accuracy}')


        # Try again but lets use a machine learning model to predict the face
        # make a model that can predict the face based on the data
        # import the necessary libraries for a model from scratch 
       

        # Define the model
        model = Sequential()
        model.add(Dense(128, input_dim=45, activation='relu'))
        model.add(Dense(64, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(6, activation='softmax'))
        
        
        # Compile the model
        model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        # Train the model
        model.fit(X_train_scaled, y_train, epochs=100, batch_size=16, verbose=1)

        # Evaluate the model
        _, accuracy = model.evaluate(X_test_scaled, y_test)
        print(f'Accuracy: {accuracy}')

        # save the model 
        model.save('face_model.h5')


        # Save the model and scaler
        joblib.dump(self.model, self.model_file)
        joblib.dump(scaler, 'scaler.pkl')

    def run_inference(self):
        # Load the model and scaler
        self.model = joblib.load(self.model_file)
        scaler = joblib.load('scaler.pkl')

        # Load the machine model 
        model = keras.models.load_model('face_model.h5')


        # Read data from ESP32 (you need to implement ESPReader.read_master)
        while True:
            data = ESPReader.read_master()
            if data!= []:
                # Clear the terminal 
                print("\033[H\033[J")
                # Ensure that data includes the correct number of features
                data_scaled = scaler.transform([data])
                pred_face = self.model.predict(data_scaled)

                print(f'Predicted Face: {pred_face}')

                # round the prediction to the nearest integer
                # pred_face = int(round(pred_face[0]))
                # turn the prediction into a single value not an array 
                pred_face = pred_face[0]
                # Change the face in the vis
                if pred_face == 0:
                    Vis.colour_face('None')
                elif pred_face == 1:
                    Vis.colour_face('Top')
                elif pred_face == 2:
                    Vis.colour_face('Front')
                elif pred_face == 3:
                    Vis.colour_face('Right')
                elif pred_face == 4:
                    Vis.colour_face('Left')
                elif pred_face == 5:
                    Vis.colour_face('Back')

                # Make a prediction using the machine learning model
                data_scaled = scaler.transform([data])
                pred_face = model.predict(data_scaled, verbose=0)
                pred_face = pred_face[0]
                # pred_face = int(round(pred_face))
                # print(f'Predicted Face Model: {pred_face}')
                # Get the highest value from the prediction
                pred_face = pred_face.tolist()
                pred_face = pred_face.index(max(pred_face))
                print(f'Predicted Face Model: {pred_face}')

                # Change the face in the vis
                # if pred_face == 0:
                #     Vis.colour_face('None')
                # elif pred_face == 1:
                #     Vis.colour_face('Top')
                # elif pred_face == 2:
                #     Vis.colour_face('Front')
                # elif pred_face == 3:
                #     Vis.colour_face('Right')
                # elif pred_face == 4:
                #     Vis.colour_face('Left')
                # elif pred_face == 5:
                #     Vis.colour_face('Back')

if __name__ == '__main__':
    classifier = FaceClassifier()
    # classifier.train_model()
    classifier.run_inference()

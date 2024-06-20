import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import accuracy_score
import joblib
import os
import ESPReader
import time
# Ignore warnings
import warnings 
warnings.filterwarnings("ignore")
import threading
import VisPosAuto as Vis

# import tensorflow as tf
# from tensorflow import keras
# from tensorflow.keras import layers
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense

import threading
# import VisMultiPos as Vis

Visualier = True
Skip_Training = False


# if Visualier == True:
# # Run vis main in a thread
#     vis_instance = Vis.VisualPositionAuto(2, 2, Vis.screen_size)


# Define the csv file and path 
filename = 'ManualFinal3.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)
# Model dir 
model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'.pkl')
scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', str(filename)+'_scaler.pkl')


sensorGroup = None
# load sensor order text filez
sensorOrder_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', 'sensor_order.txt')
sensorOrder = pd.read_csv(sensorOrder_dir, header=None)
sensorOrder = sensorOrder.values.tolist()
print("Original sensor order: " + str(sensorOrder))




class MultiPosDetector:
    def __init__(self, csv_file=dir, model_file=model_dir, scaler_file=scaler_dir, sensorOrder=sensorOrder, face=1):
        self.csv_file = csv_file
        self.model_file = model_file
        self.model = None
        self.scalerfile = scaler_file
        self.sensorOrder = sensorOrder
        # self.face = None
        self.sensorGroup = None 
        self.scaler = None
        self.face = face

        self.model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', f'MultiPosDetector{self.face}.pkl')
        self.scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', f'MultiPosDetector{self.face}_scaler.pkl')

    def train_model(self):
        # Load the data
        data = pd.read_csv(self.csv_file)
        # self.face = face
        # shape of data
        print(data.shape)

        # Drop rows with NaN values
        # data.dropna(inplace=True)

        # Drop rows without 52 columns
        # data = data[data.apply(lambda x: len(x) == 52, axis=1)]
        zero_data = data[data['Face'] == 0]
        # face_data = data[data['Face'] == self.face]
        # # Empty data
        # data = []
        # data = pd.concat([zero_data, face_data])
        # print(data.shape)
        # Remove all data that doesn't match the face numnber
        data.drop(data[data['Face'] != self.face].index, inplace=True)
        data = pd.concat([zero_data, data])

        # Extract features and target
        features = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3',
                         'X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6',
                         'X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9',
                         'X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12',
                         'X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
        target = data[['Face', 'Pos1', 'Pos2', 'Pos3', 'Force1', 'Force2', 'Force3']]



        sensorOrder = self.sensorOrder
        sensorOrder = sensorOrder[self.face-1]
        sensorOrder = sensorOrder[0].split(' ')
        sensorOrder = [int(x) for x in sensorOrder]
        self.sensorGroup = int(sensorOrder[1])
        sensorGroup = self.sensorGroup
        print(f"Sensor group: {sensorGroup}")
        # exit()

        # Group every 3 sensor readings 
        if sensorGroup is not None:
            print(f"Only training on sensor group {sensorGroup} for face {self.face}")
            sensorGroup1 = data[['X1', 'Y1', 'Z1', 'X2', 'Y2', 'Z2', 'X3', 'Y3', 'Z3']] 
            sensorGroup2 = data[['X4', 'Y4', 'Z4', 'X5', 'Y5', 'Z5', 'X6', 'Y6', 'Z6']]
            sensorGroup3 = data[['X7', 'Y7', 'Z7', 'X8', 'Y8', 'Z8', 'X9', 'Y9', 'Z9']]
            sensorGroup4 = data[['X10', 'Y10', 'Z10', 'X11', 'Y11', 'Z11', 'X12', 'Y12', 'Z12']]
            sensorGroup5 = data[['X13', 'Y13', 'Z13', 'X14', 'Y14', 'Z14', 'X15', 'Y15', 'Z15']]
            # Make tuple of the sensor groups
            sensorGroups = (sensorGroup1, sensorGroup2, sensorGroup3, sensorGroup4, sensorGroup5)
            features = sensorGroups[sensorGroup]

     

        # Remove the data from the sensor group that is not zero or matching self.face
        
        # Save modified data to a new csv file
        # data.to_csv('Data/UghStrange.csv', index=False)
        # exit()



        # print(sensorGroup)
        # print out features 
        # print("Features: ")
        # print(features)
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Initialize and train the model
        print("Training model...")
        self.model =  RandomForestRegressor(random_state=42)
        self.model = RandomForestClassifier(random_state=400)
        self.model.fit(X_train_scaled, y_train)
        print("Model trained successfully")

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        # accuracy = accuracy_score(y_test, y_pred)
        # print(f'Accuracy: {accuracy}')

        # # Save the model and scaler with face number 
        model_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', f'MultiPosDetector{self.face}.pkl')
        scaler_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', f'MultiPosDetector{self.face}_scaler.pkl')
        joblib.dump(self.model, model_dir)
        joblib.dump(scaler, scaler_dir)
        self.model_file = model_dir
        self.scalerfile = scaler_dir

        return self.model, scaler

    def load_model(self):
        # Load the model and scaler
        self.model = joblib.load(self.model_file)
        self.scaler = joblib.load(self.scalerfile)
        return self.model, self.scaler

    def set_sensor_group(self, sensorGroup):
        sensorOrder = self.sensorOrder
        sensorOrder = sensorOrder[self.face-1]
        sensorOrder = sensorOrder[0].split(' ')
        sensorOrder = [int(x) for x in sensorOrder]
        self.sensorGroup = int(sensorOrder[1])
        sensorGroup = self.sensorGroup
        print(f"Sensor group: {sensorGroup}")
        return sensorGroup


    def run_inference(self, data=[]):
        # Load the model and scaler
        if self.model is None or self.scaler is None:
            self.load_model()

        # check if sensor group is set 
        if self.sensorGroup is None:
            self.set_sensor_group(self.sensorGroup)




        # Load the machine model 
        # model = keras.models.load_model('face_model.h5')

    
        # Read data from ESP32 (you need to implement ESPReader.read_master)
        # while True:
            # data = ESPReader.read_master()
            # data = ESPReader.get_esp_data(ignoreErrors=True)
            # print(data)
        if data!= []:
                # Group every every 9 sensor readings
            # if self.sensorGroup:
            sensorGroup1 = data[0:9]
            sensorGroup2 = data[9:18]
            sensorGroup3 = data[18:27]
            sensorGroup4 = data[27:36]
            sensorGroup5 = data[36:45]
                # Make tuple of the sensor groups
            sensorGroups = (sensorGroup1, sensorGroup2, sensorGroup3, sensorGroup4, sensorGroup5)
            data = sensorGroups[self.sensorGroup]


            # Clear the terminal 
            # print("\033[H\033[J")
            # Ensure that data includes the correct number of features
            data_scaled = self.scaler.transform([data])
            pred = self.model.predict(data_scaled)
            # pred_face = pred[0]

            # print the prediction
            # print(f'Predicted Face and Pos: {pred}')

            pred_face = pred[0][0]
            pred_pos1 = pred[0][1]
            pred_pos2 = pred[0][2]
            pred_pos3 = pred[0][3]
            pred_force1 = pred[0][4]
            pred_force2 = pred[0][5]
            pred_force3 = pred[0][6]

            # print(f'Predicted Face: {pred_face}')
            # print(f'Predicted Pos1: {pred_pos1}')
            # print(f'Predicted Pos2: {pred_pos2}')
            # print(f'Predicted Pos3: {pred_pos3}')
            # print(f'Predicted Force1: {pred_force1}')
            # print(f'Predicted Force2: {pred_force2}')
            # print(f'Predicted Force3: {pred_force3}')
            # print(' ')

            # if Visualier == True:
            #     pred_pos1 = pred_pos1 - 1
            #     pred_pos2 = pred_pos2 - 1
            #     pred_pos3 = pred_pos3 - 1
            #     vis_instance.change_all_square_colors(Vis.GREY)
            #     if pred_face >= 0:
            #         # Multiply the first element of Vis.RED by the force prediction
            #         Colour = 255 * (pred_force1 / 5)
            #         Colour = (Colour, 0, 0)
            #         vis_instance.change_square_color(pred_pos1, Colour ) 
            #         Colour = 255 * (pred_force2 / 5)
            #         Colour = (Colour, 0, 0)
            #         vis_instance.change_square_color(pred_pos2, Colour )
            #         Colour = 255 * (pred_force3 / 5)
            #         Colour = (Colour, 0, 0)
            #         vis_instance.change_square_color(pred_pos3, Colour )
            
            return pred_face, pred_pos1, pred_pos2, pred_pos3, pred_force1, pred_force2, pred_force3



def run_pygame():
    vis_instance.run()
            
if __name__ == '__main__':

    if Visualier == True:
        vis_instance = Vis.VisualPositionAuto(2, 2, Vis.screen_size)
        # vis_instance.run()

    list_of_classifiers = []
    for face in range(1, 6):
    #     # Include the fance number in the class name
    #     # nameClass = f'MultiPosDetector{face}'
        classifier = MultiPosDetector(face=face)
        if Skip_Training == False:
            print(f'Training model for face {face}')
            classifier.train_model()
        list_of_classifiers.append(classifier)
    # This method breaks for some reason? Make them all manually 
    # Init with face 1
    # classifier1 = MultiPosDetector(face=1)
    # # classifier1 = MultiPosDetector()
    # classifier1.train_model()
    # list_of_classifiers.append(classifier1)
    # classifier2 = MultiPosDetector(face=2)
    # classifier2.train_model()
    # list_of_classifiers.append(classifier2)

    
    # exit()
    
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()
    vis_instance.change_all_square_colors(Vis.GREY)
    print('Running inference...')
    # classifier.run_inference()

    while True:
        list_of_preds = []
        data = ESPReader.get_esp_data()
        if data != []:
            # Clear the terminal
            print("\033[H\033[J")
            
            for classifier in list_of_classifiers:
                pred = classifier.run_inference(data)
                face = list_of_classifiers.index(classifier) + 1
                print(f'Face: {face}')
                print("Prediction: ", pred)
                print(' ')

                list_of_preds.append(pred)


            if Visualier:
                vis_instance.change_all_square_colors(Vis.GREY)

                for pred in list_of_preds:
                    face = pred[0]
                    pred_pos1 = pred[1] - 1
                    pred_pos2 = pred[2] - 1
                    pred_pos3 = pred[3] - 1        
                    # Give each face a different colour
                    if face == 1:
                        vis_instance.change_square_color(pred_pos1, [255 * (pred[4] / 5), 0, 0] )
                        vis_instance.change_square_color(pred_pos2, [255 * (pred[5] / 5), 0, 0] )
                        vis_instance.change_square_color(pred_pos3, [255 * (pred[6] / 5), 0, 0] )
                    elif face == 2:
                        vis_instance.change_square_color(pred_pos1, [0, 255 * (pred[4] / 5), 0] )
                        vis_instance.change_square_color(pred_pos2, [0, 255 * (pred[5] / 5), 0] )
                        vis_instance.change_square_color(pred_pos3, [0, 255 * (pred[6] / 5), 0] )
                    elif face == 3:
                        vis_instance.change_square_color(pred_pos1, [0, 0, 255 * (pred[4] / 5)] )
                        vis_instance.change_square_color(pred_pos2, [0, 0, 255 * (pred[5] / 5)] )
                        vis_instance.change_square_color(pred_pos3, [0, 0, 255 * (pred[6] / 5)] )
                    elif face == 4:
                        vis_instance.change_square_color(pred_pos1, [255 * (pred[4] / 5), 255 * (pred[4] / 5), 0] )
                        vis_instance.change_square_color(pred_pos2, [255 * (pred[5] / 5), 255 * (pred[5] / 5), 0] )
                        vis_instance.change_square_color(pred_pos3, [255 * (pred[6] / 5), 255 * (pred[6] / 5), 0] )
                    elif face == 5:
                        vis_instance.change_square_color(pred_pos1, [255 * (pred[4] / 5), 0, 255 * (pred[4] / 5)] )
                        vis_instance.change_square_color(pred_pos2, [255 * (pred[5] / 5), 0, 255 * (pred[5] / 5)] )
                        vis_instance.change_square_color(pred_pos3, [255 * (pred[6] / 5), 0, 255 * (pred[6] / 5)] )


                # pred_pos1 = pred[1] - 1
                # pred_pos2 = pred[2] - 1
                # pred_pos3 = pred[3] - 1
                # pred_force1 = pred[4]
                # pred_force2 = pred[5]
                # pred_force3 = pred[6]
                # # Get face from index of classifier
                # face = list_of_classifiers.index(classifier) + 1
                # print(f'Face: {face}')
                # print(f'Pos1: {pred_pos1}' + f' Pos2: {pred_pos2}' + f' Pos3: {pred_pos3}')
                # print(f'Force1: {pred_force1}' + f' Force2: {pred_force2}' + f' Force3: {pred_force3}')
                # print(' ')

        # print(data)
        # Get p
        # pred = list_of_classifiers.run_inference(data)
        # print("Prediction: ", pred)
        
        # if Visualier == True:
        #     pred_pos1 = pred[1] - 1
        #     pred_pos2 = pred[2] - 1
        #     pred_pos3 = pred[3] - 1
        #     vis_instance.change_all_square_colors(Vis.GREY)
        #     if pred[0] >= 0:
        #         # Multiply the first element of Vis.RED by the force prediction
        #         Colour = 255 * (pred[4] / 5)
        #         Colour = (Colour, 0, 0)
        #         vis_instance.change_square_color(pred_pos1, Colour ) 
        #         Colour = 255 * (pred[5] / 5)
        #         Colour = (Colour, 0, 0)
        #         vis_instance.change_square_color(pred_pos2, Colour )
        #         Colour = 255 * (pred[6] / 5)
        #         Colour = (Colour, 0, 0)
        #         vis_instance.change_square_color(pred_pos3, Colour )








import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten, LSTM
from tensorflow.keras.callbacks import EarlyStopping
import os
import ESPReader
import warnings 
warnings.filterwarnings("ignore")
import threading
import VisPosAuto as Vis



vis_instance = Vis.VisualPositionAuto(5, 5, Vis.screen_size)
# Define the csv file and path 
filename = 'facePosForceAuto.csv'
# The path is up one directory from the current file, then into the Data directory
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

# Load your data into a pandas DataFrame
data = pd.read_csv(dir)

# Set all face values that are 10 to 0
data.loc[data['Face'] == 10, 'Face'] = 0

# Separate features and targets
features = data.iloc[:, 3:].values  # Sensor readings
targets = data.iloc[:, :3].values   # Side, Pos, Force

# Normalize features
scaler = StandardScaler()
features = scaler.fit_transform(features)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

def build_and_train_fcnn():
    model = Sequential()
    model.add(Dense(256, input_dim=45, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(128, activation='relu'))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(X_train, y_train, epochs=200, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    mae = model.evaluate(X_test, y_test, verbose=0)[1]
    model.save('fcnn_model.h5')
    return mae

def build_and_train_cnn():
    X_train_reshaped = X_train.reshape(X_train.shape[0], 5, 3, 3, 1)
    X_test_reshaped = X_test.reshape(X_test.shape[0], 5, 3, 3, 1)

    model = Sequential()
    model.add(Conv2D(32, (2, 2), activation='relu', padding='same', input_shape=(5, 3, 3, 1)))
    model.add(MaxPooling2D((2, 2)))
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.3))
    model.add(Dense(64, activation='relu'))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(X_train_reshaped, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    mae = model.evaluate(X_test_reshaped, y_test, verbose=0)[1]
    model.save('cnn_model.h5')
    return mae

def build_and_train_lstm():
    X_train_reshaped = X_train.reshape(X_train.shape[0], 5, 9)
    X_test_reshaped = X_test.reshape(X_test.shape[0], 5, 9)

    model = Sequential()
    model.add(LSTM(64, input_shape=(5, 9), return_sequences=True))
    model.add(LSTM(32))
    model.add(Dropout(0.2))
    model.add(Dense(32, activation='relu'))
    model.add(Dense(3, activation='linear'))

    model.compile(optimizer='adam', loss='mse', metrics=['mae'])

    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    model.fit(X_train_reshaped, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])
    mae = model.evaluate(X_test_reshaped, y_test, verbose=0)[1]
    model.save('lstm_model.h5')
    return mae

def run_inference_fcnn(model_path, input_data):
    # Load the model with custom_objects
    model = load_model(model_path, custom_objects={'mse': 'mean_squared_error'})
    
    # Ensure input data is normalized using the same scaler
    input_data = scaler.transform(np.array(input_data).reshape(1, -1))
    
    # Predict
    prediction = model.predict(input_data)
    return prediction


def run_pygame():
    vis_instance.run()


if __name__ == "__main__":
    fcnn_mae = build_and_train_fcnn()
    # cnn_mae = build_and_train_cnn()
    # lstm_mae = build_and_train_lstm()

    # print(f"FCNN MAE: {fcnn_mae}")
    # print(f"CNN MAE: {cnn_mae}")
    # print(f"LSTM MAE: {lstm_mae}")

    # Example inference with the FCNN model
    test_input = X_test[1]  # Replace with your actual input data
    # Load model from model directory 
    fcnn_model = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Models', 'fcnn_model.h5')
    prediction = run_inference_fcnn(fcnn_model, test_input)
    print(f"FCNN Prediction: {prediction}")

    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()
    vis_instance.change_all_square_colors(Vis.GREY)

    # Get data from ESP32
    while True:
        data = ESPReader.get_esp_data()
        if data != []:
            prediction = run_inference_fcnn(fcnn_model, data)
            # Clear the terminal
            print("\033[H\033[J")
            # print(f"FCNN Prediction: {prediction}")
            # Extract the predicted face, pos, and force
            pred_face = int(round(prediction[0][0]))
            pred_pos = int(round(prediction[0][1]))
            pred_force = prediction[0][2]
            print(f"Predicted Face: {pred_face}")
            print(f"Predicted Pos: {pred_pos}")
            print(f"Predicted Force: {pred_force}")
            # If pred_force is greater than 5 set it to 5
            pred_force = 5 if pred_force > 5 else pred_force
            # Change the face in the vis
            if vis_instance:
                pred_pos = pred_pos - 1
                vis_instance.change_all_square_colors(Vis.GREY)
                if pred_face >= 0:
                    # Multiply the first element of Vis.RED by the force prediction
                    colour = 255 * (pred_force / 5)
                    colour = (colour, 0, 0)
                    vis_instance.change_square_color(pred_pos, colour)


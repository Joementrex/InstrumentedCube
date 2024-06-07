import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import mean_squared_error
from sklearn.cluster import KMeans
import joblib
import ESPReader
import numpy as np
import warnings
warnings.filterwarnings("ignore")
import os

# Define the csv file and path 
filename = 'manualCollection.csv'
dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Data', filename)

# Check if file exists
try:
    with open(dir) as f:
        pass
except FileNotFoundError:
    print(f'File {dir} not found. Please check the file path and try again.')
    exit()

class ModelTrainer:
    def __init__(self, csv_file=dir, model_file='model.pkl'):
        self.csv_file = csv_file
        self.model_file = model_file
        self.model = None
        self.n_clusters = 5  # Adjust number of clusters based on the expected number of faces
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42)

    def train_model(self):
        # Load the data from the CSV file
        data = pd.read_csv(self.csv_file)
        data.dropna(inplace=True)

        # Extract the features (XYZ values) and target variables (Pos)
        features = data[[f'X{i}' for i in range(1, 16)] + 
                        [f'Y{i}' for i in range(1, 16)] + 
                        [f'Z{i}' for i in range(1, 16)]]
        target = data[['Pos']]

        # Group sensors by face
        faces = [
            [f'X{i}', f'Y{i}', f'Z{i}', f'X{i+1}', f'Y{i+1}', f'Z{i+1}', f'X{i+2}', f'Y{i+2}', f'Z{i+2}']
            for i in range(1, 16, 3)
        ]

        # Use KMeans to cluster sensors based on their spatial coordinates
        cluster_labels = np.zeros((features.shape[0], len(faces)))
        for idx, face in enumerate(faces):
            sensor_positions = features[face].values
            self.kmeans.fit(sensor_positions)
            cluster_labels[:, idx] = self.kmeans.labels_

        # Add the cluster labels to the features dataframe
        for i in range(self.n_clusters):
            features[f'cluster_{i}'] = (cluster_labels == i).astype(int).sum(axis=1)

        # Split the data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

        # Scale the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Initialize the model
        self.model = MultiOutputRegressor(RandomForestRegressor(random_state=100))

        # Train the model
        self.model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        y_pred = self.model.predict(X_test_scaled)

        # Evaluate the model
        mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
        print(f'Mean Squared Error for Pos: {mse}')

        # Save the model
        joblib.dump(self.model, self.model_file)

        return scaler

    def run_inference(self, scaler):
        while True:
            data = ESPReader.read_master()
            if data != []:
                sensor_positions = np.array(data).reshape(1, 15, 3)
                self.kmeans.fit(sensor_positions[0])
                cluster_labels = self.kmeans.labels_
                for i in range(self.n_clusters):
                    data.append((cluster_labels == i).astype(int).sum())

                data_scaled = scaler.transform([data])
                preds = self.model.predict(data_scaled)

                print("\033[H\033[J")
                print(sensor_positions)
                print(f'Predicted Pos: {preds}')

if __name__ == '__main__':
    trainer = ModelTrainer()
    scaler = trainer.train_model()
    trainer.model = joblib.load('model.pkl')
    trainer.run_inference(scaler)

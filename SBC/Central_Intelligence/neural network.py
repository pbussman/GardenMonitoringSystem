import sqlite3
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# Connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')

# Load data from the Readings table
readings_query = "SELECT * FROM Readings"
readings_df = pd.read_sql_query(readings_query, conn)

# Load data from the Weather table
weather_query = "SELECT * FROM Weather"
weather_df = pd.read_sql_query(weather_query, conn)

# Merge the two dataframes on the timestamp column
data_df = pd.merge(readings_df, weather_df, on='timestamp')

# Define the feature columns and target column
feature_columns = ['air_temperature', 'humidity_x', 'soil_moisture', 'soil_temperature', 'ambient_light', 'temperature_f', 'humidity_y', 'precipitation_inches', 'wind_speed_mph']
target_column = 'soil_moisture'

# Create a binary target column: 1 if soil moisture is below a threshold (e.g., 30), otherwise 0
data_df['water'] = (data_df[target_column] < 30).astype(int)

# Split the data into features (X) and target (y)
X = data_df[feature_columns]
y = data_df['water']

# Standardize the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Build the neural network model
model = Sequential()
model.add(Dense(64, input_dim=len(feature_columns), activation='relu'))
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=10, validation_split=0.2)

# Evaluate the model
y_pred = (model.predict(X_test) > 0.5).astype("int32")
print(classification_report(y_test, y_pred))

# Save the trained model to a file
model.save('garden_watering_model.h5')

print("Model training complete. The model is saved as 'garden_watering_model.h5'.")

# Close the database connection
conn.close()

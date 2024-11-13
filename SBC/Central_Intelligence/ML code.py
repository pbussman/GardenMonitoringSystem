import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')

# Load data from the Readings table
readings_query = "SELECT * FROM Readings"
readings_df = pd.read_sql_query(readings_query, conn)

# Load data from the Weather table
weather_query = "SELECT * FROM Weather"
weather_df = pd.read_sql_query(weather_query, conn)

# Load data from the FloatSensorReadings table
float_sensors_query = "SELECT * FROM FloatSensorReadings"
float_sensors_df = pd.read_sql_query(float_sensors_query, conn)

# Merge the dataframes on the timestamp column
data_df = pd.merge(readings_df, weather_df, on='timestamp')
data_df = pd.merge(data_df, float_sensors_df, on='timestamp')

# Define the feature columns and target column
feature_columns = [
    'air_temperature', 'humidity_x', 'soil_moisture', 'soil_temperature', 'ambient_light',
    'temperature_f', 'humidity_y', 'precipitation_inches', 'wind_speed_mph',
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4'
]
target_column = 'soil_moisture'

# Create a binary target column: 1 if soil moisture is below a threshold (e.g., 30), otherwise 0
data_df['water'] = (data_df[target_column] < 30).astype(int)

# Split the data into features (X) and target (y)
X = data_df[feature_columns]
y = data_df['water']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest classifier
clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y_train)

# Make predictions on the test set
y_pred = clf.predict(X_test)

# Print the classification report
print(classification_report(y_test, y_pred))

# Save the trained model to a file
joblib.dump(clf, 'garden_watering_model.pkl')

print("Model training complete. The model is saved as 'garden_watering_model.pkl'.")

# Close the database connection
conn.close()

import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, filename='ml_training.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')

# Connect to the SQLite database
conn = sqlite3.connect('sensor_data.db')
logging.info("Connected to the SQLite database.")

# Load data from the Readings table
readings_query = "SELECT * FROM Readings"
readings_df = pd.read_sql_query(readings_query, conn)
logging.info("Loaded data from the Readings table.")

# Load data from the Weather table
weather_query = "SELECT * FROM Weather"
weather_df = pd.read_sql_query(weather_query, conn)
logging.info("Loaded data from the Weather table.")

# Load data from the FloatSensorReadings table
float_sensors_query = "SELECT * FROM FloatSensorReadings"
float_sensors_df = pd.read_sql_query(float_sensors_query, conn)
logging.info("Loaded data from the FloatSensorReadings table.")

# Load data from the Maintenance table
maintenance_query = "SELECT * FROM Maintenance"
maintenance_df = pd.read_sql_query(maintenance_query, conn)
logging.info("Loaded data from the Maintenance table.")

# Merge the dataframes on the timestamp column
data_df = pd.merge(readings_df, weather_df, on='timestamp')
data_df = pd.merge(data_df, float_sensors_df, on='timestamp')
logging.info("Merged dataframes on the timestamp column.")

# Aggregate maintenance activities by garden bed and date
maintenance_agg = maintenance_df.groupby(['garden_bed_id', 'date']).agg({
    'activity': lambda x: ','.join(x),  # Combine activities into a single string
    'notes': lambda x: ' '.join(x)  # Combine notes into a single string
}).reset_index()
logging.info("Aggregated maintenance activities by garden bed and date.")

# Merge with the main dataset
data_df = pd.merge(data_df, maintenance_agg, left_on=['garden_bed_id', 'timestamp'], right_on=['garden_bed_id', 'date'], how='left')
logging.info("Merged maintenance activities with the main dataset.")

# Create binary features for maintenance activities
data_df['watering'] = data_df['activity'].apply(lambda x: 1 if 'watering' in x else 0)
data_df['fertilizing'] = data_df['activity'].apply(lambda x: 1 if 'fertilizing' in x else 0)
logging.info("Created binary features for maintenance activities.")

# Define the feature columns and target column
feature_columns = [
    'air_temperature', 'humidity_x', 'soil_moisture', 'soil_temperature', 'ambient_light',
    'temperature_f', 'humidity_y', 'precipitation_inches', 'wind_speed_mph',
    'sensor_1', 'sensor_2', 'sensor_3', 'sensor_4',
    'watering', 'fertilizing',  # Add more features as needed
    'barrel_water_level', 'house_water_availability'  # New features for water sources
]
target_column = 'water_source'  # New target column for water source

# Create a binary target column: 0 for house water supply, 1 for water barrels
data_df['water_source'] = data_df['activity'].apply(lambda x: 1 if 'barrel' in x else 0)
logging.info("Created binary target column for water source.")

# Handle missing values
data_df = data_df.fillna(method='ffill').fillna(method='bfill')
logging.info("Handled missing values.")

# Split the data into features (X) and target (y)
X = data_df[feature_columns]
y = data_df['water_source']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
logging.info("Split the data into training and testing sets.")

# Hyperparameter tuning using Grid Search
param_grid = {
    'n_estimators': [50, 100, 200],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4]
}

grid_search = GridSearchCV(estimator=RandomForestClassifier(random_state=42), param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
grid_search.fit(X_train, y_train)
logging.info("Completed Grid Search for hyperparameter tuning.")

# Best parameters from Grid Search
best_params = grid_search.best_params_
logging.info(f"Best parameters: {best_params}")

# Train the Random Forest classifier with the best parameters
clf = RandomForestClassifier(**best_params, random_state=42)
clf.fit(X_train, y_train)
logging.info("Trained the Random Forest classifier with the best parameters.")

# Make predictions on the test set
y_pred = clf.predict(X_test)
logging.info("Made predictions on the test set.")

# Print the classification report
report = classification_report(y_test, y_pred)
logging.info(f"Classification report:\n{report}")
print(report)

# Save the trained model to a file
joblib.dump(clf, 'garden_watering_model.pkl')
logging.info("Model training complete. The model is saved as 'garden_watering_model.pkl'.")

# Close the database connection
conn.close()
logging.info("Closed the database connection.")

import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import joblib

# Generate synthetic industrial dataset
np.random.seed(42)

data_size = 500

temperature = np.random.uniform(350, 550, data_size)
pressure = np.random.uniform(8, 18, data_size)
machine_load = np.random.uniform(40, 100, data_size)
runtime = np.random.uniform(1, 10, data_size)

# Realistic industrial formula + noise
energy = (
    temperature * 0.75 +
    pressure * 14 +
    machine_load * 6 +
    runtime * 55 +
    np.random.normal(0, 20, data_size)
)

# Create dataframe
df = pd.DataFrame({
    "temperature": temperature,
    "pressure": pressure,
    "machine_load": machine_load,
    "runtime": runtime,
    "energy": energy
})

X = df[["temperature", "pressure", "machine_load", "runtime"]]
y = df["energy"]

# Train model
model = LinearRegression()
model.fit(X, y)

# Save model
joblib.dump(model, "energy_model.pkl")

print("Model trained and saved successfully.")
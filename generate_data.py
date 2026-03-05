import pandas as pd
import numpy as np

np.random.seed(42)

data = {
    "Machine_ID": np.random.randint(1, 6, 500),
    "Temperature": np.random.normal(75, 5, 500),
    "Production_Time": np.random.normal(8, 2, 500),
    "Output": np.random.normal(100, 15, 500),
}

df = pd.DataFrame(data)

df["Energy_Consumed"] = (
    0.5 * df["Temperature"] +
    2 * df["Production_Time"] +
    0.3 * df["Output"] +
    np.random.normal(0, 5, 500)
)

df["Emission_Factor"] = 0.82
df["Carbon_Emission"] = df["Energy_Consumed"] * df["Emission_Factor"]

df.to_csv("data/manufacturing_data.csv", index=False)

print("Data Generated Successfully!")
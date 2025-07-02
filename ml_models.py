import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

# Load data
df = pd.read_csv("logs.csv")

# Encode categorical columns
le_location = LabelEncoder()
le_device = LabelEncoder()

df["location_encoded"] = le_location.fit_transform(df["location"])
df["device_encoded"] = le_device.fit_transform(df["device"])

# Features and target
X = df[["location_encoded", "time", "device_encoded"]]
y = df["is_suspicious"]

# Convert time to int (hour only for simplicity)
X["time"] = df["time"].apply(lambda x: int(x.split(":")[0]))

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

def predict_suspicion(location, time_str, device):
    loc_enc = le_location.transform([location])[0] if location in le_location.classes_ else 0
    dev_enc = le_device.transform([device])[0] if device in le_device.classes_ else 0
    hour = int(time_str.split(":")[0])
    X_new = [[loc_enc, hour, dev_enc]]
    prediction = model.predict(X_new)[0]
    return prediction

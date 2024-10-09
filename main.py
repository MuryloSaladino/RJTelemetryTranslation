import pandas as pd
import numpy as np

treated_df = pd.DataFrame()
df = pd.read_csv("./data/telemetry-rio-5-laps.csv")

# Add timestamp in milliseconds
treated_df["Timestamp(ms)"] = df["timestamp_ms"] - df["timestamp_ms"].iloc[0]

# Add Revolutions Per Minute
treated_df["RPM"] = df["current_engine_rpm"]

# Add position in X
treated_df["Position X"] = df["position_x"]

# Add position in Y
treated_df["Position Y"] = df["position_y"]

# Add position in Z
treated_df["Position Z"] = df["position_z"]

# Add speed in Km/h
treated_df["Speed(Km/h)"] = df["speed"] * 3.6

# Add percentage of fuel left in the tank 
treated_df["Fuel"] = df["fuel"]

# Add torque in Nm
treated_df["Torque"] = df["torque"]

# Add Distance Traveled in meters
treated_df["Distance Traveled"] = df["distance_traveled"]

# Add how much the break is being pressed from 0 to 255
treated_df["Brake Pedal"] = df["brake"]

# Add how much the acceleration is being pressed from 0 to 255
treated_df["Acceleration Pedal"] = df["acceleration"]

# Add whether the car ran over a strip
treated_df["Ran over strip"] = df["wheel_on_rumble_strip_front_left"] | df["wheel_on_rumble_strip_front_right"] | df["wheel_on_rumble_strip_rear_left"] | df["wheel_on_rumble_strip_rear_right"]

# Add the lap number starting in 0
treated_df["Lap"] = df["lap_number"]

# Add the last lap time
treated_df["Last lap time"] = df["last_lap_time"]

# Add the current lap time in minutes
treated_df["Current lap time(min)"] = df["current_lap_time"] / 60

# Add the current best lap time
treated_df["Best lap time"] = df["best_lap_time"]

# Add the current gear
treated_df["Gear"] = df["gear"]

# Add whether the gear was changed
df["previous_gear"] = df["gear"].shift(1);
treated_df["Changed Gear"] = df["gear"] != df["previous_gear"]

# Add the steer from -127(left) to 127(right)
treated_df["Steering Wheel Movement"] = df["steer"]

# Add car acceleration in m/s²
df["previous_speed"] = df["speed"].shift(1);
df["two_previous_speed"] = df["speed"].shift(2);
df["previous_timestamp"] = df["timestamp_ms"].shift(1);
df["two_previous_timestamp"] = df["timestamp_ms"].shift(2);

def calculate_acceleration(row):
    if row["timestamp_ms"] == row["previous_timestamp"]:
        return 0;

    if row["previous_timestamp"] == row["two_previous_timestamp"]:
        return (row["speed"] - row["two_previous_speed"]) / (row["timestamp_ms"] - row["two_previous_timestamp"]) * 1000
    
    return (row["speed"] - row["previous_speed"]) / (row["timestamp_ms"] - row["previous_timestamp"]) * 1000

treated_df["Acceleration(m/s²)"] = df.apply(calculate_acceleration, axis=1)

# Add time in minutes
treated_df["Time in minutes"] = treated_df["Timestamp(ms)"] / 60000


# Add state to use as label in map
conditions = [
    treated_df["Ran over strip"],
    treated_df["Changed Gear"],
    treated_df["Speed(Km/h)"] >= 200,
    (treated_df["Speed(Km/h)"] >= 100) & (treated_df["Speed(Km/h)"] < 200),
]
choices = [
    "Running over rumble strips",
    "Changing gear",
    "> 200 Km/h",
    "> 100 Km/h",
]
treated_df['Car Condition'] = np.select(conditions, choices, default='< 100 Km/h')


treated_df.to_csv("./data/treated-datasheet.csv", decimal=",", sep=";")

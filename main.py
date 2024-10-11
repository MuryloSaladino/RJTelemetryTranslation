import pandas as pd
import numpy as np
import math

treated_df = pd.DataFrame()
df = pd.read_csv("./data/telemetry-rio-5-laps.csv")

# Add timestamp in milliseconds
treated_df["Timestamp(ms)"] = df["timestamp_ms"] - df["timestamp_ms"].iloc[0]

# Add Revolutions Per Minute
treated_df["RPM"] = df["current_engine_rpm"]

# Add Coordinates
theta = math.radians(30)

treated_df["Position X"] = (df["position_x"] * math.cos(theta)) - (df["position_z"] * math.sin(theta))
treated_df["Position Y"] = (df["position_x"] * math.sin(theta)) + (df["position_z"] * math.cos(theta))
treated_df["Position Z"] = df["position_y"]

# treated_df["Position X"] = df["position_x"]
# treated_df["Position Y"] = df["position_z"]
# treated_df["Position Z"] = df["position_y"]

# Add speed in Km/h
treated_df["Speed(Km/h)"] = df["speed"] * 3.6

# Add percentage of fuel left in the tank 
treated_df["Fuel"] = df["fuel"]

# Add percentage of fuel wasted for lap
df["last_lap"] = df["lap_number"].shift(1);
df["new_lap"] = df["lap_number"] != df["last_lap"]

initial_fuel = 0.0
df["lap_wasted_fuel"] = 0.0

for i, row in df.iterrows():
    if row["new_lap"]:
        initial_fuel = row["fuel"]
    df.at[i, "lap_wasted_fuel"] = initial_fuel - row["fuel"]

treated_df["Wasted Fuel per Lap"] = df["lap_wasted_fuel"]

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
# df["previous_speed"] = df["speed"].shift(1)
# treated_df["Acceleration(m/s²)"] = (df["speed"] - df["previous_speed"]) / (df["since_last_ns"] / (10**9))

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

# Add Speed Range
treated_df["Speed Range"] = (treated_df["Speed(Km/h)"] // 40) * 40

# Add car acceleration in m/s² V2
treated_df['Race Time(s)'] = df['current_race_time'].apply(lambda x: int(x))
treated_df["speed"] = df["speed"]
df_per_second = treated_df.groupby('Race Time(s)').agg({'speed': 'mean'}).reset_index()
df_per_second['Acceleration(m/s²)'] = df_per_second['speed'].diff()

treated_df = pd.merge(treated_df, df_per_second[['Race Time(s)', 'Acceleration(m/s²)']], on='Race Time(s)', how='left')
treated_df.fillna(0, inplace=True)

# Add Pedal State
conditions = [
    df["brake"] > 126,
    df["acceleration"] > 50
]
choices = ["Brake", "Gas"]

treated_df["Pedal State"] = np.select(conditions, choices, default='None')

# Write final CSV
treated_df.to_csv("./data/treated-datasheet.csv", decimal=",", sep=";")

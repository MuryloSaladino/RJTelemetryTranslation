import pandas as pd
import numpy as np
import math

treated_df = pd.DataFrame()
df = pd.read_csv("./data/telemetry-rio-5-laps.csv")

df = df.loc[df["distance_traveled"] > 0].reset_index()

# Add timestamp in milliseconds
treated_df["Timestamp(ms)"] = df["timestamp_ms"] - df["timestamp_ms"].iloc[0]

# Add Revolutions Per Minute
treated_df["RPM"] = df["current_engine_rpm"]

# Add Coordinates
# Vertical Version:
# theta = math.radians(30)
# treated_df["Position X"] = (df["position_x"] * math.cos(theta)) - (df["position_z"] * math.sin(theta))
# treated_df["Position Y"] = (df["position_x"] * math.sin(theta)) + (df["position_z"] * math.cos(theta))
# treated_df["Position Z"] = df["position_y"]
# Horizontal version:
treated_df["Position X"] = df["position_x"]
treated_df["Position Y"] = df["position_z"]
treated_df["Position Z"] = df["position_y"]

# Add speed in km/h
treated_df["Speed(km/h)"] = df["speed"] * 3.6

# Add percentage of fuel left in the tank 
treated_df["Fuel"] = df["fuel"]

# Add percentage of fuel wasted for lap
df["last_lap"] = df["lap_number"].shift(1)
df["new_lap"] = df["lap_number"] != df["last_lap"]

# Add the lap number starting in 0
treated_df["Lap"] = df["lap_number"]

# Add wasted fuel per lap
df["lap_initial_fuel"] = df.groupby("lap_number")["fuel"].transform("first")
treated_df["Wasted Fuel per Lap"] = df["lap_initial_fuel"] - treated_df["Fuel"]

# Add lap wasted fuel
treated_df["Lap Wasted Fuel"] = treated_df.groupby("Lap")["Wasted Fuel per Lap"].transform("last")

# Add the last lap time
treated_df["Last lap time"] = df["last_lap_time"]

# Add the current lap time in minutes
treated_df["Current lap time(min)"] = df["current_lap_time"] / 60

# Add lap time
treated_df["Lap Time(min)"] = treated_df.groupby("Lap")["Current lap time(min)"].transform("last")

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

# Add the current best lap time
treated_df["Best lap time"] = df["best_lap_time"]

# Add the current gear
treated_df["Gear"] = df["gear"]

# Add whether the gear was changed
df["previous_gear"] = df["gear"].shift(1);
treated_df["Changed Gear"] = df["gear"] != df["previous_gear"]

# Add the steer from -127(left) to 127(right)
treated_df["Steering Wheel Movement"] = df["steer"]

# Add time in minutes
treated_df["Time in minutes"] = treated_df["Timestamp(ms)"] / 60000

# Add state to use as label in map
conditions = [
    treated_df["Ran over strip"],
    treated_df["Changed Gear"],
    treated_df["Speed(km/h)"] >= 200,
    (treated_df["Speed(km/h)"] >= 100) & (treated_df["Speed(km/h)"] < 200),
]
choices = [
    "Running over rumble strips",
    "Changing gear",
    "> 200 km/h",
    "> 100 km/h",
]
treated_df['Car Condition'] = np.select(conditions, choices, default='< 100 km/h')

# Add Speed Range
treated_df["Speed Range"] = (treated_df["Speed(km/h)"] // 40) * 40

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

# Add Wheel Rotation
treated_df["Wheel Rotation Front-Left"] = df["wheel_rotation_speed_front_left"]
treated_df["Wheel Rotation Front-Right"] = df["wheel_rotation_speed_front_right"]
treated_df["Wheel Rotation Rear-Left"] = df["wheel_rotation_speed_rear_left"]
treated_df["Wheel Rotation Rear-Right"] = df["wheel_rotation_speed_rear_right"]

# Add Tire Temperature
def fahrenheit_to_kelvin(f):
    return 273.5 + ((f - 32.0) * (5.0/9.0)) 

treated_df["Tire Temperature Front-Left"] = fahrenheit_to_kelvin(df["tire_temp_front_left"])
treated_df["Tire Temperature Front-Right"] = fahrenheit_to_kelvin(df["tire_temp_front_right"])
treated_df["Tire Temperature Rear-Left"] = fahrenheit_to_kelvin(df["tire_temp_rear_left"])
treated_df["Tire Temperature Rear-Right"] = fahrenheit_to_kelvin(df["tire_temp_rear_right"])

# Add Race Section
df["lap_distance_traveled"] = df.groupby("lap_number")["distance_traveled"].transform("first")
df["lap_distance_traveled"] = treated_df["Distance Traveled"] - df["lap_distance_traveled"]

conditions = [
    df["lap_distance_traveled"] <= 450,
    df["lap_distance_traveled"] <= 950,
    df["lap_distance_traveled"] <= 1150,
    df["lap_distance_traveled"] <= 1700,
    df["lap_distance_traveled"] <= 2250,
    df["lap_distance_traveled"] <= 3000,
    df["lap_distance_traveled"] <= 3600,
    df["lap_distance_traveled"] <= 4100,
    df["lap_distance_traveled"] <= 4400,
    df["lap_distance_traveled"] <= 4600,
    df["lap_distance_traveled"] <= 5250,
    df["lap_distance_traveled"] <= 5550,
]
choices = [
    "1. Start",
    "2. Long Curve 1",
    "3. Right Angle Curve",
    "4. Straightaway 1",
    "5. C Curve",
    "6. Nose Curve",
    "7. Reflect Curve",
    "8. Superman Curve",
    "9. Superman Straightaway",
    "10. Pre-Longway Curve",
    "11. Longway",
    "12. Tip of the Iceberg"
]
treated_df["Race Section"] = np.select(conditions, choices, default='Final Curve')


# Add Car Strengh Vectors
treated_df["Yaw"] = df["yaw"]
treated_df["Pitch"] = df["pitch"]
treated_df["Roll"] = df["roll"]

# Write final CSV
treated_df.to_csv("./data/treated-datasheet.csv", decimal=",", sep=";")

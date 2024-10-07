import pandas as pd

treated_df = pd.DataFrame()
df = pd.read_csv("./data/telemetry-rio-5-laps.csv")

treated_df["Timestamp(ms)"] = df["timestamp_ms"] - df["timestamp_ms"].iloc[0]

treated_df["RPM"] = df["current_engine_rpm"]

treated_df["Position X"] = df["position_x"]
treated_df["Position Y"] = df["position_y"]
treated_df["Position Z"] = df["position_z"]

treated_df["Speed(Km/h)"] = df["speed"] * 3.6

treated_df["Fuel"] = df["fuel"]
treated_df["Torque"] = df["torque"]

treated_df["Distance Traveled"] = df["distance_traveled"]

treated_df["Brake Pedal"] = df["brake"]
treated_df["Acceleration Pedal"] = df["acceleration"]

treated_df["Ran over strip"] = df["wheel_on_rumble_strip_front_left"] | df["wheel_on_rumble_strip_front_right"] | df["wheel_on_rumble_strip_rear_left"] | df["wheel_on_rumble_strip_rear_right"]

treated_df["Lap"] = df["lap_number"]

treated_df["Best lap time"] = df["best_lap_time"]
treated_df["Current lap time"] = df["current_lap_time"]

df["previous_gear"] = df["gear"].shift(1);

treated_df["Gear"] = df["gear"]
treated_df["Changed Gear"] = df["gear"] != df["previous_gear"]

treated_df.to_csv("./data/treated-datasheet.csv")

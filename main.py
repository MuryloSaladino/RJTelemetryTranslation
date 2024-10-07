import pandas as pd

treated_df = pd.DataFrame()
df = pd.read_csv("./data/telemetry-rio-5-laps.csv")

treated_df["timestamp_ms"] = df["timestamp_ms"] - df["timestamp_ms"].iloc[0]

treated_df["rpm"] = df["current_engine_rpm"]

treated_df["position_x"] = df["position_x"]
treated_df["position_y"] = df["position_y"]
treated_df["position_z"] = df["position_z"]

treated_df["speed_kmh"] = df["speed"] * 3.6

treated_df["fuel"] = df["fuel"]
treated_df["torque"] = df["torque"]

treated_df["distance_traveled"] = df["distance_traveled"]

treated_df["brake_pedal"] = df["brake"]
treated_df["acceleration_pedal"] = df["acceleration"]

treated_df["gear"] = df["gear"]

treated_df["ran_over_strip"] = df["wheel_on_rumble_strip_front_left"] | df["wheel_on_rumble_strip_front_right"] | df["wheel_on_rumble_strip_rear_left"] | df["wheel_on_rumble_strip_rear_right"]

treated_df["lap"] = df["lap_number"]

treated_df["best_lap_time"] = df["best_lap_time"]
treated_df["current_lap_time"] = df["current_lap_time"]

# treated_df["changed_gear"] = df["gear"]

treated_df.to_csv("./data/treated-datasheet.csv")

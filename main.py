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

treated_df.to_csv("./data/treated-datasheet.csv")


# 'Unnamed: 0', 'since_last_ns', 'timestamp_ms', 'current_engine_rpm',
# 'wheel_rotation_speed_front_left', 'wheel_rotation_speed_front_right',
# 'wheel_rotation_speed_rear_left', 'wheel_rotation_speed_rear_right',
# 'wheel_on_rumble_strip_front_left', 'wheel_on_rumble_strip_front_right',
# 'wheel_on_rumble_strip_rear_left', 'wheel_on_rumble_strip_rear_right',
# 'wheel_in_puddle_depth_front_left', 'wheel_in_puddle_depth_front_right',
# 'wheel_in_puddle_depth_rear_left', 'wheel_in_puddle_depth_rear_right',
# 'tire_slip_rotation_front_left', 'tire_slip_rotation_front_right',
# 'tire_slip_rotation_rear_left', 'tire_slip_rotation_rear_right',
# 'tire_slip_angle_front_left', 'tire_slip_angle_front_right',
# 'tire_slip_angle_rear_left', 'tire_slip_angle_rear_right',
# 'tire_combined_slip_front_left', 'tire_combined_slip_front_right',
# 'tire_combined_slip_rear_left', 'tire_combined_slip_rear_right',
# 'tire_temp_front_left', 'tire_temp_front_right', 'tire_temp_rear_left',
# 'tire_temp_rear_right', 'normalized_suspension_travel_front_left',
# 'normalized_suspension_travel_front_right',
# 'normalized_suspension_travel_rear_left',
# 'normalized_suspension_travel_rear_right',
# 'suspension_travel_meters_front_left',
# 'suspension_travel_meters_front_right',
# 'suspension_travel_meters_rear_left',
# 'suspension_travel_meters_rear_right', 'position_x', 'position_y',
# 'position_z', 'acceleration_x', 'acceleration_y', 'acceleration_z',
# 'velocity_x', 'velocity_y', 'velocity_z', 'angular_velocity_x',
# 'angular_velocity_y', 'angular_velocity_z', 'yaw', 'pitch', 'roll',
# 'speed', 'power', 'torque', 'boost', 'fuel', 'distance_traveled',
# 'acceleration', 'brake', 'clutch', 'handbrake', 'gear', 'steer',
# 'lap_number', 'best_lap_time', 'last_lap_time', 'current_lap_time',
# 'current_race_time', 'race_position'
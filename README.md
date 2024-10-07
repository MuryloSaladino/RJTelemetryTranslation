# RJTelemetryTranslation

### Python script to treat a race datasheet

### [Datasheet link](https://www.kaggle.com/datasets/alexhexan/fm7-rio-de-janeiro-race-telemetry)



## Data dictionary


### Treated data

|   **Column**   | **Name in the datasheet** |       **Data type**       |                         **Description**                        |
|:--------------:|:-------------------------:|:-------------------------:|:--------------------------------------------------------------:|
|  timestamp_ms  |       "timestamp_ms"      |            Int            | Amount of time in miliseconds from the moment the race started |
|       rpm      |    "current_engine_rpm"   |            Int            |           Rotations per minute at that point of time           |
| ran_over_strip |     Calculated Column     |            Bool           |  True if any of the four wheels is going through rumble strips |
|   position_x   |        "position_x"       |           Float           |                Position of the car in the X axis               |
|   position_y   |        "position_y"       |           Float           |                Position of the car in the Y axis               |
|      speed     |          "speed"          | Float / Meters per second |                        Speed of the car                        |
|                |                           |                           |                                                                |
# WAVE ROVER - ESP32 Firmware JSON Communication Protocol

## Development Setup

- **Robot**: Waveshare Rover  
- **ESP32 Firmware Version**: 10.56 (obtained in OLED screen)
- **Controller**: Raspberry Pi 4B (Raspberry Pi OS, 64-bit)  
- **Connection**: Serial via GPIO (physical port)  

---

## Motion Command Set

### CMD_ROS_CTRL — ROS-Like Motion Control

- **Type**: Robot Movement  
- **ID**: `"T": 13`

This command emulates ROS2-style mobile robot motion commands.

```json
{"T": 13, "X": [float], "Z": [float]}
```

- `X`: Linear velocity in meters/second (m/s)  
- `Z`: Angular velocity in radians/second (rad/s)

> [!WARNING]
> This command is originally designed for UGV01 with encoders, but it **also works on motors without encoders**.

**Example**:
```json
{"T": 13, "X": 0.1, "Z": 0.3}
```
Sets the robot to move forward at 0.1 m/s with a rotational speed of 0.3 rad/s.

---

### CMD_SPEED_CTRL — Wheel Speed Control

- **Type**: Robot Movement  
- **ID**: `"T": 1`

Controls the rotational speed and direction of the left and right wheels. No encoders required.

```json
{"T": 1, "L": [float], "R": [float]}
```

- `L`: Left wheel speed (range: -0.5 to +0.5)  
- `R`: Right wheel speed (range: -0.5 to +0.5)  
  - Positive values: forward  
  - Negative values: backward  

**Example**:
```json
{"T": 1, "L": 0.5, "R": 0.25}
```
Sets left wheel to 100% speed forward, right wheel to 50% speed forward.

---

### CMD_PWM_INPUT — Direct Motor PWM Control

- **Type**: Robot Movement  
- **ID**: `"T": 11`

Directly sets the PWM values for the motors.

```json
{"T": 11, "L": [int], "R": [int]}
```

- `L`: PWM for left motor (range: -255 to +255)  
- `R`: PWM for right motor (range: -255 to +255)  
  - Positive values: forward  
  - Negative values: backward  

**Example**:
```json
{"T": 11, "L": 89, "R": -164}
```
Left motor runs forward with PWM 89, right motor runs backward with PWM 164.

> [!WARNING]
> Low PWM values may not rotate the motor due to poor low-speed performance of DC gear motors.

> [!NOTE]
> Use this command only for debugging. For normal movement, prefer `CMD_SPEED_CTRL`.

---

## Sensor Command Set

### Get IMU Data

Use the following command to obtain various IMU sensor readings:

```json
{"T": 126}
```

Returns:

1. Heading angle  
2. Geomagnetic field  
3. Acceleration  
4. Attitude (orientation)  
5. Temperature  
6. (Other values - to be documented)  

---

## Communication Mode

### Continuous Feedback Mode

- Disable feedback (default):
```json
{"T": 131, "cmd": 0}
```

- Enable feedback:
```json
{"T": 131, "cmd": 1}
```

- **When disabled**: Information is sent only in response to queries.  
- **When enabled**: Information is sent periodically without a query.

> [!IMPORTANT]
> This mode is essential for integration with a ROS-based system.

---

### Serial Port Echo

When enabled, all commands sent to the ESP32 will also appear in the serial console.

- Turn off echo (default):
```json
{"T": 143, "cmd": 0}
```

- Turn on echo:
```json
{"T": 143, "cmd": 1}
```

---


---

## IMU Data Units and Interpretation

When using command `{"T":126}`, the ESP32 with Waveshare Rover returns various sensor data. Below are the typical units and interpretation guidelines for each sensor output.

| Measurement Type        | Unit                                | Notes                                                                                                  |
|-------------------------|-------------------------------------|--------------------------------------------------------------------------------------------------------|
| **Heading Angle**       | Degrees (°)                         | Yaw angle relative to magnetic north.                                                                 |
| **Geomagnetic Field**   | Microtesla (µT)                     | Magnetometer readings; values may require calibration.                                                 |
| **Acceleration**        | g (gravitational acceleration)      | Raw values; e.g., if sensitivity is 16384 LSB/g, divide raw value by 16384.                            |
| **Attitude (Orientation)** | Degrees (°)                     | Includes roll, pitch, and yaw orientation angles.                                                     |
| **Temperature**         | Degrees Celsius (°C)                | Ambient temperature from onboard sensor.                                                               |
| **Other Sensor Readings** | Varies                            | May include pressure (hPa), altitude (m), or gyroscope data (°/s) depending on firmware capabilities.  |

### Notes on Conversion

- **Acceleration**: If sensitivity is 16384 LSB/g, convert by:  
  ```raw_value / 16384.0 = acceleration in g```

- **Gyroscope**: For 32.8 LSB/(°/s) sensitivity, convert by:  
  ```raw_value / 32.8 = angular velocity in °/s```

- **Magnetometer**: For typical 0.15 µT/LSB, convert by:  
  ```raw_value * 0.15 = field strength in µT```

> [!NOTE]
> The exact fields and scaling may vary depending on firmware version. (Confirmed version: **10.56**)

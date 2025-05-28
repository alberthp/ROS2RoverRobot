# serial_simple_teleopctrl.py

This script enables manual teleoperation control of a robot via keyboard input, sending commands over a serial port in JSON format. It supports real-time adjustment of linear (X) and angular (Z) velocities using arrow keys, with a spacebar command to stop the robot and escape to exit. The script opens the specified serial port, continuously listens for keyboard events, and sends updated motion commands at a regular interval. It also reads and displays incoming serial data for feedback.

Communication with ESP32 controller is based on the JSON communication based defined by [Waveshare](https://www.waveshare.com/wiki/WAVE_ROVER)

ROS Control - CMD_ROS_CTRL
```bash
{"T":13,"X":0.1,"Z":0.3}
```
Instruction using the standard movement instruction of ROS. The X value is the moving linear velocity in m/s and the Z value is the steering angular velocity in rad/s.


## Usage

```bash
python serial_simple_teleopctrl.py <serial_port>
```

for Serial GPIO port instance:
```bash
python3 serial_simple_ctrl.py /dev/ttyS0
```


## Keyboard Controls

- **Up Arrow**: Increase forward speed (X)
- **Down Arrow**: Increase backward speed (X)
- **Left Arrow**: Increase left turn (Z)
- **Right Arrow**: Increase right turn (Z)
- **Spacebar**: Stop robot (X=0, Z=0)
- **Esc**: Exit program

## Dependencies

- [pyserial](https://pypi.org/project/pyserial/)
- [pynput](https://pypi.org/project/pynput/)

---

## Python Virtual Environment Setup and Usage Guide

1. **Create a virtual environment (venv) in the current directory:**
    ```bash
    python3 -m venv venv
    ```

2. **Activate the virtual environment:**

    - On Linux/macOS:
        ```bash
        source venv/bin/activate
        ```
    - On Windows:
        ```bash
        venv\Scripts\activate
        ```

3. **Install required dependencies:**
    ```bash
    pip install pyserial pynput
    ```

4. **Run the script (while venv is activated):**
    ```bash
    python serial_simple_teleopctrl.py <serial_port>
    ```

5. **Deactivate the virtual environment when done:**
    ```bash
    deactivate
    ```
for Serial GPIO port instance:
```bash
python3 serial_simple_ctrl.py /dev/ttyS0
```

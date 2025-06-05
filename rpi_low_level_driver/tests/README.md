# Raspberry Pi - ESP32 Communication Tests

This directory contains Python scripts designed to test the low-level serial communication and JSON protocol between the **Raspberry Pi** and the **ESP32 firmware** on the Waveshare Rover robot. These tests are independent of the ROS2 system and focus solely on direct RPi-ESP32 interaction.

---

## 1. Setup

To run these tests, you'll need to set up a Python virtual environment and install the necessary dependencies.

1.  **Navigate to this directory:**
    ```bash
    cd /path/to/your/robot_project/rpi_low_level_driver/tests/
    ```

2.  **Create a Python Virtual Environment:**
    This creates a dedicated environment to avoid conflicts with your system's Python packages.
    ```bash
    python3 -m venv venv
    ```

3.  **Activate the Virtual Environment:**
    You'll need to activate this environment every time you want to run the tests.
    ```bash
    source venv/bin/activate
    ```
    (On Windows, it might be `.\venv\Scripts\activate`)

4.  **Install Dependencies:**
    Install all required Python libraries listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```
    *Ensure your `requirements.txt` file exists in this directory and lists necessary packages like `pyserial`.*

---

## 2. Running the Tests

Once your virtual environment is set up and activated, you can run individual test scripts.

**Important:** Before running any test, ensure the ESP32 is powered on and connected to the Raspberry Pi's serial GPIOs. You may also need to adjust the serial port configuration in `rpi_low_level_driver/config/rpi_serial_config.yaml` if it's not `/dev/ttyS0` or similar.

To run a specific test, use the Python interpreter from your activated virtual environment:

```bash
python <test_script_name.py>

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

#Raspberry Pi middle-level control unit

This tutorial is oriented to provide instructions to set up the Raspberry Pi and use it as middle-level control unit.

## Platform components
This is the list of components, OS and minimum software list used for the development platform

* Host: Raspberry Pi 5 8GB
* Hat for SSD: Waveshare NVMe PCIe To M.2 Hat+ Adapter with PoE, Compatible with Raspberry Pi 5, Supports NVMe Drive Protocol 2230/2242 M.2 Solid State Drive and 802.3af/at Network Standard, with Cooling Fan
* SSD unit: SAMSUNG PM9B1 SSD 128 GB M.2 PCI Express 4.0 NVMe 2230 MZ9L4128HCHQ Solid State Drive OEM Bulk
* OS: Raspberry Pi OS "Bookworm" (Debian 12) for 64bits

## Raspberry Pi setup

### Setting a remote acces via VNC (Raspberry Pi Connect)
Why Remote Desktop (VNC) for Raspberry Pi?: Setting up remote desktop access, like through VNC or Raspberry Pi Connect, is useful for debugging the code and monitor execution inside Raspberry Pi in the field without needing physical cables and a desktop computer. 


### Table of Contents

1.  [Prerequisites](#1-prerequisites)
2.  [Initial OS Setup](#2-initial-os-setup)
3.  [Configure Boot & Wayland](#3-configure-boot--wayland)
4.  [Install & Configure Raspberry Pi Connect](#4-install--configure-raspberry-pi-connect)
5.  [Verify Setup](#5-verify-setup)
6.  [Access Your Pi Remotely](#6-access-your-pi-remotely)
7.  [Troubleshooting](#7-troubleshooting)

---

### 1. Prerequisites

Before you begin, ensure you have:

* **Raspberry Pi 5**
* **Raspberry Pi OS Bookworm** (the full **Desktop** version, not "Lite") installed on an SD card or SSD.
* A stable **internet connection** for your Raspberry Pi.
* A **Raspberry Pi ID** account. If you don't have one, create it at [https://www.raspberrypi.com/account/](https://www.raspberrypi.com/account/).
* Initial access to your Raspberry Pi (via monitor/keyboard or SSH if already configured).

---

### 2. Initial OS Setup

It's always a good practice to ensure your system is up to date after a fresh install.

1.  Open a **terminal** on your Raspberry Pi.
2.  Update your package lists and upgrade all installed packages:
    ```bash
    sudo apt update
    sudo apt full-upgrade -y
    sudo reboot
    ```

---

### 3. Configure Boot & Wayland

This step ensures your Pi boots directly into the graphical desktop, which is essential for Raspberry Pi Connect to share the display. We'll also confirm the Wayland compositor setup.

1.  Open a **terminal** on your Raspberry Pi.
2.  Run `raspi-config`:
    ```bash
    sudo raspi-config
    ```
3.  Navigate using arrow keys and select options:
    * Go to **3 System Options**.
    * Select **S5 Boot / Auto Login**.
    * Choose **B2 Desktop Autologin** (this ensures the `pi` user automatically logs into the desktop). Press `Enter`.
    * Go to **6 Advanced Options**.
    * Select **A6 Wayland**.
    * Ensure **W2 Wayfire** is selected. Press `Enter`.
    * Go to **3 Interface Options**.
    * Select **I3 VNC**.
    * Choose **Yes** to enable VNC (on Bookworm, this primarily configures and activates `wayvnc`, which `rpi-connect` uses). Press `Enter`.
4.  Select **Finish** and choose **Yes** to reboot your Raspberry Pi.

---

### 4. Install & Configure Raspberry Pi Connect

Now we'll install the remote access software and link it to your Raspberry Pi ID.

1.  After your Pi reboots, open a **terminal**.
2.  Install the `rpi-connect` and `wayvnc` packages:
    ```bash
    sudo apt install rpi-connect wayvnc
    ```
    *Note: While `raspi-config` enables VNC, explicitly installing `wayvnc` ensures it's present for `rpi-connect`.*
3.  **Ensure `wayvnc.service` is enabled and active for your user.** This was a common pitfall:
    ```bash
    systemctl --user enable wayvnc.service
    systemctl --user start wayvnc.service
    ```
4.  **Link your Raspberry Pi to your Raspberry Pi ID:**
    * Open the **"Raspberry Pi Connect" application** from the Raspberry Pi's desktop menu (usually under "Internet" or "Accessories").
    * Log in using your **Raspberry Pi ID** (email and password).
    * Provide a descriptive **device name** (e.g., "MyPi5Lab", "Rover01").
    * Click **"Connect"** or **"Link"**.
5.  **Restart the `rpi-connect` service** to ensure it picks up the WayVNC setup:
    ```bash
    systemctl --user restart rpi-connect.service
    ```
    *Optional: You can perform another full reboot (`sudo reboot`) here for good measure.*

---

### 5. Verify Setup

Before attempting remote access, confirm that Raspberry Pi Connect sees all the necessary components.

1.  After the last reboot (if performed), open a **terminal** on your Raspberry Pi.
2.  Run the `rpi-connect doctor` command:
    ```bash
    rpi-connect doctor
    ```
3.  **Expected Output:** You should see a `✓` next to all items, especially:
    ```
    ✓ Screen sharing services enabled and active
    ✓ Wayland compositor available
    ```
    If you see any `✗`, double-check the previous steps, especially the `raspi-config` settings and the `systemctl --user enable/start wayvnc.service` commands.

---

### 6. Access Your Pi Remotely

Now that everything is configured, you can access your Raspberry Pi from any device with a modern web browser.

1.  On your **remote device** (computer, tablet, smartphone), open a web browser.
2.  Navigate to the Raspberry Pi Connect portal:
    [https://connect.raspberrypi.com/](https://connect.raspberrypi.com/)
3.  **Log in** with your Raspberry Pi ID.
4.  You'll see a list of your linked Raspberry Pi devices. Click on the **name of your Pi** (e.g., "Rover01").
5.  You should now see the **"Desktop"** option available. Click it to view and control your Pi's graphical desktop environment. The "Terminal" option will also be available for command-line access.

---

### 7. Troubleshooting

If you encounter issues, review these common problems and solutions:

* **"Desktop" option is greyed out or missing:**
    * Ensure your Raspberry Pi OS is the **Desktop version**, not Lite.
    * Verify **`raspi-config` -> `Boot / Auto Login`** is set to **`B2 Desktop Autologin`**.
    * Check `rpi-connect doctor` output for `✗ Screen sharing services enabled and active`.
    * Confirm **`wayvnc` is installed** (`apt list --installed | grep wayvnc`).
    * Verify **`wayvnc.service` is active** for your user (`systemctl --user status wayvnc.service` should show `active (running)`). If not, run `systemctl --user enable wayvnc.service` and `systemctl --user start wayvnc.service`.
    * Restart the `rpi-connect` service: `systemctl --user restart rpi-connect.service`.
* **"No journal files were found." error with `journalctl --user`:**
    * Ensure `loginctl enable-linger $(whoami)` is set for your user.
* **Network/Heartbeat Errors (`ERRO Error sending heartbeat...`):**
    * This usually indicates a DNS or general network connectivity issue on your Pi. Ensure your Pi has stable internet access and correct DNS server configurations. While often not blocking the remote shell, it can affect overall reliability.

If you continue to experience problems, provide the full output of `rpi-connect doctor` and `systemctl --user status rpi-connect.service` for further diagnosis.


## Test Programs 

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

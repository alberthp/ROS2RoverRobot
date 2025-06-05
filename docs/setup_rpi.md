# Guide to configure the Raspberry Pi 

This guide includes:

# Table of Contents
- [System configuration](#system-configuration)
- [Basic program using JSON based Waveshare protocol emulating ROS2 movement command](#basic-driving-program)


## 1. System configuration 

Subsetion for correct OS, basic developing tools installation and configuration

### Hardware
* Raspberry Pi 4b with 8gB
* microSD Samsung 32GB EVO Plus

## Installing OS
This guide uses Raspberry Pi OS:
* Desktop version
* Release date: May 13th 2025
* System: 64-bit
* Kernel version: 6.12, Debian version: 12 (bookworm)

The OS is installed into a SMD card using the [Raspberry Pi Imager](https://www.raspberrypi.com/software/). The installation has used the [Windows version](https://downloads.raspberrypi.org/imager/imager_latest.exe)

## Communication ports

### GPIO serial port 
This port is used for communications between Raspberry Pi 4b and ESP32 robot board using the mini UART (ttyS0). This is connected to the GPIO pins 14 (TX) and 15 (RX). By default, this is often used for Bluetooth on the Pi 4B.

Steps to open the port:

1. Disable Serial Console (if enabled):
    * Open Raspberry Pi configuration tool: `sudo raspi-config`
    * Navigate to 3 Interface Options.
    * Select P6 Serial Port.
    * When asked "Would you like a login shell to be accessible over serial?", select **No**.
    * When asked "Would you like the serial port hardware to be enabled?", select **Yes**.
    * Exit raspi-config and reboot the Pi: `sudo reboot`

2. Swaping UARTs if necessary (ensure UART is mapped to the GPIO pins)
    * Edit `config.txt to` Configure UART: `sudo nano /boot/firmware/config.txt`
    * Add or modify the following lines:
        * Enable UART: `enable_uart = 1`
        * ensure these lines are NOT present or are commented out:
            * `# dtoverlay=disable-bt   <-- DO NOT USE THIS, it disables Bluetooth`
            * `# dtoverlay=miniuart-bt  <-- DO NOT USE THIS, it swaps ttyAMA0 and ttyS0`
    * Save file and reboot the Pi:  `sudo reboot`

3. Verify the Serial Port and Bluetooth:
    * Check Serial Port: confirm which device serial0 points to `ls -l /dev/serial*` -> `lrwxrwxrwx 1 root root (other info) /dev/serial0 -> ttyS0`
    * Check Bluetooth Status: `sudo systemctl status bluetooth` -> `Active: active (running)`


## 2. Basic driving program 
using JSON based Waveshare protocol emulating ROS2 movement command.
For detailed setup instructions for the Raspberry Pi, see [RaspberryPiSetup/README.md](RaspberryPiSetup/README.md).

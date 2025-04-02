# Introduction
This document is oriented as a guide to install ROS2 in [Wave Rover](https://www.waveshare.com/product/robotics/mobile-robots/raspberry-pi-robots/wave-rover.htm?sku=25377) Onboard ESP32 Module.

## Requirements

### Install ESP32 Add-on in Arduino IDE 

#### Installation procedure

1. Install [Arduino IDE](https://www.arduino.cc/en/software)
2. Install ESP32 Add-on in Arduino IDE
   1. Arduino IDE, go to File -> Preferences
   2. Enter the following board manager into the “Additional Board Manager URLs” field: https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json ![Install Additional board](./imgs/ArduinoIDEAddBoard.png)
   3. Open Boards Manager. Go to Tools -> Board -> Boards Manager…
   4. Search for ESP32 and select esp32 by Espressif Systems  ![Install Additional board](./imgs/ArduinoIDEUseBoard.png)

#### Testing installation

1. Plug the ESP32 board to computer. 
2. Open Arduino IDE 
3. Select your Board in Tools > Board menu (in my case it’s the DOIT ESP32 DEVKIT V1)


https://randomnerdtutorials.com/installing-the-esp32-board-in-arduino-ide-windows-instructions/
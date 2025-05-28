"""
serial_simple_teleopctrl.py

This script enables manual teleoperation control of a robot via keyboard input,
sending commands over a serial port in JSON format. It supports real-time
adjustment of linear (X) and angular (Z) velocities using arrow keys, with a
spacebar command to stop the robot and escape to exit. The script opens the
specified serial port, continuously listens for keyboard events, and sends
updated motion commands at a regular interval. It also reads and displays
incoming serial data for feedback.

Usage:
    python serial_simple_teleopctrl.py <serial_port>

Keyboard Controls:
    Up Arrow    - Increase forward speed (X)
    Down Arrow  - Increase backward speed (X)
    Left Arrow  - Increase left turn (Z)
    Right Arrow - Increase right turn (Z)
    Spacebar    - Stop robot (X=0, Z=0)
    Esc         - Exit program

Dependencies:
    - pyserial
    - pynput

-----------
Python Virtual Environment Setup and Usage Guide
-----------

1. Create a virtual environment (venv) in the current directory:
    python3 -m venv venv

2. Activate the virtual environment:
    On Linux/macOS:
        source venv/bin/activate
    On Windows:
        venv\Scripts\activate

3. Install required dependencies:
    pip install pyserial pynput

4. Run the script (while venv is activated):
    python serial_simple_teleopctrl.py <serial_port>

5. Deactivate the virtual environment when done:
    deactivate
"""
import serial
import argparse
import threading
import time
from pynput import keyboard # Import the keyboard module

# Global variables for serial port and movement commands
ser = None
current_x = 0.0
current_z = 0.0
x_increment = 0.05 # Adjust this value for how much X changes per keypress
z_increment = 0.1  # Adjust this value for how much Z changes per keypress
max_speed = 1.0    # Maximum absolute linear speed
max_turn = 5.0     # Maximum absolute angular speed

def read_serial():
    """Reads data from the serial port and prints it."""
    while True:
        try:
            data = ser.readline().decode('utf-8').strip() # .strip() to remove newline characters
            if data:
                print(f"Received: {data}")
        except serial.SerialException as e:
            print(f"Serial read error: {e}")
            break # Exit thread on serial error
        except Exception as e:
            print(f"Error in read_serial: {e}")
            break

def send_command():
    """Sends the current X and Z command to the serial port."""
    global current_x, current_z
    command_str = f'{{"T":13, "X":{current_x:.2f}, "Z":{current_z:.2f}}}'
    try:
        ser.write(command_str.encode() + b'\n')
        #print(f"Sent: {command_str}") # Uncomment for debugging sent commands
    except serial.SerialException as e:
        print(f"Serial write error: {e}")
        # Optionally, handle re-connection or exit
    except Exception as e:
        print(f"Error sending command: {e}")

def on_press(key):
    """Callback function for key press events."""
    global current_x, current_z

    try:
        if key == keyboard.Key.up:
            current_x = min(current_x + x_increment, max_speed)
            print(f"X increased to: {current_x:.2f}")
        elif key == keyboard.Key.down:
            current_x = max(current_x - x_increment, -max_speed) # Allow negative X
            print(f"X decreased to: {current_x:.2f}")
        elif key == keyboard.Key.left:
            current_z = min(current_z + z_increment, max_turn) # Increase Z for left turn (positive Z)
            print(f"Z increased to: {current_z:.2f} (Left turn)")
        elif key == keyboard.Key.right:
            current_z = max(current_z - z_increment, -max_turn) # Decrease Z for right turn (negative Z)
            print(f"Z decreased to: {current_z:.2f} (Right turn)")
        elif key == keyboard.Key.space: # Stop the robot
            current_x = 0.0
            current_z = 0.0
            print("Robot stopped (X=0, Z=0)")
        elif key == keyboard.Key.esc:
            print("Exiting program.")
            return False # Stop listener
    except AttributeError:
        # Handle special keys that don't have a char attribute (e.g., arrows)
        pass

def main():
    """Main function to set up serial communication and keyboard listener."""
    global ser, current_x, current_z

    parser = argparse.ArgumentParser(description='Serial JSON Communication with Keyboard Control')
    parser.add_argument('port', type=str, help='Serial port name (e.g., COM1 or /dev/ttyUSB0)')

    args = parser.parse_args()

    # Initialize serial port
    try:
        ser = serial.Serial(args.port, baudrate=115200, dsrdtr=None)
        ser.setRTS(False)
        ser.setDTR(False)
        print(f"Opened serial port: {args.port}")
    except serial.SerialException as e:
        print(f"Error opening serial port {args.port}: {e}")
        return

    # Start serial reception thread
    serial_recv_thread = threading.Thread(target=read_serial)
    serial_recv_thread.daemon = True # Daemonize thread so it exits when main program exits
    serial_recv_thread.start()

    # Start keyboard listener
    listener = keyboard.Listener(on_press=on_press)
    listener.daemon = True # Daemonize listener
    listener.start()

    print("\nUse Arrow keys to control the robot:")
    print("  Up Arrow: Increase forward speed (X)")
    print("  Down Arrow: Increase backward speed (X)")
    print("  Left Arrow: Increase left turn (Z)")
    print("  Right Arrow: Increase right turn (Z)")
    print("  Spacebar: Stop robot (X=0, Z=0)")
    print("  Esc: Exit program\n")
    print("Initial values: X=0.00, Z=0.00")

    try:
        while True:
            send_command()
            time.sleep(0.1) # Send commands at 10 Hz (every 100ms)
    except KeyboardInterrupt:
        print("Program interrupted by user (Ctrl+C).")
    finally:
        if ser and ser.is_open:
            # Send a stop command before closing
            current_x = 0.0
            current_z = 0.0
            send_command()
            time.sleep(0.1) # Give time for the stop command to be sent
            ser.close()
            print("Serial port closed.")
        print("Exiting program.")

if __name__ == "__main__":
    main()

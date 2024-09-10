from Phidget22.Devices.BLDCMotor import BLDCMotor
from Phidget22.Phidget import *
from pynput.keyboard import Key, Listener
import time

def onAttach(self):
    print("Attached!")

def onDetach(self):
    print("Detached!")

def on_press(key):
    try:
        # Check if 'd' is pressed for positive velocity
        if key.char == 'd':
            print("Positive Velocity")
            elbowMotor.setTargetVelocity(0.2)
        # Check if 'c' is pressed for negative velocity
        elif key.char == 'c':
            print("Negative Velocity")
            elbowMotor.setTargetVelocity(-0.2)
    except AttributeError:
        pass

def on_release(key):
    # Stop the motor when key is released
    elbowMotor.setTargetVelocity(0)
    # You can add a specific key to break the loop and end the program, e.g., pressing 'esc'
    if key == Key.esc:
        return False

def main():
    global elbowMotor
    elbowMotor = BLDCMotor()

    elbowMotor.setDeviceSerialNumber(708023)
    elbowMotor.setHubPort(3)

    elbowMotor.setOnAttachHandler(onAttach)
    elbowMotor.setOnDetachHandler(onDetach)

    elbowMotor.openWaitForAttachment(5000)

    # Listen for keyboard input
    with Listener(on_press=on_press, on_release=on_release) as listener:
        try:
            input("Press Enter to Stop\n")
        except (Exception, KeyboardInterrupt):
            pass
        finally:
            listener.stop()  # Stop listening to the keyboard

    elbowMotor.close()

if __name__ == "__main__":
    main()

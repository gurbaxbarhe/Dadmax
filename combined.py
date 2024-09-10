from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
from Phidget22.Devices.Stepper import *
from roboclaw import Roboclaw
from pynput.keyboard import Key, Listener
from serial import Serial, SerialException
import threading
import time

def onAttach(self):
    print("Dadmax is running!")

def onDetach(self):
    print("Dadmax is not running!")

# Initialize RoboClaw
motor_com_port = 'COM24'
serial_obj = Serial(motor_com_port, 38400)  # Default baudrate for RoboClaw is 38400
rc = Roboclaw(serial_obj) 

# Constants
stepper_position = 10000
stepper_acceleration = 1000
shoulder_elbow_velocity_in = 0.6
wrist_speed = 64
stop = 0

# Controlling the robot manually with keys
def on_press(key):
    try:
        global stepper, shoulderMotor, elbowMotor
        # HEIGHT ADJUSTMENT CONTROL
        if key.char == 'q':
            print("Stepper is moving upward")
            stepper.setTargetPosition(stepper_position)  
        elif key.char == 'a':  
            print("Stepper is moving downward")
            stepper.setTargetPosition(-stepper_position)  
        # SHOULDER CONTROL
        elif key.char == 'w':
            print("Shoulder is moving inward")
            shoulderMotor.setTargetVelocity(shoulder_elbow_velocity_in)
        elif key.char == 's':  
            print("Shoulder is moving outward")
            shoulderMotor.setTargetVelocity(-shoulder_elbow_velocity_in)  
        # ELBOW CONTROL
        elif key.char == 'e':  
            print("Elbow is moving inward")
            elbowMotor.setTargetVelocity(-shoulder_elbow_velocity_in)
        elif key.char == 'd':
            print("Elbow is moving outward")
            elbowMotor.setTargetVelocity(shoulder_elbow_velocity_in)
        elif key.char == 'x':
            print("Elbow and shoulder is moving inward")
            shoulderMotor.setTargetVelocity(shoulder_elbow_velocity_in)
            elbowMotor.setTargetVelocity(-shoulder_elbow_velocity_in)
        elif key.char == 'c':
            print("Elbow and shoulder is moving outward")
            shoulderMotor.setTargetVelocity(-shoulder_elbow_velocity_in)
            elbowMotor.setTargetVelocity(shoulder_elbow_velocity_in)
        # WRIST CONTROL
        elif key.char == 'r':
            print("Wrist is moving outward")
            rc.forward_m1(wrist_speed) 
        elif key.char == 'f':
            print("Wrist is moving inward")
            rc.backward_m1(wrist_speed)  
    except AttributeError:
        pass

def on_release(key):
    global stepper, shoulderMotor, elbowMotor
    # For BLDC motors, setting velocity to 0 is correct for stopping
    shoulderMotor.setTargetVelocity(stop)
    elbowMotor.setTargetVelocity(stop)
    #rc.forward_backward_m1(0)  
    # Escape key to break the loop
    if key == Key.esc:
        return False

def main_motor():
    global elbowMotor, shoulderMotor, stepper

    # Stepper motor initialization
    stepper = Stepper()
    stepper.openWaitForAttachment(1000) 
    stepper.setEngaged(True)

    # Shoulder motor initialization
    shoulderMotor = BLDCMotor()
    shoulderMotor.setDeviceSerialNumber(708023)  # Adjust as needed
    shoulderMotor.setHubPort(4)
    shoulderMotor.setOnAttachHandler(onAttach)
    shoulderMotor.setOnDetachHandler(onDetach)
    shoulderMotor.openWaitForAttachment(5000)

    # Elbow motor initialization
    elbowMotor = BLDCMotor()
    elbowMotor.setDeviceSerialNumber(708023)  # Adjust as needed
    elbowMotor.setHubPort(3)
    elbowMotor.setOnAttachHandler(onAttach)
    elbowMotor.setOnDetachHandler(onDetach)
    elbowMotor.openWaitForAttachment(5000)

    # Keyboard input listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass
    finally:
        listener.stop()  # Ensure listener stops when exiting
        # Clean up devices
        stepper.setEngaged(False)
        stepper.close()
        elbowMotor.close()
        shoulderMotor.close()
        serial_obj.close()  # Close the serial connection to RoboClaw

if __name__ == "__main__":
    main_motor()
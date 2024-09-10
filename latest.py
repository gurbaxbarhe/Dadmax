# Importing libraries 
from Phidget22.Phidget import *
from Phidget22.Devices.BLDCMotor import *
from Phidget22.Devices.Stepper import *
from Phidget22.Devices.VoltageInput import VoltageInput
from roboclaw import Roboclaw
from pynput.keyboard import Key, Listener
from serial import Serial, SerialException
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime
import threading
import cv2
import sys

# Global Variables for Phidgets and RoboClaw
motor_com_port = 'COM24'  
serial_obj = Serial(motor_com_port, 38400)
rc = Roboclaw(serial_obj, 0x80)

# Constants 
stepper_position = 20000  # This is a fixed position for demonstration

# Constnats 
shoulder_elbow_velocity_in = 0.4
wrist_speed = 64
stop_speed = 0
calibration_factor = 10000
threshold_force = 40  # Threshold in Newtons
times = []
forces = []
voltageInput0 = VoltageInput()
stepper = Stepper()
shoulderMotor = BLDCMotor()
elbowMotor = BLDCMotor()

def setup_phidgets():
    try:
        # Phidgets device setup
        stepper.openWaitForAttachment(5000)
        stepper.setEngaged(True)
        shoulderMotor.setDeviceSerialNumber(708023)
        shoulderMotor.setHubPort(4)
        shoulderMotor.openWaitForAttachment(5000)
        elbowMotor.setDeviceSerialNumber(708023)
        elbowMotor.setHubPort(3)
        elbowMotor.openWaitForAttachment(5000)
        voltageInput0.setOnVoltageChangeHandler(onVoltageInput0_VoltageChange)
        voltageInput0.openWaitForAttachment(5000)
    except PhidgetException as e:
        print(f"Phidget Exception {e.code} ({e.details})")
        sys.exit()

def onVoltageInput0_VoltageChange(self, voltage):
    force = voltage * calibration_factor
    if force > threshold_force:
        print("Force exceeds threshold, stopping...")
        plt.close('all')
        sys.exit()
    times.append(datetime.now())
    forces.append(force)

def animate(i, times, forces):
    plt.cla()
    plt.plot(times, forces, label="Force (N)")
    plt.axhline(y=threshold_force, color='r', linestyle='-', label="Threshold (40 N)")
    plt.legend(loc="upper right")
    plt.gcf().autofmt_xdate()
    plt.xlabel('Time')
    plt.ylabel('Force (N)')
    plt.title('Live Force over Time')

# Modify the on_press and on_release functions as per script (A), including wrist control
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
    shoulderMotor.setTargetVelocity(stop_speed)
    elbowMotor.setTargetVelocity(stop_speed)
    rc.forward_backward_m1(0)  
    # Escape key to break the loop
    if key == Key.esc:
        return False

def face_detection():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        cv2.imshow('Face detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def main_motor():
    setup_phidgets()
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()
    try:
        input("Press Enter to Stop\n")
    except:
        pass
    finally:
        listener.stop()
        stepper.setEngaged(False)
        stepper.close()
        shoulderMotor.close()
        elbowMotor.close()
        serial_obj.close()

def main():
    threading.Thread(target=face_detection, daemon=True).start()
    threading.Thread(target=main_motor, daemon=True).start()

    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, fargs=(times, forces), interval=1000)
    plt.show()

if __name__ == "__main__":
    main()
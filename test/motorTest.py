from Phidget22.Devices.BLDCMotor import *
from Phidget22.Phidget import *
import time
def onAttach(self):
    print("Attach!")
def onDetach(self):
    print("Detach!")

def main ():
    elbowMotor = BLDCMotor()
    #shoulderMotor = BLDCMotor()

    elbowMotor.setDeviceSerialNumber(708023)
    #shoulderMotor.setDeviceSerialNumber(708023)
    elbowMotor.setHubPort(3)
    #shoulderMotor.setHubPort(4)

    elbowMotor.setOnAttachHandler(onAttach)
    #shoulderMotor.setOnAttachHandler(onAttach)
    elbowMotor.setOnDetachHandler(onDetach)
    #shoulderMotor.setOnDetachHandler(onDetach)

    elbowMotor.openWaitForAttachment(1000)
    elbowMotor.setTargetVelocity(-0.5)
    time.sleep(2)
    elbowMotor.close()

    #shoulderMotor.openWaitForAttachment(1000)
    #shoulderMotor.setTargetVelocity(0.5)
    time.sleep(2)
    #shoulderMotor.close()

    elbowMotor.openWaitForAttachment(1000)
    elbowMotor.setTargetVelocity(-0.5)
    time.sleep(2)
    elbowMotor.close()

    try:
        input("Press Enter to Stop\n")
    except (Exception, KeyboardInterrupt):
        pass

main()
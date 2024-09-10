from Phidget22.Devices.BLDCMotor import *
from Phidget22.Phidget import *
import time

def onAttach(self):
    print("Attach!")


def onDetach(self):
    print("Detach!")


elbowMotor = BLDCMotor()
#shoulderMotor = BLDCMotor()

elbowMotor.setDeviceSerialNumber(708023)
#shoulderMotor.setDeviceSerialNumber(708023)
elbowMotor.setHubPort(3)
#shoulderMotor.setHubPort(3)

elbowMotor.setOnAttachHandler(onAttach)
#shoulderMotor.setOnAttachHandler(onAttach)
elbowMotor.setOnDetachHandler(onDetach)
#shoulderMotor.setOnDetachHandler(onDetach)

elbowMotor.openWaitForAttachment(1000)
#shoulderMotor.openWaitForAttachment(1000)
elbowMotor.setTargetVelocity(0.2)
#shoulderMotor.setTargetVelocity(-0.5)
time.sleep(2)
#shoulderMotor.close()

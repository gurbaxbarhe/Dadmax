from Phidget22.Phidget import *
from Phidget22.Devices.Stepper import *
import time

def main():
	stepper0 = Stepper()

	stepper0.openWaitForAttachment(5000)

	stepper0.setTargetPosition(50000)
	stepper0.setEngaged(True)

	try:
		input("Press Enter to Stop\n")
	except (Exception, KeyboardInterrupt):
		pass

	stepper0.close()

main()
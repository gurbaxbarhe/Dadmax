from Phidget22.Devices.VoltageInput import VoltageInput
from Phidget22.Phidget import PhidgetException
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Initialize lists to store time and voltage values
times = []
forces = []

def onVoltageInput0_VoltageChange(self, voltage):
    # Assuming voltage to force conversion is direct for illustration
    force = voltage * 10000  # Modify this conversion as necessary
    print("Voltage [1]: " + str(voltage) + " -> Force: " + str(force))
    # Append current time and force to lists
    times.append(datetime.now())
    forces.append(force)

def animate(i, times, forces):
    # Limit lists to keep last 60 values
    times = times[-60:]
    forces = forces[-60:]
    
    # Clear current plot
    plt.cla()
    # Plot new values
    plt.plot(times, forces)
    plt.gcf().autofmt_xdate()  # Format date on x-axis
    plt.xlabel('Time')
    plt.ylabel('Force (x10,000)')
    plt.title('Live Force over Time')

def main():
    voltageInput0 = VoltageInput()

    try:
        voltageInput0.setChannel(1)
        voltageInput0.setOnVoltageChangeHandler(onVoltageInput0_VoltageChange)
        voltageInput0.openWaitForAttachment(1000)
        
        # Set up plot to call animate() function periodically
        fig = plt.figure()
        ani = animation.FuncAnimation(fig, animate, fargs=(times, forces), interval=1000)
        plt.show()
        
        input("Press Enter to Stop\n")
        
    except PhidgetException as e:
        print(f"Phidget Exception {e.code} ({e.details})")
        exit(1)
    
    finally:
        voltageInput0.close()

if __name__ == "__main__":
    main()

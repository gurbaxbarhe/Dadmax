from roboclaw import Roboclaw
from serial import Serial
import time

motor_com_port = 'COM22'

serial_obj = Serial(motor_com_port, 38400) # default baudrate is 38400
rc = Roboclaw(serial_obj)

timing = 10
speed = 64
stop = 0
rc.forward_backward_mixed(64) # stops both motors

while 1:
    rc.forward_m1((speed))  # 1/4 power forward

    rc.backward_m1((speed))  # 1/4 power backward
    time.sleep((timing))

    #stops motor
    rc.forward_backward_mixed(64)
    time.sleep((timing))


# With exception to stop script
# from roboclaw import Roboclaw
# from serial import Serial
# import time
# import threading

# motor_com_port = 'COM18'

# serial_obj = Serial(motor_com_port, 38400)  # default baudrate is 38400
# rc = Roboclaw(serial_obj)

# timing = 10
# speed = 64
# stop = 0

# # Flag to control the loop execution
# running = True

# def control_motors():
#     rc.forward_backward_mixed(64)  # stops both motors initially
    
#     global running
#     while running:
#         rc.forward_m1(speed)  # 1/4 power forward
#         rc.backward_m1(speed)  # 1/4 power backward
#         time.sleep(timing)
        
#         # Stops motor
#         rc.forward_backward_mixed(64)
#         time.sleep(timing)

# # Start motor control in a separate thread
# motor_thread = threading.Thread(target=control_motors)
# motor_thread.start()

# input("Press Enter to stop...\n")

# # Stop the loop and wait for the thread to finish
# running = False
# motor_thread.join()

# # Cleanup: make sure to stop motors and close serial connection properly
# rc.forward_backward_mixed(64)  # ensure motors are stopped
# serial_obj.close()

import time
from pyfirmata import Arduino, util
from roboclaw import Roboclaw
from serial import Serial

motor_com_port = 'COM13'
arduino_com_port = 'COM14'

# Setup for Roboclaw
serial_obj = Serial(motor_com_port, 38400) 
rc = Roboclaw(serial_obj)
rc.Open()

# Setup for PyFirmata in Arduino
board = Arduino(arduino_com_port)
it = util.Iterator(board)
it.start()

# Analog pin for the force sensor
anal = board.get_pin('a:0:i')  

# Define initial speed and stop conditions
speed = 5
stop = 0

# Open port and move motor M1 forward at initial speed
rc.forward_m1(0x80, speed)

# Monitor force sensor and motor runtime
start_time = time.time()
runtime = 3  
max_iter = 100
inter_count = 0

# Force threshold
force_max = 5

try:
    while True:
        current_time = time.time()
        # Read fdorce sensor value
        analV = anal.read()  
        if analV != 0:
            # Scale reading (0 to 1) to (0 to 1023)
            force_value = analV * 1023  
            print(f"Force value: {force_value}")
            if force_value > force_max:  
                print(f"Force threshold exceeded, achieved {force_max} - stopping motor.")
                rc.forward_m1(0x80, stop)
                break

        # ** Likely need to convert this into hh:mm:ss format, pass as datetime() for both. Aids.
        if current_time - start_time > runtime:
            print("Runtime completed. Stopping motor.")
            rc.forward_m1(0x80, stop)
            break


        
        if inter_count >= max_iter:
            print(f"Ending after max iteration: {max_iter}")
            break
        
        inter_count += 1
        time.sleep(0.1)

finally:
    board.exit()

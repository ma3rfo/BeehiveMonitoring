import time
import RPi.GPIO as GPIO
from datetime import datetime
import signal
import sys
import time

#cover sensor pin and setup
cover_sensor = 16
detection_interval = 10

GPIO.setmode(GPIO.BOARD)
GPIO.setup(cover_sensor,GPIO.IN)

#counting pins and setup
# Define pins and modes for RPi
bees_count = 1000  # Total number of bees expected
outer_sensor = 13
inner_sensor = 15
leaving_count = 0
entering_count = 0
sensor_order = 1  # Track which sensor was triggered first (sensor 1)
state1 = True
state2 = True
GPIO.setmode(GPIO.BOARD)
GPIO.setup(outer_sensor, GPIO.IN)
GPIO.setup(inner_sensor, GPIO.IN)


# to stop the program when the system shuts down
def clean_up(signal_received, frame):
    print("\nSystem is shutting down... Cleaning up GPIO.")
    GPIO.cleanup()
    sys.exit(0)

# Handle system signals
signal.signal(signal.SIGTERM, clean_up)

#function to detect the state of the hive cover
def hive_cover():
    global cover_sensor,detection_interval
    start_time = time.time()
    # Get the state of the sensor and the time of reading
    sensor_state = GPIO.input(cover_sensor)
    current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if sensor_state == False:
        cover_state = 'CLOSED'
    elif sensor_state == True:
        cover_state = 'OPEN'
    print(f'HIVE IS {cover_state} at: {current_timestamp}',flush = True)
    elapsed_time = time.time() - start_time
    time.sleep(max(0, detection_interval - elapsed_time))
    # time.sleep(detection_interval)


# Define callback functions for counting
def outer_sensor_callback(channel):
    global sensor_order,leaving_count, state1, state2
    if sensor_order == 1  and state1 :
        # If the outer sensor is triggered first
        sensor_order = 2
        state1 = False
        print('started entering')
    elif sensor_order == 2 and state1:
       # If the outer sensor is triggered after the inner sensor
        print("leaving the hive")
        leaving_count += 1
        sensor_order = 1  # Reset sensor order
        print(f'{leaving_count} bees left the hive')
        state2 = True
def inner_sensor_callback(channel):
    global sensor_order,  entering_count, state2, state1
    if sensor_order == 2 and state2:
        # If the inner sensor is triggered after the outer sensor
        print("Entering the hive")
        entering_count += 1
        sensor_order = 1  # Reset sensor order
        print(f'{entering_count} bees entered the hive')
        state1 = True
    elif sensor_order == 1 and state2:
        sensor_order = 2
        state2  = False
        print('started leaving')

# Add event detection for the sensors
GPIO.add_event_detect(outer_sensor, GPIO.FALLING, callback=outer_sensor_callback, bouncetime=200)
GPIO.add_event_detect(inner_sensor, GPIO.FALLING, callback=inner_sensor_callback, bouncetime=200)

try:
    print('System initiatlized. press Ctrl_c to stop')
    while True:
        # Start the hive cover detection
        net_traffic = leaving_count - entering_count
        print(f'{entering_count} bees entered',flush = True)
        print(f'{leaving_count} bees left',flush = True)
        hive_cover()
except KeyboardInterrupt:
    print("\nExiting program.")
    clean_up(None,None)

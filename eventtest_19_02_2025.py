
import time
import RPi.GPIO as GPIO

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

# Define callback functions
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
    print("System initialized. Press Ctrl+C to stop.")
    while True:
        # Calculate and print the current state
        net_traffic = leaving_count - entering_count
        print(f'{entering_count} bees entered')
        print(f'{leaving_count} bees left')
       # print(f'{entering_count} bees entered')
       # print(f"No. of bees outside the hive: {net_traffic}")
       # print(f"No. of bees inside the hive: {bees_count - net_traffic}")
        time.sleep(7)  # Reduce CPU usage

except KeyboardInterrupt:
    print("\nExiting program.")
finally:
    GPIO.cleanup()

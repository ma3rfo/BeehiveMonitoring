import time
import RPi.GPIO as GPIO
from datetime import datetime

cover_sensor = 11
detection_interval = 15

GPIO.setmode(GPIO.BOARD)
GPIO.setup(cover_sensor,GPIO.IN)

def hive_cover():
    global cover_sensor,detection_interval
    try:
        while True:
            # Get the state of the sensor and the time of reading
            sensor_state = GPIO.input(cover_sensor)
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if sensor_state == False:
                cover_state = 'CLOSED'
            elif sensor_state == True:
                cover_state = 'OPEN'
            print(f'HIVE IS {cover_state} at: {current_timestamp}')
            time.sleep(detection_interval)


    except KeyboardInterrupt:
        print("\nDetection is stopped...")
        GPIO.cleanup()


hive_cover()



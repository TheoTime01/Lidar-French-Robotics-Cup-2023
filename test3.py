import PyLidar3
import math
import time
import RPi.GPIO as GPIO

# Set up GPIO pins
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)


Obj = PyLidar3.YdLidarX4("COM3") #PyLidar3.your_version_of_lidar(port,chunk_size)
if(Obj.Connect()):
    # print("Connected to Lidar")
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    # t = time.time() # start time
    i=0
    try:
        while True:
            data = next(gen)
            i+=1
            opponent_detected = False # assume no opponent detected
            for angle in data:
                if 90<angle<270:
                    if 400<data[angle]<600: # detects an opponent
                        # t1 = time.time() - t
                        # print("tour :", i, "angle :" ,angle," distance :",data[angle], "time :", t1)
                        opponent_detected = True # set the flag to True
            if not opponent_detected: # if no opponent detected
                GPIO.output(18, GPIO.LOW) # turn off LED connected to GPIO pin 18
                GPIO.output(23, GPIO.HIGH) # turn on LED connected to GPIO pin 23
            else:
                GPIO.output(18, GPIO.HIGH) # turn on LED connected to GPIO pin 18
                GPIO.output(23, GPIO.LOW) # turn off LED connected to GPIO pin 23
    except KeyboardInterrupt:
        Obj.StopScanning()

# Clean up GPIO pins
GPIO.cleanup()

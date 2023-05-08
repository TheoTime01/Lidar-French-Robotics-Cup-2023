import PyLidar3
import time # Time module
#Serial port to which lidar connected, Get it from device manager windows
#In linux type in terminal -- ls /dev/tty* 

results=[]

#port = "/dev/ttyUSB0" #linux
Obj = PyLidar3.YdLidarX4("COM3") #PyLidar3.your_version_of_lidar(port,chunk_size)
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while (time.time() - t) < 5: #scan for 30 seconds
        print(next(gen))
        results.append(next(gen))
        time.sleep(0.5)
    Obj.StopScanning()
    Obj.Disconnect()
    with open("lidar.json","w") as f:
        f.write(str(results))
    print("Done")
else:
    print("Error connecting to device")
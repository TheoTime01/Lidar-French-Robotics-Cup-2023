import PyLidar3
import math    
import time
import csv # for writing to csv file


def al_kashi_theorem(distances):
    """
    Apply the Al-Kashi theorem to the distances to find the opposite side
    """
    results = {}
    for angle, distance in distances.items():
        opposite = 0
        for a, d in distances.items():
            if a != angle:
                opposite += d**2
        opposite -= distance**2
        opposite /= -2*distance
        opposite = math.sqrt(opposite)
        results[angle] = opposite
    return results


Obj = PyLidar3.YdLidarX4("COM3") #PyLidar3.your_version_of_lidar(port,chunk_size) 
if(Obj.Connect()):
    print(Obj.GetDeviceInfo())
    gen = Obj.StartScanning()
    t = time.time() # start time 
    while True: #scan for 30 seconds
        opp=0
        data = next(gen)
        data2 = al_kashi_theorem(data)
        for angle in data:
            distance = data[angle]
            if 40<distance<60:
                print("Distance: ", distance)
                print("Angle: ", angle)
                print("Opposite: ", data2[angle])
                print("Time taken: ", time.time() - t)
                opp = opp+data2[angle]
        
        if opp>=190:
            print("Enemy detected")
                
    Obj.StopScanning()
    Obj.Disconnect()
else:
    print("Error connecting to device")

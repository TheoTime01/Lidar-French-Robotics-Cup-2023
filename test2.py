import matplotlib.pyplot as plt
import PyLidar3
import numpy as np
import matplotlib.animation as animation

# create PyLidar3 object
lidar = PyLidar3.YdLidarX4("COM3")
lidar.StartScanning()

# verifie if there is a enemy between 90 and 270
def is_detected(data):
    """ Return True if the opposite side is greater than 190mm between the angles 20 degrees and 160 degrees
        Args:
            D: the list of distances and angles D={angle:distance}
        Returns:
            True if the opposite side is greater than 190mm between the angles 90 degrees and 270 degrees
            False otherwise
    """
    data2 = calculate_opposite_side(data)
    opp=0
    a=0
    for angle in data:
        if 90<angle<270 :
            if 40<data[angle]<60:
                if angle-a < 3:
                    opp = opp + data2[angle]
                    a=angle
                else:
                    break
        
    if opp>=100:
        print("enemy spotted")
        return True
    else:
        return False

# this code is adapted from https://gitlab.insa-rouen.fr/cpotron/ydlidar-x4-python-interface
import serial
import math
import numpy as np
import pyqtgraph as pg  # pip install PyQt5==5.13.0 <- THIS IS IMPORTANT! NEWER DOES NOT WORK ON OSX 10.12.6
import time
import csv # for writing to csv file


stepsPerRevolution = 700
degreesPerStep = 360 / stepsPerRevolution

scanId = 0
lidarPort = 'COM3'

lidar = serial.Serial(lidarPort, 128000) #serial.Serial(lidarPort, Baudrate) 
lidar.flush() # Waits for the transmission of outgoing serial data to complet 



def wait_reply_header():
    is_received = False
    while not is_received:
        b1 = lidar.read(1)
        if b1 == b'\xa5':
            b2 = lidar.read(1)
            if b2 == b'\x5a':
                return True


def get_scan():
    data = {}
    lidar.read(2)
    data['ct'] = int.from_bytes(lidar.read(1), byteorder='little') # Indicates the current packet type
    data['lsn'] = int.from_bytes(lidar.read(1), byteorder='little') #  Indicates the number of sample points contained in the current packet
    data['fsa'] = int.from_bytes(lidar.read(2), byteorder='little') >> 1 # First sample angle
    data['lsa'] = int.from_bytes(lidar.read(2), byteorder='little') >> 1 # Last sample angle
    data['sample'] = []
    lidar.read(2)
    for sample in range(0, data['lsn']):
        data['sample'].append(
            int.from_bytes(lidar.read(2), byteorder='little') / 4) # page 6 of the datasheet DEVELOPMENT MANUAL
    return data


def get_ang_correct(distance):
    if distance == 0:
        return 0
    return math.degrees(
        math.atan(21.8 * (155.3 - distance) / (155.3 * distance))) # page 7 of the datasheet DEVELOPMENT MANUAL


def process_trame(trame):
    result = {}
    result['distance'] = []
    result['angle'] = []
    angle_fsa = (trame['fsa'] / 64) + get_ang_correct(trame['sample'][0])
    angle_lsa = (trame['lsa'] / 64) + get_ang_correct(trame['sample'][-1])
    if angle_fsa < angle_lsa:
        interval = (angle_lsa - angle_fsa) / (trame['lsn'] - 1)
    else:
        interval = (360 + angle_lsa - angle_fsa) / (trame['lsn'] - 1)
    for sample in range(0, trame['lsn']):
        if trame['sample'][sample] != 0:
            result['distance'].append(trame['sample'][sample])
            angle = interval * (sample - 1) + angle_fsa + get_ang_correct(
                trame['sample'][sample])
            if angle > 360:
                result['angle'].append(angle - 360)
            elif angle < 0:
                result['angle'].append(angle + 360)
            else:
                result['angle'].append(angle)
    return result


if __name__ == '__main__':
    lidar.write(serial.to_bytes([0xA5, 0x60]))
    wait_reply_header()
    lidar.read(5)

    fig = pg.plot([], [])
    previous = 0
    size = 0
    buf = np.zeros(360)

    lastAngle = 0
    turnCount = 0


    while True:
        trame = get_scan()
        taille = trame['lsn']
        if taille > 1:
            new_value = process_trame(trame)
            if new_value['angle']:
                for index in range(0, len(new_value['angle'])):
                    lastAngle = new_value['angle'][0]
                    distance = 0
                    angle = 0
                    vertical_angle = 0

                    # Check distance and angle range
                    if new_value['distance'][index] < 40:
                        a = int(new_value['angle'][index])
                        if 0 <= a < 90:
                            print("Robot between 0-90")
                        elif 90 <= a < 180:
                            print("Robot between 90-180")
                        elif 180 <= a < 270:
                            print("Robot between 180-270")
                        elif 270 <= a <= 360:
                            print("Robot between 270-360")


                    # # Update the plot
                    # if a < previous:
                    #     size = len(buf) - previous + a
                    #     values = np.concatenate((buf[previous:], buf[:a]), axis=0)
                    #     angles = np.linspace(previous, len(buf) - 1, size) + turnCount * 360
                    #     previous = a
                    #     turnCount += 1
                    # else:
                    #     size = a - previous
                    #     values = buf[previous:a]
                    #     angles = np.linspace(previous, a - 1, size) + turnCount * 360



                    # #ecrire dans un fichier csv new_value['angle'][index] et new_value['distance'][index]
                    # #attendre 5 secondes avant de d'ecrire dans le fichier csv
                    # with open('data.csv', 'a', newline='') as csvfile:
                    #     spamwriter = csv.writer(csvfile, delimiter=' ',
                    #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    #     spamwriter.writerow([new_value['angle'][index], new_value['distance'][index]])
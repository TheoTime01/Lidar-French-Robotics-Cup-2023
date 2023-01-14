# this code is adapted from https://gitlab.insa-rouen.fr/cpotron/ydlidar-x4-python-interface
import serial
import math
import numpy as np
import pyqtgraph as pg  # pip install PyQt5==5.13.0 <- THIS IS IMPORTANT! NEWER DOES NOT WORK ON OSX 10.12.6
import time

stepsPerRevolution = 700
degreesPerStep = 360 / stepsPerRevolution

scanId = 0
lidarPort = 'COM3'

lidar = serial.Serial(lidarPort, 128000) #serial.Serial(lidarPort, Baudrate) 
lidar.flush() # Waits for the transmission of outgoing serial data to complet 
# time.sleep(1)


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


def get_cartesian_coords(buf):
    x = []
    y = []
    for angle in range(360):
        x.append(buf[angle] * np.cos(math.radians(angle)))
        y.append(buf[angle] * np.sin(math.radians(angle)))
    return (x, y)


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
        pg.QtGui.QGuiApplication.processEvents()
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

                    #print("new_value",new_value)
                    #print("new_value['angle'][0]",new_value['angle'][0])

                    a = int(new_value['angle'][index])
                    d = new_value['distance'][index]
                    buf[a] = d
                    if previous > a and previous > 300 and size > 400:
                        x, y = get_cartesian_coords(buf)
                        size = 0
                        fig.plot(x, y, clear=True, pen=(0,200,0),  symbol='o', symbolSize=1)
                        fig.setXRange(-3000, 3000)
                        fig.setYRange(-3000, 3000)
                        fig.plot([0], [0], symbolPen='r')
                    previous = a
                    size += 1
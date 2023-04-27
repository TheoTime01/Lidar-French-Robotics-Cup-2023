import matplotlib.pyplot as plt
import PyLidar3
import numpy as np
import matplotlib.animation as animation

# create PyLidar3 object
lidar = PyLidar3.YdLidarX4("COM3")
lidar.StartScanning()

# create matplotlib figure and axes
fig, ax = plt.subplots()
ax.set_title('Lidar Data')

# set the x and y limits of the plot
ax.set_xlim([-5000, 5000])
ax.set_ylim([-5000, 5000])

# create scatter plot object
scatter_plot = ax.scatter([], [], s=1)

# update function to read and display lidar data
def update(i):
    data = lidar.StartScanning()
    angles = data[0]
    distances = data[1]

    points = []
    for i, angle in enumerate(angles):
        distance = distances[i]
        x = distance * np.cos(np.radians(angle))
        y = distance * np.sin(np.radians(angle))
        points.append([x, y])

        # check for angle and distance thresholds
        if angle >= 1 and angle <= 90 and distance < 300:
            print("Enemy Right Front")

        elif angle >= 91 and angle <= 180 and distance < 300:
            print("Enemy Right Rear")

        elif angle >= 181 and angle <= 270 and distance < 300:
            print("Front left enemy")

        elif angle >= 271 and angle <= 360 and distance < 300:
            print("Left Front Enemy")

    scatter_plot.set_offsets(points)

# # set up animation
# ani = animation.FuncAnimation(fig, update, interval=50)

# plt.show()

# stop lidar scanning and disconnect
lidar.StopScanning()
lidar.Disconnect()

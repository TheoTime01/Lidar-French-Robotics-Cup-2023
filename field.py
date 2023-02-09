import csv
import math
import matplotlib.pyplot as plt

# Generate points on the terrain
points = []
for x in range(0, x_dim, 0.5):
    for y in range(0, y_dim, 0.5):
        angle = math.atan2(y, x)
        points.append((x, y, angle))

# Write points to csv file
with open("points.csv", "w") as file:
    writer = csv.writer(file)
    writer.writerow(["x", "y", "angle"])
    for x, y, angle in points:
        writer.writerow([x, y, angle])

# Read points from csv file
csv_points = []
with open("points.csv") as file:
    reader = csv.reader(file)
    next(reader) # skip header row
    for row in reader:
        x, y, angle = map(float, row)
        csv_points.append((x, y, angle))

# Compare points and create green and blue tables
green_table = []
blue_table = []
for x, y, angle in points:
    for x2, y2, angle2 in csv_points:
        if x == x2 and y == y2:
            if angle <= angle2:
                green_table.append((x, y))
            else:
                blue_table.append((x, y))

# Plot points using Matplotlib
green_x, green_y = zip(*green_table)
blue_x, blue_y = zip(*blue_table)

plt.scatter(green_x, green_y, color="green")
plt.scatter(blue_x, blue_y, color="blue")

plt.xlabel("x")
plt.ylabel("y")
plt.title("Terrain Points")

plt.show()

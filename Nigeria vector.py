import csv
import math
import random
import shapefile
import matplotlib.pyplot as plt
import pandas as pd
# -----------------------------------
# Files
# -----------------------------------
# CSV Southern Bpundary removed
FILTERED_CSV = "nigeria_boundary_filtered.csv"
# Load states boundaries
ADM1_SHP = "gadm41_NGA_1.shp"
# Load Sensors, expect information from inside the states
df = pd.read_excel("points_inside_nigeria.xlsx")

lats = df["latitude"]
lons = df["longitude"]
N_POINTS = 380

# Load filtered polyline Southern boundary removed!!!!!
coords = []
with open(FILTERED_CSV, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        lon = float(row["longitude"])
        lat = float(row["latitude"])
        coords.append((lon, lat))

# Compute cumulative arc length to find the new border length.
distances = [0.0]

for i in range(1, len(coords)):
    x1, y1 = coords[i - 1]
    x2, y2 = coords[i]
    d = math.hypot(x2 - x1, y2 - y1)
    distances.append(distances[-1] + d)

total_length = distances[-1]

# Generate uniformly spaced target distances along the border
step = total_length / N_POINTS
target_distances = [i * step for i in range(N_POINTS)]

# Interpolate points along the polyline and this points will act as border post,
# Other sensor information and other crossings
sampled_points = []

j = 0
for td in target_distances:
    while distances[j + 1] < td:
        j += 1

    d1 = distances[j]
    d2 = distances[j + 1]
    t = (td - d1) / (d2 - d1)

    x1, y1 = coords[j]
    x2, y2 = coords[j + 1]

    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)

    sampled_points.append((x, y))

# Load ADM1 states boundaries (context)
sf_states = shapefile.Reader(ADM1_SHP)
# Plot
plt.figure(figsize=(10, 12))

# Plot ADM1 states boundaries 
for shape in sf_states.shapes():
    xs = [p[0] for p in shape.points]
    ys = [p[1] for p in shape.points]
    plt.plot(xs, ys, linewidth=0.5)

# Plot boundary polyline after we have removed the southern part of the country
#--> Warning I need to damp the field to zero in the Southern part for smooth 
# {Lihle mark point}
boundary_x = [p[0] for p in coords]
boundary_y = [p[1] for p in coords]
plt.plot(boundary_x, boundary_y, linewidth=1.2, label="Filtered Boundary")

# Plot uniformly spaced points used as sensing points around the National border
#---> Warning you need sensor intial conditions {Lihle mark point}
sx = [p[0] for p in sampled_points]
sy = [p[1] for p in sampled_points]
plt.scatter(sx, sy, s=12, label="380 Boundary Points")

# Inner points plots
#---> Warning you need sensor intial conditions {Lihle mark point}
plt.scatter(
    lons,
    lats,
    s=30,
    marker="o"
)

plt.title("Nigeria Boundary inner and boundary points that influences migration")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

plt.axis("equal")
plt.grid(True, linestyle="--", alpha=0.4)
plt.legend()

plt.show()
migration_fields.py
import shapefile
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load Nigeria boundaries
# National Level
ADM0 = "gadm41_NGA_0.shp"
# Province Level
ADM1 = "gadm41_NGA_1.shp"

sf0 = shapefile.Reader(ADM0)
sf1 = shapefile.Reader(ADM1)

# Building a discritized lon-lat grid over Nigeria
lon_min, lon_max = 2.5, 14.7
lat_min, lat_max = 4.0, 14.2

nx, ny = 120, 120
lon = np.linspace(lon_min, lon_max, nx)
lat = np.linspace(lat_min, lat_max, ny)
X, Y = np.meshgrid(lon, lat)

# ---- Solution Space After computation
# Pseudo migration risk potential field
# Adjust field so it properly overlays Nation boundary.{Lihle mark point!!!}

Z = (
    0.8 * np.exp(-((X - 8.5)**2 +
                   (Y - 9.5*np.random.normal(0, 2))**2) / 8) +
    0.5 * np.exp(-((X - 6.0)**2 + (Y - 6.5)**2) / 6) +
    0.3 * np.sin(0.6 * X) * np.cos(0.6 * Y)
)

# Vector field = negative gradient
# Check if we need to account for earth curveture in Nigeria: Christoffer symbols
# {Lihle mark point!!!}
dZdy, dZdx = np.gradient(Z, lat, lon)
U = -dZdx
V = -dZdy

# =======================================
# FIGURE 1: Scalar potential field
# =======================================
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(111, projection="3d")

# --- STORE the surface ---
surf = ax.plot_surface(
    X, Y, Z,
    cmap="viridis",
    alpha=0.85,
    linewidth=0
)

# National boundary
for shp in sf0.shapes():
    xs, ys = zip(*shp.points)
    ax.plot(xs, ys, zs=0, color="black", linewidth=2)

# Province boundaries
for shp in sf1.shapes():
    xs, ys = zip(*shp.points)
    ax.plot(xs, ys, zs=0, color="gray", linewidth=0.6)

ax.set_title("Migration Scalar scalar potential")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Migration Risk Potential")
cbar = fig.colorbar(surf, ax=ax, shrink=0.6, pad=0.1)
cbar.set_label("Migration Risk Potential")

plt.show()


# =======================================
# FIGURE 2: Vector field (flow)
# =======================================
fig = plt.figure(figsize=(11, 9))
ax = fig.add_subplot(111, projection="3d")

# Downsample for clarity
skip = 6
ax.quiver(
    X[::skip, ::skip],
    Y[::skip, ::skip],
    Z[::skip, ::skip],
    U[::skip, ::skip],
    V[::skip, ::skip],
    -0.1 * np.ones_like(U[::skip, ::skip]),
    length=0.5,
    normalize=True,
    color="crimson"
)

# At National  boundary
for shp in sf0.shapes():
    xs, ys = zip(*shp.points)
    ax.plot(xs, ys, zs=0, color="black", linewidth=2)

# Province boundaries
for shp in sf1.shapes():
    xs, ys = zip(*shp.points)
    ax.plot(xs, ys, zs=0, color="gray", linewidth=0.6)

ax.set_title("Migration Flow Vector Field (−∇φ)")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
ax.set_zlabel("Potential Height")
plt.tight_layout()
plt.show()
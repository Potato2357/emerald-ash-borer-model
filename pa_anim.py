import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import geopandas
import pandas

# import data
pa_counties = geopandas.read_file("PaCounty2026_01.geojson")
data = pandas.read_csv("sim_data.csv")

frame_no = len(data.columns) - 2

fig, ax = plt.subplots(figsize=(10, 6))

# set up normalized colormap
# vmin = data.iloc[:, 2:].min().min()
vmin = 0
vmax = data.iloc[:, 2:].max().max()
norm = Normalize(vmin=vmin, vmax=vmax)
sm = ScalarMappable(cmap=plt.cm.YlGnBu, norm=norm)

def update(frame):
    ax.clear()

    frame_values = data.iloc[:, frame+2].values
    colors = sm.to_rgba(frame_values)

    pa_counties.plot(
        ax=ax,
        color=colors,
        edgecolor="black"
    )

    ax.set_title(f"t = year {frame/2}")
    ax.axis("off")


ani = FuncAnimation(fig, update, frames=frame_no, interval=200)
ani.save(filename="animation_test.gif", writer="pillow")


for i in range(frame_no):
    ax.clear()

    frame_values = data.iloc[:, i+2].values
    colors = sm.to_rgba(frame_values)

    pa_counties.plot(
        ax=ax,
        color=colors,
        edgecolor="black"
    )

    ax.set_title(f"t = year {i/2}")
    ax.axis("off")
    plt.savefig(f"./animations/frame_{i}.png")



pa_counties.plot(data.iloc[:, 1], vmin = 0, vmax = 20, cmap = plt.cm.rainbow, edgecolor="black", figsize=(12, 8), legend=True)

plt.axis("off")
plt.savefig("inf_t.png")

plt.show()
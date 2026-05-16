import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
import geopandas
import pandas

# import data
pa_counties = geopandas.read_file("PaCounty2026_01.geojson")
data = pandas.read_csv("pic_maker_dat.csv")

pa_counties.plot(data.iloc[:, 1], vmin = 0, vmax = 2, cmap = plt.cm.binary, edgecolor="black", figsize=(12, 8))

plt.axis("off")

plt.show()
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# we are creating a heatmap of geographical data
conn = sqlite3.connect('cameras.db')
df = pd.read_sql_query("SELECT * FROM cameras", conn)
df = df.dropna()
#        lat     lon   file            timestamp  cars
# 0  42.0676 -4.2227  2.jpg  2023-04-18_19-10-41     0
# 1  41.9811 -4.4348  3.jpg  2023-04-18_19-10-41     1
# 2  41.9227 -4.5063  4.jpg  2023-04-18_19-10-41     0
# 3  41.8563 -4.5531  5.jpg  2023-04-18_19-10-41     0
# 4  41.7026 -4.7118  6.jpg  2023-04-18_19-10-41     2

# transform timestamp to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'], format="%Y-%m-%d_%H-%M-%S")


# we are going to create a heatmap of the data
# create a set of timestamps, and have user select one
timestamps = df['timestamp'].unique()
for i, timestamp in enumerate(timestamps):
    print(f"{i}: {timestamp}")
selected = int(input("Select a timestamp: "))
timestamp = timestamps[selected]
print(f"Selected timestamp: {timestamp}")

# create a dataframe with only the selected timestamp
df = df[df['timestamp'] == timestamp]

# create a heatmap of coordinates and cars detected over Spain
# overlay a map of Spain from the Basemap library
from mpl_toolkits.basemap import Basemap
import numpy as np

# create a map of Spain
m = Basemap(projection='merc', llcrnrlat=35, urcrnrlat=45, llcrnrlon=-10, urcrnrlon=5, lat_ts=20, resolution='h')
m.drawcoastlines()
m.drawcountries()
m.fillcontinents(color='coral', lake_color='aqua')
m.drawmapboundary(fill_color='aqua')

# create a heatmap of the data
# we need to convert the lat/lon coordinates to x/y coordinates
# we need to convert the number of cars to a color

# convert lat/lon to x/y
x, y = m(df['lon'].values, df['lat'].values)

# convert number of cars to color
# we are going to use a colormap
# we are going to use the min/max values of the number of cars
colors = df['cars'].values
norm = plt.Normalize(colors.min(), colors.max())
cmap = plt.get_cmap('jet')
m.scatter(x, y, 5, marker='o', color=cmap(norm(colors)))
plt.colorbar(plt.cm.ScalarMappable(norm=norm, cmap=cmap), label='Cars')

# save as png with timestamp
plt.savefig(f"heatmap_{timestamp}.png")

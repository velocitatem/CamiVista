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

# create an interactive heatmap using folium
import folium
from folium.plugins import HeatMap

# create a map
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=10)

# create a color map with intensity based on number of cars
# we are going to use a linear color map
color = lambda cars: f"#{int(255 * cars / df['cars'].max()):02x}0000"
# create a list of points with lat, lon, and color
points = [[row['lat'], row['lon'], color(row['cars']), row['file']] for _, row in df.iterrows()]
# remove na values
points = [point for point in points if not any([pd.isna(x) for x in point])]
for point in points:
    # add the camera image as a popup
    folium.Marker(location=point[:2], ).add_to(m)
    folium.CircleMarker(location=point[:2], radius=10, color=point[2], fill=True, fill_color=point[2], fill_opacity=0.9, popup=folium.Popup(f"<img src='/mnt/s/Documents/Projects/SpainCameras/images/{timestamp}/{point[3]}-aied.jpg' />")).add_to(m)

# add the heatmap



# save the map
m.save('heatmap.html')

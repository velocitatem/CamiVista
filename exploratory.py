import sqlite3
import os
import numpy as np
import pandas as pd


# download cameras.db fro https://drive.google.com/file/d/1k2ctA37Ezsjt8twBvo4fqQb3XpDPOcVP/view?usp=sharing
import urllib.request
url = 'https://drive.google.com/uc?export=download&id=1k2ctA37Ezsjt8twBvo4fqQb3XpDPOcVP'
urllib.request.urlretrieve(url, 'cameras.db')

db = sqlite3.connect('cameras.db')
cursor = db.cursor()
df = pd.read_sql_query("SELECT * FROM cameras", db)
print(df.describe())
print(df.head())
#        lat     lon   file            timestamp highway  highway_position  cars heading province
# 0  42.0676 -4.2227  2.jpg  2023-04-21_15-02-18    a-62              57.9     1       -       34
# 1  41.9811 -4.4348  3.jpg  2023-04-21_15-02-18    a-62              78.5     0       -       34
# 2  41.9227 -4.5063  4.jpg  2023-04-21_15-02-18    a-62              87.9     0       +       34
# 3  41.8563 -4.5531  5.jpg  2023-04-21_15-02-18    a-62              96.3     3       -       34
# 4  41.7026 -4.7118  6.jpg  2023-04-21_15-02-18    a-62             118.3     4       +       47

# create a map with the highlighted highways
import folium
from folium.plugins import MarkerCluster
from folium.plugins import FastMarkerCluster

# create a map with the highlighted highways
m = folium.Map(location=[41.65, -4.75], zoom_start=7, tiles='Stamen Terrain')
folium.TileLayer('openstreetmap').add_to(m)
folium.TileLayer('cartodbpositron').add_to(m)
folium.TileLayer('cartodbdark_matter').add_to(m)
folium.TileLayer('stamenterrain').add_to(m)
folium.TileLayer('stamentoner').add_to(m)
folium.TileLayer('stamenwatercolor').add_to(m)
folium.LayerControl().add_to(m)

highways = df['highway'].unique()
# create a color for each highway based on the min and max of the cars in total in the data
min_cars = df['cars'].min()
max_cars = df['cars'].max()
# color should be a greadient from red to green
colorHW = lambda mean: '#%02x%02x%02x' % (int(255-mean/max_cars*255), int(mean/max_cars*255), 0)
for highway in highways:
    df_highway = df[df['highway'] == highway]
    # sort by highway_position
    df_highway = df_highway.sort_values(by=['highway_position'])
    # average cars on the highway
    cars = df_highway['cars'].mean()
    color = colorHW(cars)
    # create a polyline
    folium.PolyLine(df_highway[['lat', 'lon']].values.tolist(), color=color, weight=2.5, opacity=1).add_to(m)


m.save('map.html')

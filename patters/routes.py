import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('../cameras.db')
df = pd.read_sql_query("SELECT * FROM cameras", conn)
df = df.dropna()
#        lat     lon   file            timestamp  cars
# 0  42.0676 -4.2227  2.jpg  2023-04-18_19-10-41     0
# 1  41.9811 -4.4348  3.jpg  2023-04-18_19-10-41     1
# 2  41.9227 -4.5063  4.jpg  2023-04-18_19-10-41     0
# 3  41.8563 -4.5531  5.jpg  2023-04-18_19-10-41     0
# 4  41.7026 -4.7118  6.jpg  2023-04-18_19-10-41     2

# create a set of timestamps, and have user select one
timestamps = df['timestamp'].unique()
for i, timestamp in enumerate(timestamps):
    print(f"{i}: {timestamp}")
selected = int(input("Select a timestamp: "))
timestamp = timestamps[selected]
print(f"Selected timestamp: {timestamp}")

# create a dataframe with only the selected timestamp
df = df[df['timestamp'] == timestamp]


# using the data, identify routes and plot them on a map
# using a clustering algorithm, identify the routes and plot them on a map
# https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import numpy as np

routes = DBSCAN(eps=0.02, min_samples=2).fit_predict(df[['lat', 'lon']])
# eps: The maximum distance between two samples for them to be considered as in the same neighborhood.
# min_samples: The number of samples (or total weight) in a neighborhood for a point to be considered as a core point. This includes the point itself.

import folium

# create map
m = folium.Map(location=[df['lat'].mean(), df['lon'].mean()], zoom_start=10)

# plot the routes, using a different color for each route (identified by the cluster number)
for route in np.unique(routes):
    if route == -1:
        continue
    df_route = df[routes == route]
    # folium.PolyLine(df_route[['lat', 'lon']].values.tolist(), color='red').add_to(m)

# create a generalized shape and arrow for each route (using the mean of the coordinates)
# the direction is given by the highest count of cars to the lowest count of cars
directed_paths = []
for route in np.unique(routes):
    if route == -1:
        continue
    df_route = df[routes == route]
    df_route = df_route.sort_values('cars')
    start = df_route.iloc[0]
    end = df_route.iloc[-1]
    # folium.Marker([start['lat'], start['lon']], icon=folium.Icon(color='green', icon='info-sign')).add_to(m)
    # folium.Marker([end['lat'], end['lon']], icon=folium.Icon(color='red', icon='info-sign')).add_to(m)
    # folium.PolyLine([[start['lat'], start['lon']], [end['lat'], end['lon']]], color='blue').add_to(m)
    directed_paths.append([[start['lat'], start['lon']], [end['lat'], end['lon']]])

# use the directed paths to create a vector field and plot it on the map. Each directed path is a cector, interpolate the vectors to create a vector field
# plot each vector as a simple arrow on the map
field = []
for i in range(len(directed_paths)):
    for j in range(i+1, len(directed_paths)):
        field.append([directed_paths[i], directed_paths[j]])
# fill in the field with interpolated vectors to create a vector field
# range of the field is from the minimum latitude to the maximum latitude, and from the minimum longitude to the maximum longitude of the data
# the number of vectors in the field is the number of directed paths squared
min_lat = df['lat'].min()
max_lat = df['lat'].max()
min_lon = df['lon'].min()
max_lon = df['lon'].max()
horizontal_count = len(directed_paths) ** 2
vertical_count = len(directed_paths) ** 2

def interpolate(position):
    # position is a tuple of latitude and longitude
    # closest_vector is a tuple of two tuples of latitude and longitude
    # find the closest vector to the position by checking 0.01 degrees in each direction
    closest_vectors = []
    # search in a radious around the position to find the closest 3 vectors
    while len(closest_vectors) < 3:
        for i in range(-1, 2):
            for j in range(-1, 2):
                for vector in field:
                    if vector[0][0] == position[0] + i * 0.01 and vector[0][1] == position[1] + j * 0.01:
                        closest_vectors.append(vector)
    # get the average direction of the closest vectors
    direction = [0, 0]
    for vector in closest_vectors:
        direction[0] += vector[1][0] - vector[0][0]
        direction[1] += vector[1][1] - vector[0][1]
    direction[0] /= len(closest_vectors)
    direction[1] /= len(closest_vectors)
    # return the direction
    return direction

print(horizontal_count, vertical_count)
empty_field = np.zeros((horizontal_count, vertical_count))
for i in range(horizontal_count):
    for j in range(vertical_count):
        position = (min_lat + i * (max_lat - min_lat) / horizontal_count, min_lon + j * (max_lon - min_lon) / vertical_count)
        direction = interpolate(position)
        # create a new set of coordinates for the vector based on the direction and the position
        print(direction)



# plot the vector field on the map






# save the map
m.save('map.html')

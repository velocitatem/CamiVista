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
# go through each directed path and find a neighbor that is going in a similar direction
# if a neighbor is found, draw an arrow from the start of the first to the start of the second and to the end of the second
# use a cosine similarity to determine if the vectors are similar enough
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# for each path, look for a neighbor that is only 0.01 degrees away
def proximity_check(path, path2):
    # end of first is by the start of the second
    end= path[1]
    start = path2[0]
    if abs(end[0] - start[0]) < 0.05 and abs(end[1] - start[1]) < 0.05:
        return True
    print("Not close enough")



# find paths that are similar in direction and position and merge them

def approx(directed_paths):
    new_paths = []
    for path in directed_paths:
        for path2 in directed_paths:
            print("Checking paths")
            if proximity_check(path, path2):
                # if the paths are similar, merge them
                if cosine_similarity(path[1], path2[1]) > 0.9:
                    # create a new path that is the first path with the second path appended to it
                    new_path = path
                    new_path.append(path2[1])
                    new_paths.append(new_path)
                    break

    return new_paths

for i in range(20):
    directed_paths = approx(directed_paths)

for path in directed_paths:
    folium.PolyLine(path, color='blue').add_to(m)







# save the map
m.save('map.html')

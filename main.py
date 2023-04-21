# get this data: https://www.dgt.es/.content/.assets/json/camaras.json
# example item in the list:
# {
# 	"2": {
# 		"carretera": "A-62",
# 		"id": "4",
# 		"imagen": "http://infocar.dgt.es/etraffic/data/camaras/4.jpg",
# 		"fecha": "2022/03/09 08:49:25",
# 		"sentido": "+",
# 		"latitud": "41.9227",
# 		"longitud": "-4.5063",
# 		"provincia": "34",
# 		"pk": "87.9"
# 	}
# }

# download and plot the images on a map

import json
import urllib.request
import folium
import os
from datetime import datetime

# create a map
m = folium.Map(location=[40.416775, -3.703790], zoom_start=6)


def fetch_data():
    # download the json file
    url = 'https://www.dgt.es/.content/.assets/json/camaras.json'
    urllib.request.urlretrieve(url, 'cameras.json')

    # load the json file
    with open('cameras.json') as f:
        data = json.load(f)

    return data

import sqlite3
from countcars import count_cars

def create_db():
    # create the database
    conn = sqlite3.connect('cameras.db')
    c = conn.cursor()
    # lat, lon, file, timestamp, cars (counted), highway, highway_position
    c.execute('''CREATE TABLE cameras
                    (lat real, lon real, file text, timestamp text, highway text, highway_position real, cars integer)''')


    conn.commit()


def save_data(data):
    # create a new directory with all the downloaded images
    if not os.path.exists('images'):
        os.makedirs('images')

    # create current timestamp directory
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    path = os.path.join('images', timestamp)
    os.makedirs(path)

    # save the json file
    with open(os.path.join(path, 'cameras.json'), 'w') as f:
        json.dump(data, f)

    conn = sqlite3.connect('cameras.db')
    c = conn.cursor()
    # download the images
    for item in data['camaras']:
        url = item['imagen']
        filename = url.split('/')[-1]
        print('Downloading', url, 'to', filename)
        try:
            urllib.request.urlretrieve(url, os.path.join(path, filename))
            count = count_cars(os.path.join(path, filename))
            # c.execute("INSERT INTO cameras VALUES (?, ?, ?, ?, ?)", (item['latitud'], item['longitud'], filename, timestamp, count))
            c.execute("INSERT INTO cameras VALUES (?, ?, ?, ?, ?, ?, ?)", (item['latitud'], item['longitud'], filename, timestamp, item['carretera'], item['pk'], count))
            conn.commit()
        except:
            print('Error downloading', url)
    c.close()
def main():
    if not os.path.exists('cameras.db'):
        create_db()
    data = fetch_data()
    save_data(data)

if __name__ == '__main__':
    main()

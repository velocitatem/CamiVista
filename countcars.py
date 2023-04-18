import cv2
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
import sys
import os

def count_cars(inputFile):
    im = cv2.imread(inputFile)
    bbox, label, conf = cv.detect_common_objects(im)
    output_image = draw_bbox(im, bbox, label, conf)
    # save the image with the same name as the input file
    cv2.imwrite(inputFile+"-aied.jpg", output_image)
    print('Number of cars in the image is '+ str(label.count('car')))
    return label.count('car')

import sqlite3
def main():
    # get the list of files in the current directory
    direct = '/mnt/s/Documents/Projects/SpainCameras/images/2023-04-14_10-13-34/'
    files = os.listdir(direct)
    # create a new database to store the results
    timestampNow = direct.split('/')[-1]
    dbName = 'count-cars1-'+timestampNow+'.db'
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    # create a table to store the results
    c.execute('''CREATE TABLE IF NOT EXISTS cars
                    (filename text, count integer)''')

    # loop through the files
    for file in files:
        # check if the file is an image
        if file.endswith('.jpg'):
            # count the cars in the image
            fullPath = os.path.join('/mnt/s/Documents/Projects/SpainCameras/images/2023-04-14_10-13-34/', file)
            count=count_cars(fullPath)
            # store the results in the database
            c.execute("INSERT INTO cars VALUES (?,?)", (file, count))
            conn.commit()
    conn.close()


if __name__ == '__main__':
    main()

# path: show_heatmap.py

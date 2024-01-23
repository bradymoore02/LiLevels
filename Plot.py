import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import numpy as np

def read_the_csv(filename):
    data = {}
    minx = 1e5
    maxx = 0
    miny = 1e5
    maxy = 0
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader, None)
        for row in csv_reader:
            frame = int(row[0])
            if len(row)>1:
                data[frame] = {'x': [], 'y': []} 
            for coord in row[1:]:
                x = float(coord.strip('()').split(',')[0])
                y = float(coord.strip('()').split(',')[1])
                data[frame]['x'].append(x)
                data[frame]['y'].append(y)
                if frame > 2:
                    if x < minx:
                        minx = x
                    if x > maxx:
                        maxx = x
                    if y < miny:
                        miny = y
                    if y > maxy:
                        maxy = y
    return data, minx, maxx, miny, maxy

def correct(xlist,ylist, slope_correction):
    newy = []

    for i, x in enumerate(xlist):
        newy.append(ylist[i]-slope_correction*x)
    return np.array(newy)

def scaling(channels, data):
    pixel_len = np.sqrt(data[1]['x'][1]-data[1]['x'][0])**2+(data[1]['y'][1]-data[1]['y'][0])
    real_len = channels*3 # in mm
    return real_len/pixel_len
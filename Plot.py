import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import csv
import numpy as np

def read_the_csv(filename):
    data = {}
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

    print(data.keys())
    x0, y0 = data[3]['x'][0], data[3]['y'][0]
    
    for frame in data.keys():
        data[frame]['x'] = [d-x0 for d in data[frame]['x']]
        data[frame]['y'] = [d-y0 for d in data[frame]['y']]
    
    return data, x0,y0

def correct(xlist,ylist, slope_correction):
    newy = []
    for i, x in enumerate(xlist):
        newy.append(ylist[i]-slope_correction*x)
    return np.array(newy)

def scaling(channels, data):
    pixel_len = np.sqrt(data[1]['x'][1]-data[1]['x'][0])**2+(data[1]['y'][1]-data[1]['y'][0])
    real_len = channels*3 # in mm
    print(real_len/pixel_len)
    return real_len/pixel_len
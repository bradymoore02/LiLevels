import matplotlib.pyplot as plt
import numpy as np
import csv
import Plot
## 60 fps for all videos ##


# Initialize lists for frames, x values, and y values
data = {}

# Path to the CSV file
VIDEO_NAME = 'PunchMouth_IIICropped'
csv_file_path = f'OutputCSVs/{VIDEO_NAME}.csv' 

FOLDER = f'PlotAnimation/{VIDEO_NAME}'
# Read CSV file and populate lists
data,x1,x2,y1,y2 = Plot.read_the_csv(csv_file_path)
            
# Print the lists
def correct(xlist,ylist):
    newy = []
    slope_correction = (data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])
    intercept = data[0]['x'][0]*slope_correction+data[0]['y'][0]
    for i, x in enumerate(xlist):
        newy.append(ylist[i]-slope_correction*x)
    return np.array(newy)

for frame in data.keys():
    if frame <3:
        continue
    plt.clf()
    slope_correction = float(data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])
    pixelscale = Plot.scaling(10, data)
    plt.xlim(x1*pixelscale,x2*pixelscale*1.1)
    plt.ylim(-y2*pixelscale-4,y2*pixelscale-2)      
    #plt.axis('equal')
    plt.plot(np.array(data[frame]['x'])[1:]*pixelscale, -correct(data[frame]['x'], data[frame]['y'])[1:]*pixelscale, label=f'Frame {frame}', marker='x')
    plt.title(f't = {round(float(frame)/60,3)} s')
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.draw()
    plt.pause(.5)
    plt.savefig(f'{FOLDER}/{frame}.png')
plt.show()
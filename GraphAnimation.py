import matplotlib.pyplot as plt
import numpy as np
import csv
import Plot
## 60 fps for all videos ##


# Initialize lists for frames, x values, and y values
data = {}

# Path to the CSV file
VIDEO_NAME = 'PunchMouth-Set2-1'

#VIDEO_NAME = 'Distributor_Filling_Crop'
csv_file_path = f'OutputCSVs/{VIDEO_NAME}.csv' 

FOLDER = f'PlotAnimation/{VIDEO_NAME}'
# Read CSV file and populate lists
data,x0,y0 = Plot.read_the_csv(csv_file_path)
            

slope_correction = float(data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])

pixelscale = Plot.scaling(10, data)

for frame in data.keys():
    if frame <3:
        continue
    plt.clf()
    #plt.xlim(x1*pixelscale,x2*pixelscale*1.1)
    #plt.ylim(-y2*pixelscale-4,y2*pixelscale-2) 
    plt.xlim(0,45)   
    plt.ylim(0,7)  
    #plt.axis('equal')
    plt.plot(np.array(data[frame]['x'])*pixelscale, -Plot.correct(data[frame]['x'], data[frame]['y'],slope_correction)*pixelscale+6.7, label=f'Frame {frame}', marker='x')
    plt.title(f't = {round(float(frame)/60,3)} s')
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.draw()
    plt.pause(.5)
    plt.savefig(f'{FOLDER}/{str(frame).zfill(3)}.png')
plt.show()
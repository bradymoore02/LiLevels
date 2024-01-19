import matplotlib.pyplot as plt
import numpy as np
import csv

## 60 fps for all videos ##


# Initialize lists for frames, x values, and y values
plotting_dict = {}

# Path to the CSV file
csv_file_path = 'OutputCSVs/1-2-30to40A.csv' 

# Read CSV file and populate lists
with open(csv_file_path, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    
    next(csv_reader, None)
    for row in csv_reader:
        frame = int(row[0])
        if len(row)>1:
            plotting_dict[frame] = {'x': [], 'y': []} 
        for coord in row[1:]:
            plotting_dict[frame]['x'].append(float(coord.strip('()').split(',')[0]))
            plotting_dict[frame]['y'].append(float(coord.strip('()').split(',')[1]))
            
# Print the lists
print("Frames:", plotting_dict)
def correct(xlist,ylist):
    newy = []
    slope_correction = (plotting_dict[0]['y'][1]-plotting_dict[0]['y'][0])/(plotting_dict[0]['x'][1]-plotting_dict[0]['x'][0])
    intercept = plotting_dict[0]['x'][0]*slope_correction+plotting_dict[0]['y'][0]
    for i, x in enumerate(xlist):
        newy.append(ylist[i]-slope_correction*x)
    return np.array(newy)

for frame in plotting_dict.keys():
    plt.clf()
    plt.xlim(0,50)
    plt.ylim(0,6)    
    plt.gca().set_aspect('equal')  
    print(plotting_dict[0]['y'][1],plotting_dict[0]['y'][0],plotting_dict[0]['x'][1],plotting_dict[0]['x'][0])
  
    slope_correction = float(plotting_dict[0]['y'][1]-plotting_dict[0]['y'][0])/(plotting_dict[0]['x'][1]-plotting_dict[0]['x'][0])
    intercept = plotting_dict[0]['x'][0]*slope_correction+plotting_dict[0]['y'][0]
    print(slope_correction, intercept)
    
    
    #plt.plot(plotting_dict[frame]['x'], -np.array(plotting_dict[frame]['x'])*slope_correction+intercept)
    
    pixelscale = 35.4
    plt.plot(np.array(plotting_dict[frame]['x'])[1:]/pixelscale, -correct(plotting_dict[frame]['x'], plotting_dict[frame]['y'])[1:]/pixelscale+25, label=f'Frame {frame}', marker='x')
    print(plotting_dict[0]['y'][1],plotting_dict[0]['y'][0],plotting_dict[0]['x'][1],plotting_dict[0]['x'][0])
    plt.title(f't = {round(float(frame)/60,3)} s')
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.draw()
    plt.pause(.5)
plt.show()
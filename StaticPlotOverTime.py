import matplotlib.pyplot as plt
import numpy as np
import csv
import Plot

VIDEO_NAME = 'PunchMouth-Set2-1'
#VIDEO_NAME = 'Distributor_Filling_Crop'

data, x0,y0= Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
scale_factor = Plot.scaling(10, data)
#scale_factor = 0.0354
slope_correction = (data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])

#frames_to_plot = [8,14,20,26]
frames_to_plot = [69,81,95,109]
#frames_to_plot = [10,44,73,105]
print(data)
for frame in frames_to_plot:
    if frame > 2:
        plt.plot(np.array(data[frame]['x'])*scale_factor, -Plot.correct(data[frame]['x'],data[frame]['y'], slope_correction)*scale_factor+6.7, label=f't={round(frame/60,2)}',marker='o')
plt.ylim(0,5)
plt.xlim(0,55)
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.legend()
#plt.gca().set_aspect('equal')
plt.savefig(f'StaticPlotsOverTime/{VIDEO_NAME}.png',dpi=300)
plt.show()
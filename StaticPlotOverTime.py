import matplotlib.pyplot as plt
import numpy as np
import csv
import Plot

VIDEO_NAME = 'PunchMouth_IIICropped'
data, a,b,c,d = Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
scale_factor = Plot.scaling(10, data)
slope_correction = (data[0]['y'][1]-data[0]['y'][0])/(data[0]['x'][1]-data[0]['x'][0])

frames_to_plot = [8,14,20,26]
print(data)
for frame in frames_to_plot:
    if frame > 2:
        plt.plot(np.array(data[frame]['x'])*scale_factor, -Plot.correct(data[frame]['x'],data[frame]['y'], slope_correction)*scale_factor, label=f't={round(frame/60,2)}')
plt.xlabel('x [mm]')
plt.ylabel('y [mm]')
plt.legend()
#plt.gca().set_aspect('equal')
plt.show()
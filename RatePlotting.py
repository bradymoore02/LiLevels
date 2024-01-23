import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import Plot

VIDEO_NAME = 'PunchMouth_IIICropped'
data, a,b,c,d = Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
print(data)
scale_factor = Plot.scaling(10, data)
channels = {}
frames = []
for channel in range(11):
    channels[channel] = []
    for frame in data.keys():
        if frame > 2:
            channels[channel].append(-data[frame]['y'][channel]*scale_factor)
            if channel ==0:
                frames.append(frame)

for channel in channels.keys():
    x =frames
    y = channels[channel]
    
    coeffs = np.polyfit(x, y, 3)
    poly_func = np.poly1d(coeffs)
    deriv_coeff = np.polyder(coeffs)
    deriv_func = np.poly1d(deriv_coeff)
    xfit = np.linspace(min(x), max(x), 100)
    plt.figure(0)
    plt.plot(x, y, label=channel)
    plt.plot(xfit, poly_func(xfit), c = 'k')
    #plt.show()
    plt.figure(1)
    plt.plot(xfit, deriv_func(xfit), label=f'Channel {channel}')
plt.legend()
plt.xlabel("Frame number")
plt.ylabel("Rise rate [mm/frame]")
plt.show()
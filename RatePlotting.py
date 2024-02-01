import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import csv
import Plot
from scipy.optimize import curve_fit

def poly2(x,a,b):
    return x**2*a+x*b #+c implied

def func23(x,a,b):
    return a*x**(2/3)+b

def func23d(x,a,b):
    return 2/3*a*x**(-1/3)

def poly1(x, a, b):
    return x*a*2 + b

#VIDEO_NAME = 'PunchMouth-Set2-1'
VIDEO_NAME = 'PunchMouth-Set2-3-'

data, x0,y0 = Plot.read_the_csv(f"OutputCSVs/{VIDEO_NAME}.csv")
print(data)
scale_factor = Plot.scaling(10, data)
channels = {}
frames = []
for channel in range(12):
    channels[channel] = []
    for frame in data.keys():
        if frame > 3:
            channels[channel].append(-data[frame]['y'][channel]*scale_factor)
            if channel ==0:
                frames.append(frame)


for channel in channels.keys():
    x =frames
    y = channels[channel]
    x_adjusted = np.array(x)-x[0]
    y_adjusted = np.array(y)-y[0]
    
    coeffs = np.polyfit(x, y, 3)
    poly_func = np.poly1d(coeffs)
    deriv_coeff = np.polyder(coeffs)
    deriv_func = np.poly1d(deriv_coeff)
    
    coeff0 = np.polyfit(x, y_adjusted,2)
    poly_func0 = np.poly1d(coeff0)
    deriv_coeff0 = np.polyder(coeff0)
    deriv_func_0 = np.poly1d(deriv_coeff0)
    xfit = np.linspace(min(x), max(x), 100)
    
    params, cov = curve_fit(poly2, x_adjusted,y_adjusted)
    
    params23, cov = curve_fit(func23,x_adjusted,y_adjusted)
    
    plt.figure(0)
    plt.plot(x, y, label=channel)
    plt.plot(xfit, poly2(xfit-x[0],*params)+y[0], c = 'k')
    #plt.show()
    plt.figure(1)
    
    
    plt.plot(xfit/60, poly1(xfit-x[0],*params)*60, label=f'Channel {channel+1}')
    
    
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Rise rate [mm/s]")
plt.savefig(f'RatePlotting/{VIDEO_NAME}.png',dpi=300)
plt.show()